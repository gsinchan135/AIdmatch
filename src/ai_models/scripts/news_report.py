import os
import requests
import json
import spacy
import numpy as np
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# Access your NewsAPI key
NEWS_API = os.getenv('NEWS_API')

# Load NLP Model for extracting disaster type and location
nlp = spacy.load("en_core_web_sm")

# Load AI models for summarization and embeddings
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_disaster_context(user_description):
    """
    Extracts disaster type and location from the user description using NLP.
    """
    doc = nlp(user_description)
    
    # Define common disaster keywords
    disaster_keywords = ["fire", "wildfire", "hurricane", "flood", "earthquake", "tornado", "storm"]
    extracted_disaster = None
    extracted_location = None

    # Look for disaster keywords
    for token in doc:
        if token.text.lower() in disaster_keywords:
            extracted_disaster = token.text.lower()
    
    # Use named entity recognition for location information
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:
            extracted_location = ent.text

    return extracted_disaster or "disaster", extracted_location or "USA"

def fetch_disaster_news(user_description):
    """
    Fetch live news articles related to the user's disaster event and location.
    """
    disaster_type, location = extract_disaster_context(user_description)
    print(f"Extracted Disaster: {disaster_type}, Location: {location}")

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": f"{disaster_type} {location}",
        "apiKey": NEWS_API,
        "pageSize": 10,
        "language": "en",
        "sortBy": "publishedAt"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Error retrieving news:", response.text)
        return []

    articles = response.json().get("articles", [])
    
    # Filter out articles without a useful description
    filtered_articles = [
        {"title": a["title"], "description": a["description"], "url": a["url"]}
        for a in articles
        if a["description"]
    ]
    return filtered_articles

def get_summarized_news(user_description):
    """
    Fetch disaster-related news, rank articles by similarity to the user's description,
    and return a summarized key takeaway along with top articles.
    """
    disaster_type, location = extract_disaster_context(user_description)
    articles = fetch_disaster_news(user_description)
    
    if not articles:
        return {"disaster_type": disaster_type, 
                "summary": "No relevant news found for this event.", 
                "articles": []}
    
    # Compute embedding for the user description
    user_embedding = embedding_model.encode([user_description])[0]
    
    # Get embeddings for all article descriptions
    article_texts = [a["description"] for a in articles]
    article_embeddings = embedding_model.encode(article_texts)
    
    # Compute cosine similarity between user description and each article description
    similarities = np.dot(article_embeddings, user_embedding) / (
        np.linalg.norm(article_embeddings, axis=1) * np.linalg.norm(user_embedding) + 1e-10)
    
    # Rank articles based on similarity and select the top 5
    top_indices = np.argsort(similarities)[::-1][:5]
    top_articles = [articles[i] for i in top_indices]
    
    # Combine the descriptions from the top articles for summarization
    combined_text = " ".join([a["description"] for a in top_articles])
    summary_output = summarizer(combined_text, max_length=150, min_length=50, do_sample=False)
    summary = summary_output[0]["summary_text"]
    
    return {
        "disaster_type": disaster_type,
        "summary": summary,
        "articles": top_articles
    }

if __name__ == "__main__":
    user_description = "My house was flooded during the heavy rains, and I need urgent help."
    summarized_news = get_summarized_news(user_description)
    print(json.dumps(summarized_news, indent=2))
