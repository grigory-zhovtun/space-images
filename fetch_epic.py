import argparse
import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from utils import download_image

def fetch_epic():
    load_dotenv()
    api_key = os.environ.get('NASA_API_KEY')
    if not api_key:
        raise ValueError("NASA_API_KEY not found in environment variables.")
    epic_url = 'https://api.nasa.gov/EPIC/api/natural'
    payload = {
        "api_key": api_key,
    }
    response = requests.get(epic_url, params=payload)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, list):
        print("Expected list of EPIC data, but got different format.")
        return
    images_path = 'images/nasa_epic'
    for item in data:
        image_name = item["image"]
        date_str = item["date"].split()[0]  # Формат: 'YYYY-MM-DD'
        year, month, day = date_str.split("-")
        image_url = (
            f"https://epic.gsfc.nasa.gov/archive/natural/"
            f"{year}/{month}/{day}/jpg/{image_name}.jpg"
        )
        download_image(image_url, images_path)
    print("Done!")

def main():
    parser = argparse.ArgumentParser(description="Download NASA EPIC images.")
    args = parser.parse_args()
    try:
        fetch_epic()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == '__main__':
    main()