"""
Model Training & Serialization Module for Spam Message Detector.
Trains TF-IDF vectorizer and Soft Voting Ensemble ML models.
Outputs serialized model files: spam_model.pkl, vectorizer.pkl, metrics.json.
"""

import os
import json
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

from dataset import get_raw_dataset
from nlp_preprocessor import clean_text

MODEL_FILE = "spam_model.pkl"
VECTORIZER_FILE = "vectorizer.pkl"
METRICS_FILE = "metrics.json"

def train_and_save_model():
    """
    Trains the vectorizer and ML ensemble model, evaluates performance metrics,
    and saves serialized artifacts to disk.
    """
    print("[*] Loading multi-domain training dataset...")
    raw_data = get_raw_dataset()
    
    texts = [clean_text(item["text"]) for item in raw_data]
    labels = np.array([item["label"] for item in raw_data])
    channels = [item["channel"] for item in raw_data]
    
    print(f"[*] Total dataset size: {len(texts)} samples (Spam: {sum(labels)}, Ham: {len(labels) - sum(labels)})")
    
    # 1. Feature Extraction via TF-IDF Vectorizer
    print("[*] Vectorizing text features with TF-IDF (unigrams + bigrams)...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=1,
        max_features=5000
    )
    X = vectorizer.fit_transform(texts)
    
    # 2. Instantiate base classifiers
    mnb = MultinomialNB(alpha=0.2)
    lr = LogisticRegression(C=1.5, max_iter=500, solver='lbfgs')
    svc_base = LinearSVC(C=1.0, max_iter=2000, random_state=42)
    svc = CalibratedClassifierCV(svc_base)  # Enables predict_proba support for Soft Voting
    
    # 3. Fit base models
    mnb.fit(X, labels)
    lr.fit(X, labels)
    svc.fit(X, labels)
    
    # Evaluate individual base models
    mnb_preds = mnb.predict(X)
    lr_preds = lr.predict(X)
    svc_preds = svc.predict(X)
    
    # 4. Ensemble Classifier (Soft Voting)
    print("[*] Training Soft Voting Ensemble Classifier (Naive Bayes + Logistic Regression + Linear SVC)...")
    ensemble = VotingClassifier(
        estimators=[
            ('mnb', mnb),
            ('lr', lr),
            ('svc', svc)
        ],
        voting='soft'
    )
    ensemble.fit(X, labels)
    
    # 5. Model Evaluation
    ensemble_preds = ensemble.predict(X)
    
    acc = float(accuracy_score(labels, ensemble_preds))
    prec = float(precision_score(labels, ensemble_preds, zero_division=0))
    rec = float(recall_score(labels, ensemble_preds, zero_division=0))
    f1 = float(f1_score(labels, ensemble_preds, zero_division=0))
    cm = confusion_matrix(labels, ensemble_preds).tolist()
    
    metrics = {
        "dataset_size": len(texts),
        "spam_count": int(sum(labels)),
        "ham_count": int(len(labels) - sum(labels)),
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "confusion_matrix": {
            "tn": cm[0][0] if len(cm) > 0 else 0,
            "fp": cm[0][1] if len(cm) > 0 else 0,
            "fn": cm[1][0] if len(cm) > 1 else 0,
            "tp": cm[1][1] if len(cm) > 1 else 0
        },
        "model_comparison": {
            "Naive Bayes": {
                "accuracy": round(float(accuracy_score(labels, mnb_preds)), 4),
                "f1_score": round(float(f1_score(labels, mnb_preds, zero_division=0)), 4)
            },
            "Logistic Regression": {
                "accuracy": round(float(accuracy_score(labels, lr_preds)), 4),
                "f1_score": round(float(f1_score(labels, lr_preds, zero_division=0)), 4)
            },
            "Linear Support Vector Machine": {
                "accuracy": round(float(accuracy_score(labels, svc_preds)), 4),
                "f1_score": round(float(f1_score(labels, svc_preds, zero_division=0)), 4)
            },
            "Soft Voting Ensemble (Active)": {
                "accuracy": round(acc, 4),
                "f1_score": round(f1, 4)
            }
        },
        "feature_count": len(vectorizer.get_feature_names_out())
    }
    
    # 6. Save artifacts
    print(f"[*] Saving serialized model to '{MODEL_FILE}'...")
    joblib.dump(ensemble, MODEL_FILE)
    
    print(f"[*] Saving TF-IDF vectorizer to '{VECTORIZER_FILE}'...")
    joblib.dump(vectorizer, VECTORIZER_FILE)
    
    print(f"[*] Saving metrics report to '{METRICS_FILE}'...")
    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
        
    print(f"[+] Training complete! Model accuracy: {acc * 100:.2f}%, F1-Score: {f1 * 100:.2f}%")
    return metrics

if __name__ == "__main__":
    train_and_save_model()
