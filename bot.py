"""Bot for publish to Telegram Channel.

Module for publishing space photos to a Telegram channel
using a Telegram bot.
"""
from telegram import Bot
from telegram.error import NetworkError
import requests
from dotenv import load_dotenv
import os
import sys
import logging
import argparse
from time import sleep
from utils import get_shuffled_image_paths


def main():
    """Publish space photos to a Telegram channel.

    Load environment variables and retrieve the Telegram API key.
    Parse command-line arguments. If an image path is provided via the
    '--image' argument, send that image to the Telegram channel.
    Otherwise, retrieve a shuffled list of image file paths from the 'images'
    directory and send each image (as a document) to the channel in an infinite
    loop with a delay specified by the '--hours' argument
    (default is 4.0 hours).

    Environment Variables:
        TELEGRAM_API_KEY (str): API key for the Telegram bot.

    Command-line Arguments:
        --hours (float): Delay in hours between sending images.
                         Defaults to 4.0.
        --image (str): Optional; path to a specific image file. If provided,
                       send this image instead of publishing a random image.

    Raises:
        SystemExit: If the image specified by '--image' does not exist.
    """
    load_dotenv()
    api_key = os.environ['TELEGRAM_API_KEY']
    default_delay_hours = 4.0

    parser = argparse.ArgumentParser(
        description="Publish space photos to Telegram Channel"
    )
    parser.add_argument("--hours", type=float, default=default_delay_hours)
    parser.add_argument(
        "--image",
        type=str,
        help=(
            "Path to image. If it is empty, will publish random image."
        ),
    )
    parser.add_argument(
        "--chat_id",
        type=str,
        help="Telegram chat ID for publishing messages"
    )

    args = parser.parse_args()

    bot = Bot(api_key)

    if args.chat_id:
        channel_id = args.chat_id
    else:
        channel_id = os.environ['CHANNEL_ID']


    def send_image(image_path, channel_id, bot):
        with open(image_path, "rb") as doc:
            bot.send_document(chat_id=channel_id, document=doc)


    if args.image:
        if not os.path.exists(args.image):
            logging.error(f"Image {args.image} not found.")
            sys.exit(1)
        send_image(args.image, channel_id, bot)
        logging.info("Image published.")
        return

    while True:
        try:
            images_directory = os.getenv("IMAGES_DIRECTORY", "images")
            if images_directory is None:
                raise ValueError("IMAGES_DIRECTORY environment variable must be set.")
            image_paths = get_shuffled_image_paths(images_directory)
            for image_path in image_paths:
                try:
                    send_image(image_path, channel_id, bot)
                    logging.info(f"Published image: {image_path}")
                except (NetworkError, requests.exceptions.ConnectionError) as e:
                    logging.error(f"Network error encountered while sending {image_path}: {e}. Retrying in 1 second...")
                    sleep(1)
                    continue
                sleep(args.hours * 3600)
        except (NetworkError, requests.exceptions.ConnectionError) as e:
            logging.error(f"Network error encountered: {e}. Retrying in 1 second...")
            sleep(1)
            continue


if __name__ == "__main__":
    main()