import requests
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv
import os


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

    print('Downloading image: ', image_url)
    response = requests.get(image_url)
    response.raise_for_status()

    filename = get_filename_from_url(image_url)

    filepath = Path(path_to_save) / filename

    # filename = urlparse(image_url).path.split("/")[-1]
    with open(filepath, 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch():
    images_path = 'images/spacex'
    payload = {
        'id': '5eb87d47ffd86e000604b38a'
    }
    spacex_api = 'https://api.spacexdata.com/v5/launches/'
    resp = requests.get(spacex_api, params=payload)
    resp.raise_for_status()
    data = resp.json()

    for item in data:
        images = item.get("links", {}).get("flickr", {}).get("original", [])
        if len(images) == 0:
            continue
        for image in images:
            download_image(image, images_path)

    print('done!')


def fetch_nasa_picture_of_the_day():
    load_dotenv()
    api_key = os.environ['NASA_API_KEY']

    apod_url = 'https://api.nasa.gov/planetary/apod'

    payload = {
        "api_key": api_key,
        "count": 30,
        # "date": "2020-08-01",
    }

    try:
        response = requests.get(apod_url, params=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("HTTP error occurred:", err)
        return
    except requests.exceptions.RequestException as err:
        print("Request error occurred:", err)
        return

    data = response.json()

    if isinstance(data, list):
        for item in data:
            if item.get("media_type") == "image":
                image_url = item.get("url")
                download_image(image_url, "images/nasa_apod")
            else:
                print("Пропускаем элемент: media_type не 'image'.")
    else:
        # Теоретически, если API вернёт не список (напр., 1 объект),
        # можно обработать и этот случай
        print("API вернуло не список, проверяем media_type как у одиночного объекта.")
        if data.get("media_type") == "image":
            image_url = data.get("url")
            download_image(image_url, "images/nasa_apod")
        else:
            print("Сегодня APOD не является изображением!")


def fetch_epic():
    load_dotenv()
    api_key = os.environ['NASA_API_KEY']

    epic_url = 'https://api.nasa.gov/EPIC/api/natural'

    payload = {
        "api_key": api_key,
    }

    try:
        response = requests.get(epic_url, params=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("HTTP error occurred:", err)
        return
    except requests.exceptions.RequestException as err:
        print("Request error occurred:", err)
        return

    data = response.json()

    if not isinstance(data, list):
        print("Ожидался список с данными EPIC, но пришло что-то другое.")
        return

    for item in data:
        # item имеет поля "image", "date", "caption" и т.д.
        image_name = item["image"]  # Например: 'epic_1b_20210220003454'
        date_str = item["date"].split()[0]  # 'YYYY-MM-DD HH:MM:SS' -> 'YYYY-MM-DD'
        year, month, day = date_str.split("-")

        # Формируем URL для скачивания
        # Для enhanced: /archive/enhanced/YYYY/MM/DD/png/{image_name}.png
        image_url = (
            f"https://epic.gsfc.nasa.gov/archive/natural/"
            f"{year}/{month}/{day}/jpg/{image_name}.jpg"
        )

        # Скачиваем картинку
        download_image(image_url, "images/nasa_epic")



def main():
    # fetch_spacex_last_launch()
    # fetch_nasa_picture_of_the_day()
    fetch_epic()
    # print(get_file_extension("https://example.com/txt/hello%20world.txt?v=9#python"))


if __name__ == '__main__':
    main()


