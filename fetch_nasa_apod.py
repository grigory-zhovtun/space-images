"""Module for downloading NASA Astronomy Picture of the Day images."""
import argparse
import os
import requests
from dotenv import load_dotenv
from utils import download_image
import logging


def fetch_nasa_apod_data(api_key, count=30, date=None):
    """Fetch NASA APOD images.

    Args:
        key (str): API key for NASA APOD
        count (int): Number of images to fetch when date is not specified.
        date (str): Specific date (YYYY-MM-DD) to fetch APOD for.

    Returns:
        json: json object containing NASA APOD data
    """
    if not api_key:
        raise ValueError("NASA_API_KEY not found in environment variables.")
    apod_url = "https://api.nasa.gov/planetary/apod"
    payload = {"api_key": api_key}
    if date:
        payload["date"] = date
    else:
        payload["count"] = count

    response = requests.get(apod_url, params=payload)
    response.raise_for_status()

    return response.json()


def process_apod_item(item, images_path):
    """Processes a single APOD item.

    If the media_type is 'image', it downloads the image.
    Otherwise, it prints a message.

    Args:
        item (dict): APOD item.
        images_path (str): Path to directory where images are stored.
    """
    if item.get("media_type") == "image":
        image_url = item.get("url")
        download_image(image_url, images_path)
    else:
        logging.error("Skipping non-image media type.")


def download_apod_images(data, images_path="images/nasa_apod"):
    """Processes APOD data, which can be either a list of items or a single item.

    Args:
        data (dict): APOD data.
        images_path (str): Path to directory where images are stored.

    """
    if isinstance(data, list):
        for item in data:
            process_apod_item(item, images_path)
    else:
        process_apod_item(data, images_path)


def main():
    """Parse command-line arguments and download NASA APOD images."""
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Download NASA Astronomy Picture of the Day images."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=30,
        help="Number of images to fetch (default: 30)"
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Fetch APOD for a specific date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--images-path",
        type=str,
        default=os.getenv("NASA_APOD_IMAGES_PATH", "images/nasa_apod"),
        help="Path to save downloaded images)"
    )
    args = parser.parse_args()

    nasa_apod = fetch_nasa_apod_data(os.environ.get("NASA_API_KEY"), count=args.count, date=args.date)
    download_apod_images(nasa_apod, images_path=args.images_path)


if __name__ == "__main__":
    main()