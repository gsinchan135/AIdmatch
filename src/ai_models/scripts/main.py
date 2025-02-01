from summarizer import llama_summarize, compute_embedding, score_donor
from helper import extract_number_from_text

def get_top_donors(victim_text, donors, top_x=3):
    """
    Compute the matching score for each donor, generate an AI summary of the donor's offer,
    and return the top donors.
    """
    victim_embedding = compute_embedding(victim_text)
    donor_scores = []
    
    for donor in donors:
        donor_embedding = donor.get('embedding', None)
        score, computed_embedding = score_donor(victim_embedding, victim_text, donor, donor_embedding)
        donor['embedding'] = computed_embedding  # Cache the embedding.
        donor_scores.append((donor, score))
    
    donor_scores.sort(key=lambda x: x[1], reverse=True)
    
    top_donors = []
    for donor, score in donor_scores[:top_x]:
        donor_copy = donor.copy()
        donor_copy['score'] = score
        # Generate an AI summary of the donor's description.
        donor_copy['offer_summary'] = llama_summarize(donor_copy.get('description', ''))
        top_donors.append(donor_copy)
    
    return top_donors

def assign_donors(victim_text, donors, top_x=3):
    """
    Perform instant matching for a victim, return top donors,
    and update donor capacities based on the victim's need.
    
    For this hackathon demo, we assume the victim text includes a number representing
    the number of people in need. If no number is found, we default to 1.
    """
    required_people = extract_number_from_text(victim_text) or 1
    top_donors = get_top_donors(victim_text, donors, top_x=top_x)
    
    # Update donor capacities (in this simple demo, we subtract the required number).
    for donor in top_donors:
        current_capacity = donor.get('capacity', 0)
        if current_capacity >= required_people:
            donor['capacity'] = current_capacity - required_people
        else:
            donor['capacity'] = 0  # Or leave unchanged if you wish to mark it as exhausted.
    return top_donors

if __name__ == "__main__":
    # Example donor entries.
    donors = [
        {
            'id': 1,
            'donor_type': 'government',
            'donation_category': 'food and water',
            'capacity': 5,
            'description': ("Providing food packs and clean water to affected areas. "
                            "We have a large inventory of food supplies, bottled water, and hygiene kits, "
                            "which we are distributing to shelters and community centers across the region. "
                            "Our teams are ready to deploy at a moment's notice.")
        },
        {
            'id': 2,
            'donor_type': 'NGO',
            'donation_category': 'medical',
            'capacity': 2,
            'description': ("Offering comprehensive medical assistance including first aid kits, "
                            "mobile clinics, and on-site medical professionals. Our services are designed "
                            "to provide immediate and long-term support for those injured or in need of medical care.")
        },
        {
            'id': 3,
            'donor_type': 'individual',
            'donation_category': 'housing',
            'capacity': 5,
            'description': ("Can provide temporary shelter for a small family. "
                            "The shelter is a recently renovated structure equipped with basic amenities "
                            "and can accommodate families in distress.")
        },
        {
            'id': 4,
            'donor_type': 'NGO',
            'donation_category': 'food and water',
            'capacity': 20,
            'description': ("Delivering essential food and water supplies including perishable and non-perishable foods. "
                            "We work with local partners to ensure that aid reaches the most vulnerable communities "
                            "promptly.")
        }
    ]
    
    # Example victim description.
    victim_text = ("My family of 4 is stranded with very little food, water, and shelter due to the wildfires. "
                   "We urgently need help as our supplies are nearly depleted and we have no safe place to stay.")
    
    # For an instant match, we use the online greedy assignment.
    top_donors = assign_donors(victim_text, donors, top_x=3)
    
    print("Top matching donors (after assignment):")
    for donor in top_donors:
        print(f"Donor ID: {donor['id']}, Score: {donor['score']:.2f}")
        print(f"Offer Summary: {donor['offer_summary']}")
        print(f"Remaining Capacity: {donor['capacity']}\n")
