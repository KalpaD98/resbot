import pandas as pd
import json

# Load data from a JSON file
with open('cross-validation-results/config-with-bart-zero-shot/intent_errors.json', 'r') as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.json_normalize(data)
df['intent_prediction'] = df['intent_prediction.name']
df['confidence'] = df['intent_prediction.confidence']
df = df[['text', 'intent', 'intent_prediction', 'confidence']]

# Sort the DataFrame by confidence
df = df.sort_values('confidence', ascending=False)

# Save the DataFrame to a csv file
df.to_csv('output_sorted_without_bart.csv', index=False)
