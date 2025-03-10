"""Utility functions for downloading and processing images."""
import os
from pathlib import Path
from urllib.parse import urlparse
import requests
from random import shuffle


def get_filename_from_url(image_url):
    """Return file name with extension.

    Args:
        image_url (str): Image URL.

    Returns:
        str: File name.
    """
    return os.path.basename(urlparse(image_url).path)


def get_file_extension(image_url):
    """Return file extension.

    Examples:
        >>> get_file_extension('https://example.com/path/to/file.jpg')
        '.jpg'

    Args:
        image_url (str): Image URL.

    Returns:
        str: File extension.
    """
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


def get_shuffled_image_paths(images_directory=None):
    """Traverse the images directory and return shuffled image paths.

    Args:
        images_directory (str or Path, optional): Directory to search images in.
            Если не задан, используется значение переменной окружения 'IMAGES_DIRECTORY',
            либо по умолчанию 'images'.

    Returns:
        list[str]: A list of full paths to images.
    """
    if images_directory is None:
        images_directory = os.getenv("IMAGES_DIRECTORY", "images")
    images_directory = Path(images_directory)
    files_list = []
    for root, _, files in os.walk(images_directory):
        for file in files:
            files_list.append(os.path.join(root, file))
    shuffle(files_list)
    return files_list