import json
import csv

# Load the JSON data
with open('ablation-enh-with-and-without-zero-shot-5-runs/results.json') as f:
    data = json.load(f)

# Prepare the CSV data
csv_data = [['Configuration', '0% exc', '20% exc', '40% exc', '60% exc', '80% exc']]

# Temporary list to hold the configurations and their averages
temp_data = []

for config_name, values in data.items():
    # Calculate the average for each exclusion case and append a '%' sign
    averages = [str(round(sum(x[i] for x in values) / len(values) * 100, 2)) + '%' for i in range(5)]
    temp_data.append([config_name] + averages)

# Sort the configurations by the 0% exclusion case in descending order
sorted_data = sorted(temp_data, key=lambda x: float(x[1].strip('%')), reverse=True)

# Append the sorted data to the CSV data
csv_data.extend(sorted_data)

# Write the CSV data
with open('output_ablation_enh.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(csv_data)
