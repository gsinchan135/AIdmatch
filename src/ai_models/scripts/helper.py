from math import radians, sin, cos, sqrt, atan2
import numpy as np
import re

# Define keywords for each donation category to help boost matches.
category_keywords = {
    "food and water": ["food", "water", "drink", "meal", "grocery"],
    "housing": ["shelter", "house", "home", "accommodation"],
    "medical": ["medical", "hospital", "doctor", "medicine", "health", "clinic", "supplies"],
    # Add additional categories/keywords as needed.
}

def compute_composite_text(donor):
    """
    Combine the donor's structured and unstructured fields into a single string.
    This composite text will be used to compute the donor's embedding.
    """
    composite_text = (
        f"Category: {donor.get('donation_category', '')}. "
        f"Type: {donor.get('donor_type', '')}. "
        f"Offer: {donor.get('description', '')}. "
        f"Capacity: {donor.get('capacity', '')}."
    )
    return composite_text

def category_match_bonus(victim_text, donation_category):
    """
    Check if keywords associated with the donor's donation_category are present in the victim's text.
    Return a bonus score (e.g., +0.05 for each keyword found).
    """
    bonus = 0.0
    keywords = category_keywords.get(donation_category.lower(), [])
    for kw in keywords:
        if kw.lower() in victim_text.lower():
            bonus += 0.05
    return bonus

def extract_number_from_text(text):
    """
    Extract the first number found in the text.
    This could represent the number of people in need.
    """
    match = re.search(r'\b(\d+)\b', text)
    if match:
        return int(match.group(1))
    return None

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on Earth using the Haversine formula.
    Returns distance in kilometers.
    """
    R = 6371  # Earth's radius in kilometers

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    
    return distance