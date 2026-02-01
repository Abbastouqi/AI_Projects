#!/usr/bin/env python3
"""
Medical Triage Chatbot - Inference Script
=========================================
Load trained model and predict urgency from patient text.

Usage:
    python inference.py "I have severe chest pain"
    python inference.py --interactive
"""

import joblib
import sys
import argparse
import re

# Load model and vectorizer
print("Loading model...")
model = joblib.load('model_artifacts/svm_triage_model.pkl')
vectorizer = joblib.load('model_artifacts/tfidf_vectorizer.pkl')
print("✅ Model loaded!\n")

# Preprocessing function (embedded for standalone use)
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download if needed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    """Clean and preprocess medical text"""
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join(text.split())
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words or word in ['not', 'no', 'never']]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)

def predict_urgency(text):
    """Predict urgency level with safety rules"""
    text_lower = text.lower()
    
    # Emergency keywords override
    emergency_keywords = [
        'cant breathe', 'cannot breathe', 'difficulty breathing', 
        'shortness of breath', 'chest pain', 'heart attack', 'unconscious',
        'not responding', 'seizure', 'severe bleeding', 'wont stop bleeding',
        'passed out', 'suicide', 'allergic reaction', 'throat swelling'
    ]
    
    for keyword in emergency_keywords:
        if keyword in text_lower:
            return 'Emergency', 0.95, 'Safety Rule'
    
    # ML Prediction
    cleaned = preprocess_text(text)
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)[0]
    confidence = min(abs(max(model.decision_function(vector)[0])) / 2, 0.95)
    
    return prediction, confidence, 'ML Model'

def main():
    parser = argparse.ArgumentParser(description='Medical Triage Chatbot')
    parser.add_argument('text', nargs='?', help='Patient description')
    parser.add_argument('--interactive', '-i', action='store_true', 
                        help='Interactive mode')
    
    args = parser.parse_args()
    
    actions = {
        'Emergency': '🚨 Call emergency services (911) or go to ER immediately!',
        'Urgent': '⚠️ See a doctor within 24 hours. Consider urgent care.',
        'Non-urgent': '💚 Schedule routine appointment or monitor symptoms.'
    }
    
    if args.interactive:
        print("🏥 Medical Triage Chatbot (Interactive Mode)")
        print("Type 'quit' to exit\n")
        while True:
            text = input("Patient description: ")
            if text.lower() == 'quit':
                break
            urgency, conf, method = predict_urgency(text)
            print(f"  Urgency: {urgency} ({method}, {conf:.1%} confidence)")
            print(f"  Action: {actions[urgency]}\n")
    
    elif args.text:
        urgency, conf, method = predict_urgency(args.text)
        print(f"Patient: '{args.text}'")
        print(f"Urgency: {urgency}")
        print(f"Method: {method} ({conf:.1%} confidence)")
        print(f"Action: {actions[urgency]}")
    
    else:
        # Demo mode
        print("🏥 Medical Triage Chatbot - Demo")
        print("="*60)
        test_cases = [
            "I have severe chest pain and I can't breathe properly",
            "My ankle hurts a bit after jogging yesterday",
            "I have a small pimple on my nose"
        ]
        for text in test_cases:
            urgency, conf, method = predict_urgency(text)
            print(f"\n📝 {text}")
            print(f"⚡ {urgency} ({method}, {conf:.1%})")
            print(f"✅ {actions[urgency]}")

if __name__ == "__main__":
    main()
