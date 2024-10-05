import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urlparse

# Function to convert the URL path to a title
def url_to_title(url):
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Extract the path (everything after ".org/")
    path = parsed_url.path.strip('/')  # Remove leading and trailing slashes
    
    # Replace hyphens with spaces and capitalize each word
    title = path.replace('-', ' ').title()
    
    return title

# Function to extract the h1 and p tags from a given URL
def scrape_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        page_content = {}

        # Extract the h1 tag
        h1_tag = soup.find('h1')
        page_content['h1'] = h1_tag.get_text() if h1_tag else None

        # Extract all p tags and store them in a list
        page_content['paragraphs'] = [p.get_text() for p in soup.find_all('p')]

        return page_content
    else:
        print(f"Failed to retrieve the webpage at {url}. Status code: {response.status_code}")
        return None

def create_json_for(season, base_url):
    # Send an HTTP request to the base URL
    response = requests.get(base_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all <a> tags that contain links starting with a number
        numbered_links = soup.find_all('a', string=re.compile(r'^\d+\.\d+'))

        # Dictionary to store all the scraped data
        all_scraped_data = {}

        # Iterate over each numbered link, extract the href, and scrape the page
        for link in numbered_links:
            page_title = link.get_text().strip()  # e.g., "1.01 – The Kingdoms of Charles Stuart"
            page_url = link.get('href')

            # Ensure the URL is complete
            if not page_url.startswith('http'):
                page_url = requests.compat.urljoin(base_url, page_url)

            # Scrape the page
            print(f"Scraping: {page_title} -> {page_url}")
            page_data = scrape_page(page_url)

            if page_data:
                # Store the scraped data with the title as the key
                all_scraped_data[page_title] = page_data

        # Write the scraped data to a JSON file
        with open(season + ": " + url_to_title(base_url) + '.json', 'w', encoding='utf-8') as f:
            json.dump(all_scraped_data, f, ensure_ascii=False, indent=4)

        # Now you have all the scraped data in the `all_scraped_data` dictionary
        print("Finished scraping all pages.")

    else:
        print(f"Failed to retrieve the main webpage. Status code: {response.status_code}")

# The base URL for the main page with links
urls = [
    ("Season 1", 'https://elpidio.org/the-english-revolution/'),
    ("Season 2", 'https://elpidio.org/the-american-revolution/'),
    ("Season 3", 'https://elpidio.org/the-french-revolution/'),
    ("Season 4", 'https://elpidio.org/the-haitian-revolution/'),
    ("Season 5", 'https://elpidio.org/the-latin-american-revolutions/'),
    ("Season 6", 'https://elpidio.org/the-july-revolution/')
] # Note: missing seasons 7 (revolutions of 1848), 8 (paris commune), 9 (mexican revolution), 10 (russian revolution part 1), and 11 (russian revolution part 2)

for season, url in urls:
    create_json_for(season, url)

# # Example of accessing the data
# for page_title, content in all_scraped_data.items():
#     print(f"\nTitle: {page_title}")
#     print("H1:", content['h1'])
#     print("Paragraphs:", content['paragraphs'][:2], "...")  # Print only the first 2 paragraphs for brevity
