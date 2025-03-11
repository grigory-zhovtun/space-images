"""Module for downloading NASA Astronomy Picture of the Day images."""
import argparse
import os
import requests
from dotenv import load_dotenv
from utils import download_image


def fetch_nasa_apod_data(key, count=30, date=None):
    """Fetch NASA APOD images.

    Args:
        key (str): API key for NASA APOD
        count (int): Number of images to fetch when date is not specified.
        date (str): Specific date (YYYY-MM-DD) to fetch APOD for.

    Returns:
        json: json object containing NASA APOD data
    """
    api_key = key
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


def download_apod_images(data, images_path="images/nasa_apod"):
    """Download images from NASA APOD.

    Args:
        data (dict): NASA APOD data
    """
    if isinstance(data, list):
        for item in data:
            if item.get("media_type") == "image":
                image_url = item.get("url")
                download_image(image_url, images_path)
            else:
                print("Skipping non-image media type.")
    else:
        if data.get("media_type") == "image":
            download_image(data.get("url"), images_path)
        else:
            print("APOD is not an image.")
    print("Done!")


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
    try:
        json_nasa_apod = fetch_nasa_apod_data(os.environ.get("NASA_API_KEY"), count=args.count, date=args.date)
        download_apod_images(json_nasa_apod, images_path=args.images_path)
    except (ValueError, requests.exceptions.RequestException) as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()