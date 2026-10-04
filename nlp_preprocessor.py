"""
NLP Preprocessor Module for Spam Message Detector.
Provides text cleaning, normalization, feature engineering,
and explainable trigger word highlight analysis.
"""

import re
import string

# Known spam keywords with associated risk levels for Explainable AI (XAI)
SPAM_TRIGGER_LEXICON = {
    "high": [
        "urgent", "winner", "won", "claim", "prize", "lottery", "cash", "free",
        "compromised", "suspended", "verify", "password", "bank", "ssn", "inheritance",
        "bitcoin", "crypto", "forex", "xanax", "valium", "oxycontin", "viagra", "cialis",
        "sub4sub", "whatsapp", "telegram", "hacked", "88010", "80082"
    ],
    "medium": [
        "alert", "notice", "action", "immediately", "limited", "offer", "discount",
        "gift", "card", "refund", "guaranteed", "investment", "earn", "income",
        "overdue", "invoice", "unclaimed", "prescription", "followers", "subscribers",
        "click", "link", "order", "delivery", "fee", "charged", "cancel"
    ]
}

def normalize_entities(text):
    """
    Replaces URLs, phone numbers, email addresses, and currency strings with canonical tokens.
    """
    if not text:
        return ""

    # Replace URLs
    text = re.sub(r'https?://\S+|www\.\S+|t\.me/\S+', ' <URL> ', text)
    # Replace Email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', ' <EMAIL> ', text)
    # Replace Phone numbers (various formats)
    text = re.sub(r'(\+\d{1,3}[\s-]?)?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}|\b\d{4}\s?\d{6}\b|\b0800\s?\d+\b', ' <PHONE> ', text)
    # Replace Currency amounts
    text = re.sub(r'[\$£€]\d+(?:,\d{3})*(?:\.\d{2})?|\b\d+\s?(?:USD|GBP|EUR|dollars|pounds)\b', ' <CURRENCY> ', text)
    
    return text

def clean_text(text):
    """
    Full text cleaning pipeline for NLP feature vectorization.
    """
    if not text:
        return ""
    
    # 1. Entity Normalization
    normalized = normalize_entities(text)
    
    # 2. Lowercasing
    lowered = normalized.lower()
    
    # 3. Punctuation removal (keep tokens <URL>, <PHONE>, etc.)
    cleaned = re.sub(r'[^\w\s<>]', ' ', lowered)
    
    # 4. Collapse extra whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    return cleaned

def extract_meta_features(text):
    """
    Extracts numerical metadata features from raw text to boost classification accuracy.
    """
    if not text:
        return {
            "length": 0,
            "uppercase_ratio": 0.0,
            "digit_ratio": 0.0,
            "url_count": 0,
            "urgency_score": 0,
            "has_currency": 0
        }
    
    length = len(text)
    uppercase_count = sum(1 for c in text if c.isupper())
    digit_count = sum(1 for c in text if c.isdigit())
    
    uppercase_ratio = uppercase_count / length if length > 0 else 0.0
    digit_ratio = digit_count / length if length > 0 else 0.0
    
    # Count URLs
    url_count = len(re.findall(r'https?://\S+|www\.\S+|t\.me/\S+', text))
    
    # Count currency indicators
    has_currency = 1 if re.search(r'[\$£€]|\bUSD\b|\bGBP\b|\bEUR\b', text) else 0
    
    # Urgency keywords check
    lowered = text.lower()
    urgency_keywords = ["urgent", "immediately", "now", "final notice", "action required", "instant", "fast", "today", "alert", "expire"]
    urgency_score = sum(1 for kw in urgency_keywords if kw in lowered)
    
    return {
        "length": length,
        "uppercase_ratio": round(uppercase_ratio, 3),
        "digit_ratio": round(digit_ratio, 3),
        "url_count": url_count,
        "urgency_score": urgency_score,
        "has_currency": has_currency
    }

def analyze_highlights(text):
    """
    Analyzes input text and tags words with risk levels for Explainable AI (XAI) UI visualizer.
    Returns list of token dicts: [{"word": "URGENT!", "risk": "high", "reason": "High-risk spam trigger"}]
    """
    if not text:
        return []
    
    # Split text keeping spaces/punctuation intact for reconstruction
    tokens = re.split(r'(\s+)', text)
    result = []
    
    for token in tokens:
        if not token.strip():
            result.append({"text": token, "risk": "none"})
            continue
            
        clean_word = re.sub(r'[^\w]', '', token.lower())
        
        # Check against high-risk lexicon
        if clean_word in SPAM_TRIGGER_LEXICON["high"] or token.startswith("http") or token.startswith("www"):
            result.append({
                "text": token,
                "risk": "high",
                "reason": f"High-risk spam trigger keyword ('{clean_word or token}')"
            })
        elif clean_word in SPAM_TRIGGER_LEXICON["medium"]:
            result.append({
                "text": token,
                "risk": "medium",
                "reason": f"Promotional/Urgency indicator ('{clean_word}')"
            })
        elif token.isupper() and len(token) > 3 and token.isalpha():
            result.append({
                "text": token,
                "risk": "medium",
                "reason": "Aggressive ALL-CAPS formatting signal"
            })
        else:
            result.append({"text": token, "risk": "none"})
            
    return result
