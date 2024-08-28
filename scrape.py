import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry  # Updated import for urllib3
from bs4 import BeautifulSoup
import time
import random

# Function to create a requests session with retries
def create_session():
    session = requests.Session()
    retry = Retry(
        total=5,  # Total number of retries
        backoff_factor=1,  # Exponential backoff factor (wait time between retries)
        status_forcelist=[429, 500, 502, 503, 504],  # HTTP statuses to retry on
        allowed_methods=["HEAD", "GET", "OPTIONS"]  # Updated argument name
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# List of URLs to scrape
urls = [
    "https://www.dotabuff.com/heroes/abaddon",
    # Add more URLs as needed
]

def scrape_hero_data(session, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the "Best Versus" section
        best_versus_section = soup.find('section', string=lambda x: x and "Best Versus" in x)
        if best_versus_section:
            best_versus_text = best_versus_section.get_text(strip=True, separator="\n")
        else:
            best_versus_text = "No 'Best Versus' section found."

        # Extract the "Worst Versus" section
        worst_versus_section = soup.find('section', string=lambda x: x and "Worst Versus" in x)
        if worst_versus_section:
            worst_versus_text = worst_versus_section.get_text(strip=True, separator="\n")
        else:
            worst_versus_text = "No 'Worst Versus' section found."

        return {
            'url': url,
            'best_versus': best_versus_text,
            'worst_versus': worst_versus_text
        }
    except requests.exceptions.SSLError as e:
        print(f"SSL error occurred while retrieving {url}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving {url}: {e}")
        return None

# Main loop to scrape all URLs
all_hero_data = []
session = create_session()

for url in urls:
    hero_data = scrape_hero_data(session, url)
    if hero_data:
        all_hero_data.append(hero_data)
    sleep_time = random.uniform(5, 10)  # Random sleep between 5 to 10 seconds
    print(f"Sleeping for {sleep_time:.2f} seconds...")
    time.sleep(sleep_time)  # Randomized delay to avoid rate limiting

# Store the results in a text file
with open('hero_data.txt', 'w') as f:
    for data in all_hero_data:
        f.write(f"URL: {data['url']}\n")
        f.write(f"Best Versus:\n{data['best_versus']}\n\n")
        f.write(f"Worst Versus:\n{data['worst_versus']}\n\n")
        f.write("="*80 + "\n\n")

print("Data has been written to 'hero_data.txt'")
