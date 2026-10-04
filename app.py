"""
Flask Web Application Backend for Spam Message Detector.
Provides REST API endpoints for single and batch message classification,
Explainable AI (XAI) analysis, model metrics, preset examples, and UI serving.
"""

import os
import json
import joblib
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from nlp_preprocessor import clean_text, extract_meta_features, analyze_highlights
from dataset import DATASET_SAMPLES

app = Flask(__name__, static_folder="static")
CORS(app)

MODEL_FILE = "spam_model.pkl"
VECTORIZER_FILE = "vectorizer.pkl"
METRICS_FILE = "metrics.json"

model = None
vectorizer = None
metrics_data = {}

def load_artifacts():
    """Loads pre-trained model, vectorizer, and metrics."""
    global model, vectorizer, metrics_data
    if not os.path.exists(MODEL_FILE) or not os.path.exists(VECTORIZER_FILE):
        print("[!] Serialized model or vectorizer not found. Running train_model.py...")
        from train_model import train_and_save_model
        train_and_save_model()
        
    print(f"[*] Loading model from {MODEL_FILE}...")
    model = joblib.load(MODEL_FILE)
    print(f"[*] Loading vectorizer from {VECTORIZER_FILE}...")
    vectorizer = joblib.load(VECTORIZER_FILE)
    
    if os.path.exists(METRICS_FILE):
        with open(METRICS_FILE, "r", encoding="utf-8") as f:
            metrics_data = json.load(f)

# Initialize artifacts on load
load_artifacts()

def generate_risk_reasons(meta, text, is_spam, proba):
    """Generates human-readable bullet points explaining the classification verdict."""
    reasons = []
    lowered = text.lower()
    
    if is_spam:
        if meta["urgency_score"] > 0:
            reasons.append(f"High sense of urgency detected ({meta['urgency_score']} urgency call-to-actions).")
        if meta["url_count"] > 0:
            reasons.append(f"Contains {meta['url_count']} external web link(s) / suspicious URL domain.")
        if meta["has_currency"]:
            reasons.append("Promotes financial claims, currency symbols, or monetary rewards.")
        if meta["uppercase_ratio"] > 0.15:
            reasons.append(f"Excessive ALL-CAPS text ratio ({int(meta['uppercase_ratio'] * 100)}%).")
        if meta["digit_ratio"] > 0.10:
            reasons.append("High density of phone numbers, codes, or price numbers.")
        if not reasons:
            reasons.append("Contains known spam pattern phrase combinations and vocabulary.")
    else:
        if meta["url_count"] == 0:
            reasons.append("No suspicious external URLs or links detected.")
        if meta["urgency_score"] == 0:
            reasons.append("Normal, conversational tone without high-pressure urgency.")
        reasons.append("Natural text distribution matching legitimate conversational patterns.")
        
    return reasons

@app.route("/")
def serve_index():
    """Serves the primary web application interface."""
    return send_from_directory("static", "index.html")

@app.route("/<path:filename>")
def serve_static(filename):
    """Serves static assets (CSS, JS, images, icons)."""
    return send_from_directory("static", filename)

@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "online",
        "model_loaded": model is not None,
        "vectorizer_loaded": vectorizer is not None,
        "features_count": len(vectorizer.get_feature_names_out()) if vectorizer else 0
    })

