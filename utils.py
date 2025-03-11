"""Utility functions for downloading and processing images."""
import os
from pathlib import Path
from urllib.parse import urlparse
import requests
from random import shuffle


def get_filename_from_url(image_url):
    return os.path.basename(urlparse(image_url).path)


def get_file_extension(image_url):
    filename = get_filename_from_url(image_url)
    _, extension = os.path.splitext(filename)
    return extension


def download_image(image_url, path_to_save):
    """Download an image from URL and save it to the specified path.

    Args:
        image_url (str): URL to download the image from.
        path_to_save (str): Path where the image will be saved.
    """
    Path(path_to_save).mkdir(parents=True, exist_ok=True)
    print("Downloading image:", image_url)
    response = requests.get(image_url)
    response.raise_for_status()
    filename = get_filename_from_url(image_url)
    filepath = Path(path_to_save) / filename
    with open(filepath, "wb") as file:
        file.write(response.content)


def get_shuffled_image_paths(images_directory):
    """Traverse the specified images directory and return a shuffled list of image paths.

    Args:
        images_directory (str or Path): The directory in which to search for images.
            A valid directory must be provided.

    Returns:
        list[str]: A list containing the full paths to the images found in the directory.

    Raises:
        ValueError: If images_directory is None.
    """
    if images_directory is None:
        raise ValueError("images_directory must be provided and cannot be None.")
    images_directory = Path(images_directory)
    file_full_paths = []
    for root, _, files in os.walk(images_directory):
        for file in files:
            file_full_paths.append(os.path.join(root, file))
    shuffle(file_full_paths)
    return file_full_paths