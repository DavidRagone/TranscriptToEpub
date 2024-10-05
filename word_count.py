import json, glob, os

# Function to calculate word count for each episode
def calculate_word_counts(file_name):
    # Load the JSON data from the file
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Dictionary to store word counts for each episode
    word_counts = {}

    # Iterate over each episode in the JSON data
    for episode_title, content in data.items():
        # Get the paragraphs for the episode
        paragraphs = content.get('paragraphs', [])
        
        # Count the total number of words in all paragraphs
        total_words = sum(len(paragraph.split()) for paragraph in paragraphs)
        
        # Store the word count for the episode
        word_counts[episode_title] = total_words

    return word_counts

# Directory containing the script (and the .json files)
current_directory = os.path.dirname(os.path.abspath(__file__))

# Use glob to find all .json files in the current directory
json_files = glob.glob(os.path.join(current_directory, '*.json'))

# Iterate over all JSON files and calculate word counts
for json_file in json_files:
    # print(f"Processing file: {json_file}")
    
    # Calculate word counts for the current file
    word_counts = calculate_word_counts(json_file)
    
    # Print word counts for each episode in the file and count total words in file
    total_words = 0
    for episode, count in word_counts.items():
        # print(f"{episode}: {count} words")
        total_words += count
    print(f"total words in season {json_file}: {total_words:,}")