import requests
from transformers import pipeline
from context_extractor import extract_context

from dotenv import load_dotenv
import os

load_dotenv()

# Access your NewsAPI key
NEWS_API = os.getenv('NEWS_API')

# def get_live_news(context, page_size=5):
#     """
#     Retrieve live news articles for the given context using NewsAPI.org.
#     """
#     url = "https://newsapi.org/v2/top-headlines"
#     params = {
#         "q": context,   # use the extracted context as the query term
#         "apiKey": NEWS_API,
#         "pageSize": page_size,
#         "language": "en"
#     }
    
#     response = requests.get(url, params=params)
#     if response.status_code != 200:
#         print("Error retrieving news:", response.text)
#         return ""
    
#     data = response.json()
#     articles = data.get("articles", [])
    
#     news_context = ""
#     for article in articles:
#         title = article.get("title", "")
#         description = article.get("description", "")
#         news_context += f"Title: {title}\nDescription: {description}\n\n"
    
#     return news_context

# def generate_situation_report(location, user_description):
#     """
#     Generate a personalized situation report using live news data and the extracted context.
#     """
#     # Step 1: Extract context based on the user description and location.
#     context = extract_context(user_description, location)
#     print(f"Extracted Context: {context}")
    
#     # Step 2: Retrieve live news using the extracted context.
#     news_context = get_live_news(context)
    
#     # Step 3: Build the prompt for the generative model.
#     prompt = (
#         f"Location: {location}\n"
#         f"Context: {context}\n\n"
#         "Live News Data:\n"
#         f"{news_context}\n"
#         "Based on the above live news data, generate a concise summary of the key events related to the incident. "
#         "Include the current situation, any key updates, and relevant details on the impact of the event. "
#         "Your summary should be informative and provide a clear picture of what is happening.\n\n"
#         "Situation Report:"
#     )

#     # Step 4: Use a text-generation model to produce the report.
#     generator = pipeline("text-generation", model="gpt2", max_length=300)
#     generated = generator(prompt, num_return_sequences=1)
#     report = generated[0]['generated_text']
#     return report

# # Example usage:
# if __name__ == "__main__":
#     # Example parameters (simulate different incidents)
#     location_california = "California"
#     description_fire = "I lost my house in a wildfire. The fire is raging and my community is in chaos."
    
#     # Generate situation reports for both scenarios.
#     print("=== California Wildfire Report ===")
#     report_ca = generate_situation_report(location_california, description_fire)
#     print(report_ca)
import requests
import numpy as np
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import json
import os
import spacy

# Load NLP Model for extracting disaster type and location
nlp = spacy.load("en_core_web_sm")

# Load AI models
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load API key from environment variable
def extract_disaster_context(user_description):
    """
    Extracts disaster type and location from user description using NLP.
    """
    doc = nlp(user_description)
    
    # Common disaster keywords
    disaster_keywords = ["fire", "wildfire", "hurricane", "flood", "earthquake", "tornado", "storm"]
    extracted_disaster = None
    extracted_location = None

    for token in doc:
        if token.text.lower() in disaster_keywords:
            extracted_disaster = token.text.lower()

    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:
            extracted_location = ent.text

    return extracted_disaster or "disaster", extracted_location or "USA"

def fetch_disaster_news(user_description):
    """
    Fetch live news articles related to the user's specific disaster event and location.
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
    
    # Filter out articles that do not contain useful descriptions
    filtered_articles = [
        {"title": a["title"], "description": a["description"], "url": a["url"]}
        for a in articles
        if a["description"]
    ]
    return filtered_articles

def cluster_news(articles, num_clusters=3):
    """
    Cluster news articles based on their descriptions.
    """
    if not articles:
        return []

    descriptions = [a["description"] for a in articles if a["description"]]
    embeddings = embedding_model.encode(descriptions)

    # Apply KMeans clustering
    num_clusters = min(num_clusters, len(articles))  # Avoid errors if there are fewer articles than clusters
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(embeddings)

    clustered_articles = {i: [] for i in range(num_clusters)}
    for i, cluster_id in enumerate(clusters):
        clustered_articles[cluster_id].append(articles[i])

    return clustered_articles

def summarize_cluster(articles):
    """
    Generate a summary for a cluster of related news articles.
    """
    if not articles:
        return ""

    # Combine descriptions into one text
    combined_text = " ".join([a["description"] for a in articles if a["description"]])

    # Summarize using BART
    summary = summarizer(combined_text, max_length=100, min_length=30, do_sample=False)
    return summary[0]["summary_text"]

def get_summarized_news(user_description):
    """
    Fetch disaster-related news, cluster it, and return summarized key takeaways.
    """
    articles = fetch_disaster_news(user_description)
    
    if not articles:
        return [{"summary": "No relevant news found for this event.", "articles": []}]
    
    clustered_articles = cluster_news(articles)

    summarized_news = []
    for cluster_id, cluster_articles in clustered_articles.items():
        summary = summarize_cluster(cluster_articles)
        summarized_news.append({
            "cluster_id": cluster_id,
            "summary": summary,
            "articles": cluster_articles
        })

    return summarized_news

if __name__ == "__main__":
    user_description = "My house was burned down in the California wildfires, and I need help."
    summarized_news = get_summarized_news(user_description)
    print(json.dumps(summarized_news, indent=2))
