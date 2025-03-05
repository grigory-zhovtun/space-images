import argparse
import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from utils import download_image


def fetch_nasa_apod(count=30, date=None):
    load_dotenv()
    api_key = os.environ.get('NASA_API_KEY')
    if not api_key:
        raise ValueError("NASA_API_KEY not found in environment variables.")
    apod_url = 'https://api.nasa.gov/planetary/apod'
    payload = {
        "api_key": api_key,
    }
    if date:
        payload["date"] = date
    else:
        payload["count"] = count

    response = requests.get(apod_url, params=payload)
    response.raise_for_status()
    data = response.json()
    images_path = 'images/nasa_apod'

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
    parser = argparse.ArgumentParser(description="Download NASA Astronomy Picture of the Day images.")
    parser.add_argument("--count", type=int, default=30, help="Number of images to fetch (default: 30)")
    parser.add_argument("--date", type=str, help="Fetch APOD for a specific date (YYYY-MM-DD)")
    args = parser.parse_args()
    try:
        fetch_nasa_apod(count=args.count, date=args.date)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == '__main__':
    main()