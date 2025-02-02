import sys
import os
from flask import Flask, request, jsonify
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'ai_models', 'scripts'))

from ai_models.scripts.main import assign_donors
from ai_models.scripts.news_report import get_summarized_news

import requests

app = Flask(__name__)

@app.route('/api/get_summarized_news', methods=['POST'])
def get_summarized_news_route():
    data = request.json
    user_description = data.get('user_description')

    if not user_description:
        return jsonify({"error": "Invalid input"}), 400

    summarized_news = get_summarized_news(user_description)
    return jsonify(summarized_news)



app = Flask(__name__)

@app.route('/api/get_top_donors', methods=['POST'])
def get_top_donors():
    data = request.json
    victim_text = data.get('victim_text')
    victim_location = data.get('victim_location')

    if not victim_text or not victim_location:
        return jsonify({"error": "Invalid input"}), 400

    try:
        donor_response = requests.get("http://localhost:3001/donors")
        donor_response.raise_for_status()
        donors = donor_response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch donor data", "details": str(e)}), 500

    top_donors, predicted_intent = assign_donors(victim_text, victim_location, donors)
    
    return jsonify({"top_donors": top_donors, "predicted_intent": predicted_intent})

if __name__ == '__main__':
    app.run(debug=True)
