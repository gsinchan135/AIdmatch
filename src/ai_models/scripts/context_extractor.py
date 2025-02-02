# context_extractor.py
import spacy

# Load a lightweight spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_context(user_description, location):
    """
    Extracts crisis-related keywords from the user description and combines them with the location.
    
    If any crisis keywords (e.g., "fire", "hurricane", "flood") are found, they form the context.
    Otherwise, fall back to using named entities extracted from the description.
    """
    crisis_keywords = ["fire", "hurricane", "earthquake", "flood", "tornado", "wildfire", "storm"]
    lower_desc = user_description.lower()
    
    matched_keywords = [kw for kw in crisis_keywords if kw in lower_desc]
    
    if matched_keywords:
        context = f"{location} " + " ".join(matched_keywords)
    else:
        # Use spaCy NER as a fallback
        doc = nlp(user_description)
        entities = [ent.text for ent in doc.ents if ent.label_ in ["EVENT", "GPE", "NORP", "ORG"]]
        if entities:
            context = f"{location} " + " ".join(entities)
        else:
            # If nothing is found, fall back to the full description
            context = f"{location} {user_description}"
    return context
