import requests
from bs4 import BeautifulSoup
import re

# The base URL for the main page with links
base_url = 'https://elpidio.org/the-english-revolution/'

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

    # Now you have all the scraped data in the `all_scraped_data` dictionary
    print("Finished scraping all pages.")

else:
    print(f"Failed to retrieve the main webpage. Status code: {response.status_code}")

# Example of accessing the data
for page_title, content in all_scraped_data.items():
    print(f"\nTitle: {page_title}")
    print("H1:", content['h1'])
    print("Paragraphs:", content['paragraphs'][:2], "...")  # Print only the first 2 paragraphs for brevity
