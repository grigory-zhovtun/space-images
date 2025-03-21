# Space Image Downloader & Publisher

This Python project fetches and manages images from SpaceX, NASA APOD, and NASA EPIC APIs and publishes them to a Telegram channel.

---

## Features

- Fetches SpaceX launch images.
- Downloads NASA Astronomy Picture of the Day (APOD) images.
- Retrieves NASA EPIC images.
- Publishes images to a Telegram channel at specified intervals.

---

## Prerequisites

- Python 3.6 or later
- A `requirements.txt` file specifying dependencies

---

## Installation and Setup

1. **Clone the repository or download the script:**\
   Ensure you have all the Python scripts and a `requirements.txt` file.

2. **(Optional) Create and activate a virtual environment:**\
   It is recommended to use a virtual environment to avoid conflicts with other Python packages.

   ```bash
   python -m venv venv
   source venv/bin/activate       # Linux/macOS
   venv\Scripts\activate          # Windows
   ```

3. **Install dependencies from requirements.txt:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:** Create a `.env` file in the project root directory and define the required variables.

   
## Environment Variables Setup

The application uses the following environment variables:

•	**TELEGRAM_API_KEY**: API key for the Telegram bot to post images in a channel.

•	**TELEGRAM_CHANNEL_ID**: Telegram channel ID where images will be sent.

•	**NASA_API_KEY**: Your API key for accessing NASA’s APOD (and EPIC) endpoints.

•	**NASA_APOD_IMAGES_PATH**: (Optional) Specifies the directory where NASA APOD images will be saved. Default: images/nasa_apod.

•	**IMAGES_DIRECTORY**: (Optional) Specifies the directory used for storing images by the application. Default: images.

•	**NASA_SPACEX_IMAGES_PATH**: (Optional) Specifies the directory used for storing images by the application. Default: images/spacex.

•	**NASA_EPIC_IMAGES_PATH**: (Optional) Specifies the directory used for storing images by the application. Default: images/nasa_epic.

Make sure to create a .env file in the project root and define these variables accordingly before running the program.
---



## Usage

### Fetching SpaceX Launch Images

```bash
python fetch_spacex_images.py --id <launch_id>
```

If no launch ID is provided, it will fetch the latest launch images.

### Fetching NASA APOD Images

```bash
python fetch_nasa_apod.py --count 10
```

Fetches 10 Astronomy Picture of the Day images. You can also specify a specific date using `--date YYYY-MM-DD`.

### Fetching NASA EPIC Images

```bash
python fetch_epic.py
```

Retrieves and downloads NASA EPIC images.

### Publishing Images to Telegram

```bash
python bot.py 4.0
```

Publishes images to the Telegram channel every 4 hours (default). Adjust the delay as needed.

---

## Example Output

```bash
(.venv) (base) % python fetch_spacex_images.py
Downloading image: https://example.com/image1.jpg
Downloading image: https://example.com/image2.jpg
Done!
```

```bash
(.venv) (base) % python bot.py 4.0
Sending image to Telegram channel...
Waiting for 4 hours before sending the next image...
```

---

## Notes

- Ensure you have valid API keys for NASA and Telegram before running the scripts.
- All downloaded images are stored in the `images/` directory under respective subdirectories.
- You can modify `bot.py` to change the Telegram channel ID where images are posted.

