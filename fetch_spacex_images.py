"""Module for downloading SpaceX launch images."""
import argparse
import requests
import sys
from utils import download_image


def fetch_spacex_images(launch_id=None):
    """Fetch and download SpaceX launch images.

    Args:
        launch_id (str): ID of the SpaceX launch.
                         If not provided, fetches the latest launch.
    """
    images_path = "images/spacex"
    if launch_id:
        url = (
            f"https://api.spacexdata.com/v5/launches/{launch_id}"
        )
    else:
        url = "https://api.spacexdata.com/v5/launches/latest"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
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
        help="ID of the SpaceX launch (if omitted, downloads latest launch img)",
    )
    args = parser.parse_args()
    try:
        fetch_spacex_images(args.id)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()