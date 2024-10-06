import json, os, glob
from ebooklib import epub

# Function to create an EPUB file from JSON data
def create_epub_from_json(json_file, output_epub_file):
    # Load JSON data from the specified file
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create an EPUB book
    book = epub.EpubBook()

    # Set metadata for the EPUB book
    title = json_file.rsplit('.', 1)[0]
    book.set_title(title)
    book.set_language('en')

    # Add chapters for each episode in the JSON data
    for episode_title, content in data.items():
        # Create a new chapter for each episode
        chapter = epub.EpubHtml(title=episode_title, file_name=f"{episode_title}.xhtml")
        # Prepare content for the chapter
        h1 = content.get('h1', episode_title)
        paragraphs = content.get('paragraphs', [])
        
        # Create the HTML content for the chapter
        chapter_content = f"<h1>{h1}</h1>"
        for paragraph in paragraphs:
            chapter_content += f"<p>{paragraph}</p>"
        
        chapter.set_content(chapter_content)

        # Add chapter to the book
        book.add_item(chapter)

        # # Add chapter to the spine (the reading order)
        # book.add_item(epub.EpubNav())

    # Define the spine (reading order)
    book.spine = ['nav'] + list(book.get_items_of_type(epub.EpubHtml))

    # Add a navigation file to the book
    book.add_item(epub.EpubNav())

    # Write the EPUB file to disk
    epub.write_epub(output_epub_file, book)

# # Example usage
# json_file = 'scraped_data.json'  # Input JSON file
# output_epub_file = 'episodes_collection.epub'  # Output EPUB file
# create_epub_from_json(json_file, output_epub_file)

# print(f"EPUB file '{output_epub_file}' created successfully!")


# Directory containing the script (and the .json files)
current_directory = os.path.dirname(os.path.abspath(__file__))

# Use glob to find all .json files in the current directory
json_files = glob.glob(os.path.join(current_directory, '*.json'))

# Iterate over all JSON files and calculate word counts
for json_file in json_files:
    name_without_extension = json_file.rsplit('.', 1)[0]
    output_epub_file = name_without_extension + '.epub'
    create_epub_from_json(json_file, output_epub_file)

    print(f"EPUB file '{output_epub_file}' created successfully!")