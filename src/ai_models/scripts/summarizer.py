from dotenv import load_dotenv
import os

from sentence_transformers import SentenceTransformer
from huggingface_hub import InferenceClient

from sklearn.metrics.pairwise import cosine_similarity

from helper import compute_composite_text, category_match_bonus, extract_number_from_text, calculate_distance

load_dotenv()

# Access your API key
HUGGING_FACE_API = os.getenv('HUGGING_FACE_API')

# Load the pre-trained Sentence Transformer model for embeddings.
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize the LLaMA-based summarization client via Hugging Face Inference API.
client = InferenceClient("meta-llama/Meta-Llama-3-8B-Instruct", token=HUGGING_FACE_API)

def compute_embedding(text):
    """
    Given a text string, return its embedding.
    """
    return embedding_model.encode(text)

def score_donor(victim_embedding, victim_text, donor, donor_embedding=None):
    """
    Compute a score for a single donor by combining:
      - Cosine similarity between the victim's embedding and the donor's composite embedding.
      - A bonus if donor's category keywords appear in the victim text.
      - A capacity bonus/penalty based on whether the donor's capacity meets the victim's indicated need.
    
    Returns:
        (total_score, donor_embedding)
    """
    if donor_embedding is None:
        composite_text = compute_composite_text(donor)
        donor_embedding = compute_embedding(composite_text)
    
    # Compute cosine similarity between victim and donor embeddings.
    similarity = cosine_similarity([victim_embedding], [donor_embedding])[0][0]
    
    # Compute bonus from category keyword matching.
    bonus = category_match_bonus(victim_text, donor.get('donation_category', ''))
    
    # Capacity consideration: extract a number from victim text and compare with donor capacity.
    required_people = extract_number_from_text(victim_text)
    capacity = donor.get('capacity', 0)
    capacity_score = 0.0
    if required_people is not None:
        if capacity >= required_people:
            capacity_score = 0.1  # Bonus when capacity meets/exceeds the need.
        else:
            capacity_score = -0.1  # Penalty when capacity is insufficient.
    
    total_score = similarity + bonus + capacity_score
    return total_score, donor_embedding

# Add to helper.py
def score_donor_with_location(victim_embedding, victim_text, victim_location, donor, donor_embedding=None, max_distance=50):
    """
    Score a donor based on embedding similarity, intent matching, and geographic distance.
    max_distance is in kilometers.
    """
    # Get the base similarity score
    base_score, computed_embedding = score_donor(victim_embedding, victim_text, donor, donor_embedding)
    
    # Calculate distance
    try:
        distance = calculate_distance(
            victim_location['latitude'], 
            victim_location['longitude'],
            donor['location']['latitude'], 
            donor['location']['longitude']
        )
        
        # If distance is greater than max_distance, significantly reduce the score
        if distance > max_distance:
            distance_score = 0.1  # Very low score for out-of-range donors
        else:
            # Normalize distance score (closer = higher score)
            distance_score = 1 - (distance / max_distance)
            
        # Combine scores (adjust weights as needed)
        final_score = (base_score * 0.7) + (distance_score * 0.3)
        
    except (KeyError, TypeError):
        # If location data is missing, fall back to base score
        final_score = base_score * 0.5  # Penalize missing location data
        
    return final_score, computed_embedding

def llama_summarize(text, max_new_tokens=50):
    """
    Generate a concise summary using a LLaMA-based model via the Hugging Face Inference API.
    """
    prompt = f"Summarize the following text in a concise manner, do not include any extra text other than the summary:\n\n{text}\n\nSummary:"
    
    result = client.text_generation(prompt, max_new_tokens=max_new_tokens)
    
    if isinstance(result, list) and len(result) > 0:
        summary = result[0].get("generated_text", "").strip()
    else:
        summary = result
    return summary