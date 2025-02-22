import openai
from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
openai.api_key = "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"  # Replace with your OpenAI API key

# MongoDB setup
MONGO_URI = "mongodb://localhost:27017/"  # Change if needed
client = MongoClient(MONGO_URI)
db = client["chatbot_db"]  # Database name
questions_collection = db["questions"]  # Collection name

# Route to handle user queries
@app.route("/ask", methods=["POST"])
def handle_query():
    data = request.get_json()
    user_query = data.get("query")
    user_name = "Anonymous"

    # Store the question in MongoDB
    questions_collection.insert_one({
        "question": user_query,
        "user": user_name,
        "timestamp": datetime.utcnow(),
    })

    # Get AI response from OpenAI
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_query,
        max_tokens=150
    )

    answer = response.choices[0].text.strip()
    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(debug=True)
