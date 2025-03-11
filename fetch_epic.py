"""Module for downloading NASA EPIC images."""
import argparse
import os
import requests
from dotenv import load_dotenv
from utils import download_image
from datetime import datetime


def fetch_epic(key):
    """Fetch NASA EPIC images.

    Args:
        key (str): NASA EPIC image key.
    Returns:
        json: NASA EPIC json data.
    """
    api_key = key
    if not api_key:
        raise ValueError("NASA_API_KEY not found in environment variables.")
    epic_url = "https://api.nasa.gov/EPIC/api/natural"
    payload = {"api_key": api_key}
    response = requests.get(epic_url, params=payload)
    response.raise_for_status()
    return response.json()


def download_epic(data):
    """Download NASA EPIC images."""
    if not isinstance(data, list):
        print("Expected list of EPIC data, but got different format.")
        return
    images_path = "images/nasa_epic"
    for item in data:
        image_name = item["image"]
        date_str = datetime.fromisoformat(item["date"].split()[0])  # Format: 'YYYY-MM-DD'
        year, month, day = date_str.year, date_str.month, date_str.day
        image_url = (
            f"https://epic.gsfc.nasa.gov/archive/natural/"
            f"{year}/{month}/{day}/jpg/{image_name}.jpg"
        )
        download_image(image_url, images_path)
    print("Done!")


def main():
    """Download NASA EPIC images."""
    load_dotenv()
    parser = argparse.ArgumentParser(description="Download NASA EPIC images.")
    parser.parse_args()  # No arguments needed
    try:
        json_epic_data = fetch_epic(os.environ.get("NASA_API_KEY"))
        download_epic(json_epic_data)
    except (ValueError, requests.exceptions.RequestException) as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()