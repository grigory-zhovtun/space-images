"""Module for downloading SpaceX launch images."""
import argparse
import requests
import logging
import os
from utils import download_image


def fetch_spacex_data(launch_id):
    """Fetch and download SpaceX launch images.

    Args:
        launch_id (str): ID of the SpaceX launch.
    """
    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def download_spacex_image(data, images_path):
    """Download a SpaceX image.

    Args:
        data (dict): JSON data returned from the API.
        images_path (str): Path to the images folder.
    """
    images = data.get("links", {}).get("flickr", {}).get("original", [])
    if not images:
        logging.warning("No images found for this launch.")
        return
    for image in images:
        download_image(image, images_path)
    print("Done!")


def main():
    """Parse command-line arguments and download SpaceX launch images."""
    parser = argparse.ArgumentParser(description="Download SpaceX launch img.")
    parser.add_argument(
        "--id",
        type=str,
        default="latest",
        help="ID of the SpaceX launch (default: latest launch img)",
    )
    parser.add_argument(
        "--images-path",
        type=str,
        default=os.getenv("NASA_SPACEX_IMAGES_PATH", "images/spacex"),
        help="Path to save downloaded images)"
    )

    args = parser.parse_args()

    spacex_data = fetch_spacex_data(args.id)
    download_spacex_image(spacex_data, images_path=args.images_path)


if __name__ == "__main__":
    main()