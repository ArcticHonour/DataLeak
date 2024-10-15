import requests
from bs4 import BeautifulSoup
import re
import os

os.system("clear")

def search_public_leaks(search_term, urls):
    """
    Search for a username or full name in public data leaks hosted on websites.
    
    :param search_term: The username or full name to search for.
    :param urls: A list of URLs of public breach data pages.
    :return: A dictionary of URLs where the search term was found, along with the full line of context.
    """
    found_results = {}
    hit_counter = 0  # Counter for hits

    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text_lines = soup.get_text().splitlines()

                # Search for the username or full name in each line
                matches = [line for line in text_lines if re.search(re.escape(search_term), line, re.IGNORECASE)]
                
                # Print the URL and number of lines found
                print(f"\nIn URL: {url}")
                print(f"Lines found: {len(matches)}")
                
                if matches:
                    found_results[url] = matches
                    for match in matches:
                        hit_counter += 1  # Increment hit counter
                        print(f"Hit ({hit_counter}): {match.strip()}")
                else:
                    print("No matches found.")
            else:
                print(f"Failed to access {url}: {response.status_code}")
        except Exception as e:
            print(f"Error while accessing {url}: {e}")
    
    return found_results

def load_urls_from_file(filename):
    """
    Load URLs from a file, with one URL per line.
    
    :param filename: The path to the file containing the URLs.
    :return: A list of URLs.
    """
    urls = []
    try:
        with open(filename, 'r') as file:
            urls = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    return urls

if __name__ == "__main__":
    search_term = input("Enter the username or full name to search for: ")
    
    # Load URLs from data.txt file
    urls = load_urls_from_file('data.txt')
    
    if urls:
        search_public_leaks(search_term, urls)
    else:
        print("No URLs to search.")
