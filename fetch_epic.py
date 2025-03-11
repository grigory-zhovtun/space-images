"""Module for downloading NASA EPIC images."""
import argparse
import os
import requests
from dotenv import load_dotenv
from utils import download_image
from datetime import datetime


def fetch_epic(api_key: str):
    """Fetch NASA EPIC images.

    Args:
        api_key (str): Valid NASA API key.
    Returns:
        json: NASA EPIC JSON data.
    """
    epic_url = "https://api.nasa.gov/EPIC/api/natural"
    payload = {"api_key": api_key}
    response = requests.get(epic_url, params=payload)
    response.raise_for_status()
    return response.json()



def download_epic(data: list, images_path):
    """Download NASA EPIC images.

    Args:
        data (list): List of NASA EPIC data.
    """
    for item in data:
        image_name = item["image"]
        date_str = datetime.fromisoformat(item["date"].split()[0])
        year, month, day = date_str.year, date_str.month, date_str.day
        image_url = (
            f"https://epic.gsfc.nasa.gov/archive/natural/"
            f"{year}/{month}/{day}/jpg/{image_name}.jpg"
        )
        download_image(image_url, images_path)


def main():
    """Download NASA EPIC images."""
    load_dotenv()

    api_key = os.environ.get("NASA_API_KEY")
    if not api_key:
        raise ValueError("NASA_API_KEY must be provided in the environment variables.")

    parser = argparse.ArgumentParser(description="Download NASA EPIC images.")
    parser.add_argument(
        "--images-path",
        type=str,
        default=os.getenv("NASA_EPIC_IMAGES_PATH", "images/nasa_epic"),
        help="Path to save downloaded images)"
    )
    args = parser.parse_args()

    json_epic_data = fetch_epic(api_key)
    download_epic(json_epic_data, images_path=args.images_path)


if __name__ == "__main__":
    main()