import random
import torch
from torch.utils.data import Dataset, DataLoader, random_split
from transformers import BertTokenizerFast, BertForSequenceClassification, Trainer, TrainingArguments
from intent_classifier_data import (
    shelter_examples,
    food_examples,
    medical_assistance_examples,
    transportation_examples,
    financial_assistance_examples,
    supplies_examples
)

# Define label mappings
label_map = {
    "shelter": 0,
    "food": 1,
    "medical": 2,
    "transportation": 3,
    "financial": 4,
    "supplies": 5,
}

data = []

# Append examples from each category with the appropriate label.
for example in shelter_examples:
    data.append((example, label_map["shelter"]))

for example in food_examples:
    data.append((example, label_map["food"]))

for example in medical_assistance_examples:
    data.append((example, label_map["medical"]))

for example in transportation_examples:
    data.append((example, label_map["transportation"]))

for example in financial_assistance_examples:
    data.append((example, label_map["financial"]))

for example in supplies_examples:
    data.append((example, label_map["supplies"]))

# Shuffle the data
random.shuffle(data)

# Optionally, split the data into training and validation sets.
train_size = int(0.8 * len(data))
val_size = len(data) - train_size
train_data = data[:train_size]
val_data = data[train_size:]

# Create a custom Dataset class.
class IntentDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=128):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        text, label = self.data[idx]
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors="pt"
        )
        # Remove the batch dimension
        item = {key: val.squeeze(0) for key, val in encoding.items()}
        item["labels"] = torch.tensor(label)
        return item

# Initialize the tokenizer and model.
tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=6)

# Create Dataset objects.
train_dataset = IntentDataset(train_data, tokenizer)
val_dataset = IntentDataset(val_data, tokenizer)

# Define training arguments.
training_args = TrainingArguments(
    output_dir='./intent_model_results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    eval_strategy="steps",
    eval_steps=50,
    save_steps=100,
    warmup_steps=50,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
)

# Define a compute_metrics function (optional).
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    accuracy = accuracy_score(labels, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average="weighted")
    return {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1}

# Initialize the Trainer.
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics,
)

# Train the model.
trainer.train()

# Save the final model and tokenizer.
model.save_pretrained("./intent_model")
tokenizer.save_pretrained("./intent_model")