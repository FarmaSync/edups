import json
import csv

# Input JSON file
json_filename = "input.json"
csv_filename = "output.csv"

# Read JSON data from file
with open(json_filename, "r", encoding="utf-8") as json_file:
    json_data = json.load(json_file)

# Extract field names from JSON keys
if json_data:
    field_names = json_data[0].keys()
else:
    raise ValueError("JSON file is empty or not properly formatted")

# Write to CSV
with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(json_data)

print(f"CSV file '{csv_filename}' has been created successfully.")
