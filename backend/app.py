from flask import Flask, request, jsonify, render_template
import numpy as np
import os
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from flask_cors import CORS

app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend")
CORS(app)

base_dir = os.path.dirname(os.path.abspath(__file__))

# Global lazy variables
model = None
tokenizer = None
index_to_word = None
MAXLEN = 200

def load_model_and_tokenizer():
    global model, tokenizer, index_to_word

    if model is None or tokenizer is None:
        print("🔄 Loading model and tokenizer...")
        model_path = os.path.join(base_dir, "wordsuggestion.keras")
        tokenizer_path = os.path.join(base_dir, "word-suggestion-tokenizer.pkl")

        model = tf.keras.models.load_model(model_path)
        with open(tokenizer_path, "rb") as f:
            tokenizer = pickle.load(f)

        index_to_word = tokenizer.index_word
        print("✅ Model & Tokenizer loaded.")

def predict_next_words(text, n=3):
    load_model_and_tokenizer()  # ensure lazy load happens only when needed

    seq = tokenizer.texts_to_sequences([text])[0]
    seq = pad_sequences([seq], maxlen=MAXLEN-1, padding="pre")

    pred = model.predict(seq, verbose=0)[0]
    print("Prediction vector:", pred[:10])  # Debug: first 10 probs

    top_indices = pred.argsort()[-n:][::-1]
    print("Top indices:", top_indices)

    return [index_to_word[i] for i in top_indices if i in index_to_word]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/suggest", methods=["POST"])
def api_suggest():
    data = request.get_json()
    text = data.get("input_text", "")
    suggestions = predict_next_words(text, n=3) if text.strip() else []
    return jsonify({"input": text, "suggestions": suggestions})

if __name__ == "__main__":
    app.run(debug=True)
