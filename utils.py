import os
from pathlib import Path
from urllib.parse import urlparse
import requests
from random import shuffle


def get_filename_from_url(image_url):
    """Return file name with extension

    Args:
        image_url (str): image url

    Returns:
        str: file name
    """
    return os.path.basename(urlparse(image_url).path)


def get_file_extension(image_url):
    """Return file extension

    Examples:
        >>> get_file_extension('https://example.com/path/to/file.jpg')
        '.jpg'

    Args:
        image_url (str): image url

    Returns:
        str: file extension
    """
    filename = get_filename_from_url(image_url)
    _, extension = os.path.splitext(filename)
    return extension


def download_image(image_url, path_to_save):
    """Function to download an image from url and save it to path_to_save

    Args:
        image_url (string): URL to download image from
        path_to_save (string): Path to save image
    """
    Path(path_to_save).mkdir(parents=True, exist_ok=True)
    print('Downloading image:', image_url)
    response = requests.get(image_url)
    response.raise_for_status()
    filename = get_filename_from_url(image_url)
    filepath = Path(path_to_save) / filename
    with open(filepath, 'wb') as file:
        file.write(response.content)


def get_shuffled_image_paths():
    """
    Recursively traverses the 'images' directory and returns a list of image file paths
    shuffled in random order.

    Returns:
        list[str]: A list of full paths to images.
    """
    images_directory = Path('images')

    files_list = []
    for root, _, files in os.walk(images_directory):
        for file in files:
            files_list.append(os.path.join(root, file))
    shuffle(files_list)
    return files_list