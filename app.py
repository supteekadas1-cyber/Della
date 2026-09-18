from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question")
        subject = data.get("subject", "General")

        if not question:
            return jsonify({"answer": "Please enter a question."})

        # Send the question to Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": (
                    "You are an AI Study Assistant. "
                    "Explain topics clearly and simply for a college student. "
                    "Use examples when helpful. "
                    "For programming questions, explain the code clearly. "
                    "Keep answers useful for exams and study. "
                    f"\n\nStudent: {subject}\nStudent's question: {question}"
                ),
                "stream": False
            }
        )

        response.raise_for_status()

        result = response.json()

        answer = result.get("response", "I couldn't generate an answer.")

        return jsonify({"answer": answer})

    except Exception as e:
        print("ERROR:", repr(e))
        return jsonify({
            "answer": "Sorry, I couldn't process your question right now."
        })


if __name__ == "__main__":
    app.run(debug=True)

