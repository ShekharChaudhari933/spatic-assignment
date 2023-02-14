# Import necessary modules
import math
import difflib
import csv

# Define function to calculate distance between two latitude/longitude pairs
def calculate_distance(lat1, lon1, lat2, lon2):
    # Define Earth's approximate radius in kilometers
    R = 6373.0

    # Convert latitude and longitude values to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Calculate the differences in latitude and longitude
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Calculate the Haversine formula for distance between two points
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c * 1000

    # Return distance in meters
    return distance

# Define function to check the similarity of two strings
def check_similarity(str1, str2):
    # Use the SequenceMatcher class from the difflib module to calculate the similarity ratio
    ratio = difflib.SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    # Return True if the ratio is greater than 0.8, indicating high similarity
    return ratio > 0.8

# Define function to find similar entries in a list
def find_similar_entries(entries):
    # Create an empty list to store the results
    results = []

    # Loop through all pairs of entries and compare their names and locations
    for i in range(len(entries)):
        for j in range(i+1, len(entries)):
            # Check if the distance between the two entries is less than 200 meters
            if calculate_distance(entries[i]['latitude'], entries[i]['longitude'], entries[j]['latitude'], entries[j]['longitude']) < 200:
                # Check if the names of the two entries are similar
                if list(difflib.ndiff(entries[i]['name'].lower(), entries[j]['name'].lower())).count(' ') < 5:
                    # Add the pair to the results list if they are similar
                    results.append((i, j))

    # Return the list of similar entry pairs
    return results

# Load data from a CSV file
with open('data.csv', 'r') as file:
    # Use DictReader to read the CSV file and create a list of dictionaries
    reader = csv.DictReader(file)
    entries = list(reader)

# Convert latitude and longitude strings to floats
for entry in entries:
    entry['latitude'] = float(entry['latitude'])
    entry['longitude'] = float(entry['longitude'])

# Find similar entries in the list
similar_pairs = find_similar_entries(entries)

# Create a new CSV file with the similarity information
with open('output.csv', 'w', newline='') as file:
    # Define the fieldnames for the output file
    fieldnames = list(entries[0].keys())
    fieldnames.append('is_similar')
    # Use DictWriter to write the output file with the same fieldnames as the input file, plus an extra field for similarity information
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    # Loop through each entry in the list and check if it is similar to any other entry


    for i, entry in enumerate(entries):
        entry['is_similar'] = 0

        for pair in similar_pairs:
            if i in pair:
                entry['is_similar'] = 1

        writer.writerow(entry)
