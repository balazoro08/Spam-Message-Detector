# ShieldSpam AI — Smart Multi-Channel Spam Message Detector

![Python Version](https://img.shields.io/badge/Python-3.13-blue.svg)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.9-orange.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

**ShieldSpam AI** is an advanced NLP and Machine Learning application designed to detect spam and malicious phishing messages across multiple domains: **SMS / Text messages**, **Emails**, and **Social Media / Blog Comments**.

Features an **Explainable AI (XAI)** engine that highlights suspicious trigger words in real time, a **Batch File Scanner**, and a model analytics dashboard.

---

## 🌟 Key Features

- 📱 **Multi-Channel Domain Support**: Specialized detection tailored for **SMS**, **Email (Subject + Body)**, and **Social Media Comments**.
- 🤖 **Soft Voting Ensemble Classifier**: Combines **Multinomial Naive Bayes**, **Logistic Regression**, and **Linear Support Vector Classifier (SVC)** for high accuracy and robust generalization.
- 🔍 **Explainable AI (XAI) Word Highlighting**: Visually highlights high-risk spam keywords (e.g. *URGENT*, *claim*, *http://bit.ly*, *free*, *crypto*) with risk tooltips and signal breakdown.
- ⚡ **Real-Time Interactive UI**: Dark-mode glassmorphism interface built with Vanilla JS/CSS (no Node build step required).
- 📊 **Batch Scanner & CSV Export**: Drag-and-drop CSV datasets or bulk text messages to analyze at scale and export results.
- 📈 **Model Performance Dashboard**: Live KPI metrics (Accuracy, Precision, Recall, F1 Score) and Confusion Matrix grid.

---

## 🛠️ Technology Stack

- **Backend & ML**: Python 3.13, Scikit-Learn, NLTK, Joblib, NumPy, Pandas
- **API Framework**: Flask, Flask-CORS
- **Frontend**: Vanilla HTML5, CSS3 (Glassmorphism & HSL Color System), JavaScript ES6+


## 📊 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/predict` | Analyzes a single message (SMS, Email, or Comment) |
| `POST` | `/api/batch-predict` | Analyzes a list of messages or CSV rows |
| `GET` | `/api/metrics` | Returns model accuracy, confusion matrix, and benchmark scores |
| `GET` | `/api/presets` | Returns pre-configured spam and safe test examples |
| `GET` | `/api/health` | Health check and active vectorizer feature count |

---

## 📁 Repository Structure

```
├── app.py                # Flask API server & static UI router
├── dataset.py            # Multi-channel training & testing dataset
├── nlp_preprocessor.py   # Text cleaning, entity normalization & XAI highlighter
├── train_model.py        # ML training pipeline & artifact generator
├── requirements.txt      # Python package dependencies
├── README.md             # Project documentation
└── static/
    ├── index.html        # Single-page web application UI
    ├── styles.css        # Modern glassmorphism CSS design system
    └── app.js            # Client UI interaction & API consumer
```

---

## 📜 License

MIT License. Open source and free for educational and commercial use.
