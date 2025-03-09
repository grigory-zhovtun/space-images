"""Module for downloading SpaceX launch images."""
import argparse
import requests
import sys
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


def download_spacex_image(data):
    """Download a SpaceX image.

    Args:
        data (dict): JSON data returned from the API.
        images_path (str): Path to the images folder.
    """
    images_path = "images/spacex"
    images = data.get("links", {}).get("flickr", {}).get("original", [])
    if not images:
        print("No images found for this launch.")
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
    args = parser.parse_args()
    try:
        json_spacex_data = fetch_spacex_data(args.id)
        download_spacex_image(json_spacex_data)
    except (ValueError, requests.exceptions.RequestException) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()