@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Analyzes a single message (SMS, Email, or Comment).
    Expects JSON payload: {"text": "...", "channel": "sms"|"email"|"comment", "subject": "..."}
    """
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    channel = data.get("channel", "sms").lower()
    subject = data.get("subject", "").strip()
    
    if not text:
        return jsonify({"error": "No message text provided."}), 400
        
    full_text = f"Subject: {subject}\n{text}" if (channel == "email" and subject) else text
    
    # Preprocess
    cleaned = clean_text(full_text)
    meta = extract_meta_features(full_text)
    highlights = analyze_highlights(full_text)
    
    # Transform & Predict
    vectorized = vectorizer.transform([cleaned])
    probabilities = model.predict_proba(vectorized)[0]
    
    # Index 1 = Spam, Index 0 = Ham
    spam_proba = float(probabilities[1])
    is_spam = spam_proba >= 0.5
    confidence = round((spam_proba if is_spam else (1.0 - spam_proba)) * 100, 1)
    
    reasons = generate_risk_reasons(meta, full_text, is_spam, spam_proba)
    
    return jsonify({
        "label": "SPAM" if is_spam else "NOT SPAM",
        "is_spam": is_spam,
        "confidence": confidence,
        "spam_probability": round(spam_proba, 4),
        "channel": channel,
        "meta_features": meta,
        "highlights": highlights,
        "risk_reasons": reasons
    })

@app.route("/api/batch-predict", methods=["POST"])
def batch_predict():
    """
    Analyzes a batch list of messages or CSV items.
    Expects JSON: {"messages": [{"text": "...", "channel": "..."}, ...]}
    """
    data = request.get_json() or {}
    items = data.get("messages", [])
    
    if not items or not isinstance(items, list):
        return jsonify({"error": "No valid array of messages provided."}), 400
        
    results = []
    spam_count = 0
    
    for idx, item in enumerate(items):
        if isinstance(item, str):
            text = item
            channel = "sms"
        else:
            text = item.get("text", "")
            channel = item.get("channel", "sms")
            
        if not text.strip():
            continue
            
        cleaned = clean_text(text)
        meta = extract_meta_features(text)
        vectorized = vectorizer.transform([cleaned])
        probabilities = model.predict_proba(vectorized)[0]
        
        spam_proba = float(probabilities[1])
        is_spam = spam_proba >= 0.5
        if is_spam:
            spam_count += 1
            
        results.append({
            "id": idx + 1,
            "text": text,
            "channel": channel,
            "label": "SPAM" if is_spam else "NOT SPAM",
            "is_spam": is_spam,
            "spam_probability": round(spam_proba, 4),
            "confidence": round((spam_proba if is_spam else (1.0 - spam_proba)) * 100, 1),
            "meta_features": meta
        })
        
    total = len(results)
    return jsonify({
        "total": total,
        "spam_count": spam_count,
        "ham_count": total - spam_count,
        "spam_ratio": round((spam_count / total * 100), 1) if total > 0 else 0.0,
        "results": results
    })

@app.route("/api/metrics", methods=["GET"])
def get_metrics():
    """Returns stored model metrics and confusion matrix."""
    return jsonify(metrics_data)

@app.route("/api/presets", methods=["GET"])
def get_presets():
    """Returns preset test cases for UI fast-testing."""
    presets = {
        "sms_spam": "URGENT! You have won a $1,000 Walmart Gift Card. Click http://bit.ly/claim-card now to claim your prize! Reply STOP to optout",
        "sms_ham": "Hey Alex, are we still meeting for lunch at 12:30 PM at the diner?",
        "email_spam": "Subject: URGENT: Inheritance Transfer of $14.5 Million USD\nDear Friend, I am Mr. Abacha writing to seek your assistance in transferring $14,500,000 from a dormant bank account. Reply immediately with your full name, bank details, and copy of passport.",
        "email_ham": "Subject: Q3 Financial Performance Review & Strategy Meeting Agenda\nHi Team, Attached is the draft agenda for our Q3 review scheduled for Thursday at 10 AM EST. Please review the revenue figures and bring your department updates.",
        "comment_spam": "I made $15,000 in one month trading forex thanks to Mrs. Sarah! Contact her on WhatsApp +1-987-654-3210 for guaranteed signals!",
        "comment_ham": "This explanation was super clear and helpful! Loved how you broke down the NLP preprocessing steps."
    }
    return jsonify(presets)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"[*] Starting Spam Detector Web App on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
