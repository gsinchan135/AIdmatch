from summarizer import llama_summarize, compute_embedding, score_donor_with_location 
from intent_classifier import predict_intent
from helper import extract_number_from_text, calculate_distance

# In main.py
def get_top_donors(victim_text, victim_location, donors, top_x=3, max_distance=50):
    """
    Compute the matching score for each donor, considering location proximity.
    """
    victim_embedding = compute_embedding(victim_text)
    donor_scores = []
    
    for donor in donors:
        donor_embedding = donor.get('embedding', None)
        score, computed_embedding = score_donor_with_location(
            victim_embedding, 
            victim_text, 
            victim_location,
            donor, 
            donor_embedding,
            max_distance
        )
        donor['embedding'] = computed_embedding
        
        # Add distance info to donor data
        if 'location' in donor and victim_location:
            distance = calculate_distance(
                victim_location['latitude'],
                victim_location['longitude'],
                donor['location']['latitude'],
                donor['location']['longitude']
            )
            donor['distance'] = round(distance, 2)
        
        donor_scores.append((donor, score))
    
    # Sort donors by computed score
    donor_scores.sort(key=lambda x: x[1], reverse=True)
    
    top_donors = []
    for donor, score in donor_scores[:top_x]:
        donor_copy = donor.copy()
        donor_copy['score'] = score
        donor_copy['offer_summary'] = llama_summarize(donor_copy.get('description', ''))
        top_donors.append(donor_copy)
    
    return top_donors

def assign_donors(victim_text, victim_location, donors, top_x=3, max_distance=50):
    """
    Perform matching considering geographic location.
    """
    required_people = extract_number_from_text(victim_text) or 1
    predicted_intent = predict_intent(victim_text)
    print(f"Predicted intent: {predicted_intent}")
    
    # Get top donors with location consideration
    top_donors = get_top_donors(victim_text, victim_location, donors, top_x=top_x, max_distance=max_distance)
    
    # Boost scores for intent matching (keeping existing logic)
    for donor in top_donors:
        donation_category = donor.get("donation_category", "").lower()
        if predicted_intent.lower() in donation_category:
            donor["score"] += 0.05
    
    # Re-sort and update capacities
    top_donors.sort(key=lambda d: d["score"], reverse=True)
    for donor in top_donors:
        current_capacity = donor.get('capacity', 0)
        if current_capacity >= required_people:
            donor['capacity'] = current_capacity - required_people
        else:
            donor['capacity'] = 0
    
    return top_donors, predicted_intent

if __name__ == "__main__":
    # Example donor entries.
    donors = [
        {
            'id': 1,
            'donor_type': 'government',
            'donation_category': 'food and water',
            'capacity': 5,
            'location': {'latitude': 40.7128, 'longitude': -74.0060},  
            'description': (
                "Providing food packs and clean water to affected areas. "
                "We have a large inventory of food supplies, bottled water, and hygiene kits, "
                "which we are distributing to shelters and community centers across the region. "
                "Our teams are ready to deploy at a moment's notice."
            )
        },
        {
            'id': 2,
            'donor_type': 'NGO',
            'donation_category': 'medical',
            'capacity': 2,
            'location': {'latitude': 40.7404, 'longitude': -74.4234},  
            'description': (
                "Offering comprehensive medical assistance including first aid kits, "
                "mobile clinics, and on-site medical professionals. Our services are designed "
                "to provide immediate and long-term support for those injured or in need of medical care."
            )
        },
        {
            'id': 3,
            'donor_type': 'individual',
            'donation_category': 'housing',
            'capacity': 5,
            'location': {'latitude': 39.7128, 'longitude': -73.0060},  
            'description': (
                "Can provide temporary shelter for a small family. "
                "The shelter is a recently renovated structure equipped with basic amenities "
                "and can accommodate families in distress."
            )
        },
        {
            'id': 4,
            'donor_type': 'NGO',
            'donation_category': 'food and water',
            'capacity': 20,
            'location': {'latitude': 41.8781, 'longitude': -87.6298},
            'description': (
                "Delivering essential food and water supplies including perishable and non-perishable foods. "
                "We work with local partners to ensure that aid reaches the most vulnerable communities promptly."
            )
        }
    ]
    
    # Example victim description.
    victim_text = (
        "My house got destroyed in a storm and I need a safe place to stay for me and my family"
    )
    victim_location = {
        'latitude': 40.7128,  # Example: NYC coordinates
        'longitude': -74.0060
    }
    
    # Perform matching with intent-based adjustments.
    top_donors, predicted_intent = assign_donors(victim_text, victim_location, donors, top_x=3, max_distance=50)
    
    # Prepare the predictions dictionary for saving.
    predictions = {
        "victim_text": victim_text,
        "predicted_intent": predicted_intent,
        "top_donors": top_donors
    }
    
    # Print results 
    print("Top matching donors (after assignment):")
    for donor in top_donors:
        print(f"Donor ID: {donor['id']}, Score: {donor['score']:.2f}")
        print(f"Distance: {donor.get('distance', 'Unknown')} km")
        print(f"Offer Summary: {donor['offer_summary']}")
        print(f"Remaining Capacity: {donor['capacity']}\n")
