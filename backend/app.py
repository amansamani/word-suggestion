from flask import Flask, request, jsonify, render_template
import numpy as np
import os
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from flask_cors import CORS

app = Flask(__name__, static_folder="../frontend", template_folder="../frontend")
CORS(app)

base_dir = os.path.dirname(os.path.abspath(__file__))

# Load model + tokenizer
model_path = os.path.join(base_dir, "wordsuggestion.keras")
model = tf.keras.models.load_model(model_path)

tokenizer_path = os.path.join(base_dir, "word-suggestion-tokenizer.pkl")
with open(tokenizer_path, "rb") as f:
    tokenizer = pickle.load(f)

MAXLEN = 200
index_to_word = tokenizer.index_word


def predict_next_words(text, n=3):
    seq = tokenizer.texts_to_sequences([text])[0]
    seq = pad_sequences([seq], maxlen=MAXLEN-1, padding="pre")

    pred = model.predict(seq, verbose=0)[0]
    print("Prediction vector:", pred[:10])  # show first 10 probabilities

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
