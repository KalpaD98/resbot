import json
import csv

# Name of the output CSV file
csv_file_name = "output.csv"

# Number of files to process
no_of_files = 6

# List to store the extracted values
data = []
total_precision = 0
total_recall = 0
total_f1_score = 0

# Loop over the JSON files
for i in range(1, no_of_files+1):
    # Construct the file name
    json_file_name = f"collection-config_/intent_report_{i}.json"

    # Open and read the JSON file
    with open(json_file_name, "r") as json_file:
        json_data = json.load(json_file)

    # Extract the values from the "weighted avg" section
    weighted_avg = json_data["weighted avg"]
    precision = weighted_avg["precision"] * 100  # Multiply by 100 to convert to percentage
    recall = weighted_avg["recall"] * 100  # Multiply by 100 to convert to percentage
    f1_score = weighted_avg["f1-score"] * 100  # Multiply by 100 to convert to percentage

    # Update the total precision, recall, and f1-score
    total_precision += precision
    total_recall += recall
    total_f1_score += f1_score

    # Add the extracted values to the list
    data.append([f"{i}", f"{round(precision, 2)}%", f"{round(recall, 2)}%", f"{round(f1_score, 2)}%"])

# Calculate the average precision, recall, and f1-score
average_precision = total_precision / no_of_files
average_recall = total_recall / no_of_files
average_f1_score = total_f1_score / no_of_files

# Add the average precision, recall, and f1-score to the list
data.append(["average", f"{round(average_precision, 2)}%", f"{round(average_recall, 2)}%", f"{round(average_f1_score, 2)}%"])

# Write the data to the CSV file
with open(csv_file_name, "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Report #", "precision", "recall", "f1-score"])  # Write the header
    writer.writerows(data)  # Write the data
