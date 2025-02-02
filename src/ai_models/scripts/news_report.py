import requests
from transformers import pipeline
from context_extractor import extract_context

from dotenv import load_dotenv
import os

load_dotenv()

# Access your NewsAPI key
NEWS_API = os.getenv('NEWS_API')

def get_live_news(context, page_size=5):
    """
    Retrieve live news articles for the given context using NewsAPI.org.
    """
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "q": context,   # use the extracted context as the query term
        "apiKey": NEWS_API,
        "pageSize": page_size,
        "language": "en"
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Error retrieving news:", response.text)
        return ""
    
    data = response.json()
    articles = data.get("articles", [])
    
    news_context = ""
    for article in articles:
        title = article.get("title", "")
        description = article.get("description", "")
        news_context += f"Title: {title}\nDescription: {description}\n\n"
    
    return news_context

def generate_situation_report(location, user_description):
    """
    Generate a personalized situation report using live news data and the extracted context.
    """
    # Step 1: Extract context based on the user description and location.
    context = extract_context(user_description, location)
    print(f"Extracted Context: {context}")
    
    # Step 2: Retrieve live news using the extracted context.
    news_context = get_live_news(context)
    
    # Step 3: Build the prompt for the generative model.
    prompt = (
        f"Location: {location}\n"
        f"Context: {context}\n\n"
        "Live News Data:\n"
        f"{news_context}\n"
        "Based on the above live news data, generate a concise summary of the key events related to the incident. "
        "Include the current situation, any key updates, and relevant details on the impact of the event. "
        "Your summary should be informative and provide a clear picture of what is happening.\n\n"
        "Situation Report:"
    )

    # Step 4: Use a text-generation model to produce the report.
    generator = pipeline("text-generation", model="gpt2", max_length=300)
    generated = generator(prompt, num_return_sequences=1)
    report = generated[0]['generated_text']
    return report

# Example usage:
if __name__ == "__main__":
    # Example parameters (simulate different incidents)
    location_california = "California"
    description_fire = "I lost my house in a wildfire. The fire is raging and my community is in chaos."
    
    # Generate situation reports for both scenarios.
    print("=== California Wildfire Report ===")
    report_ca = generate_situation_report(location_california, description_fire)
    print(report_ca)