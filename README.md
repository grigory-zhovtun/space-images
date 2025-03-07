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

   **Required Environment Variables**

   - **NASA\_API\_KEY**\
     *Type:* String\
     *Description:* API key for accessing NASA's APOD and EPIC data.\
     *Example:*

     ```env
     NASA_API_KEY=your_nasa_api_key_here
     ```

   - **TELEGRAM\_API\_KEY**\
     *Type:* String\
     *Description:* API key for the Telegram bot to post images in a channel.\
     *Example:*

     ```env
     TELEGRAM_API_KEY=your_telegram_bot_api_key_here
     ```

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

