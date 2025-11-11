thonimport json
import requests
from extractors.instagram_parser import InstagramParser
from outputs.exporters import Exporter

def run_scraper(post_url, cookies_json, max_depth=5):
    # Initialize scraper components
    scraper = InstagramParser(post_url, cookies_json, max_depth)
    
    # Start scraping comments
    comments_data = scraper.scrape_comments()
    
    # Export results to JSON
    exporter = Exporter()
    exporter.export_to_json(comments_data, 'data/sample_output.json')
    return comments_data

if __name__ == "__main__":
    post_url = input("Enter Instagram Post URL: ")
    cookies_json = input("Enter Instagram cookies JSON: ")
    comments = run_scraper(post_url, cookies_json)
    print(f"Scraped {len(comments)} comments.")