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
    :return: A dictionary of URLs where the search term was found, along with a snippet of the context.
    """
    found_results = {}
    
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()

                # Search for the username or full name using regex
                matches = re.findall(rf'.{{0,50}}{re.escape(search_term)}.{{0,50}}', text, re.IGNORECASE)
                
                if matches:
                    found_results[url] = matches
            else:
                print(f"Failed to access {url}: {response.status_code}")
        except Exception as e:
            print(f"Error while accessing {url}: {e}")
    
    return found_results

def print_results(results):
    if results:
        print(f"Found {len(results)} result(s):")
        for url, matches in results.items():
            print(f"In URL: {url}")
            for match in matches:
                print(f"Snippet: {match.strip()}")
    else:
        print("No matches Data leaks found.")

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
        results = search_public_leaks(search_term, urls)
        print_results(results)
    else:
        print("No URLs to search.")
