import os
from transformers import pipeline

model_path = os.path.join(os.path.dirname(__file__), 'intent_model')

# Load your fine-tuned intent classifier
intent_classifier = pipeline("text-classification", model=model_path)

def predict_intent(text):
    """
    Predict the intent of the text using your fine-tuned classifier.
    
    Returns:
        The predicted intent label (e.g., "LABEL_0", "LABEL_1", or "LABEL_2") which you can map
        to your human-readable intents ("food", "shelter", "medical").
    """
    result = intent_classifier(text)
    label_num = int(result[0]['label'].split('_')[1])  # Extract number from LABEL_X
    # Map numeric labels to intent names (this mapping depends on your training data)
    label_mapping = {
        0: "shelter",
        1: "food",
        2: "medical",
        3: "transportation",
        4: "financial",
        5: "supplies"
    }
    
    return label_mapping.get(label_num,"Other")
