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


def send_image(image_path, channel_id, bot):
    with open(image_path, "rb") as doc:
        bot.send_document(chat_id=channel_id, document=doc)


def send_image_with_retry(image_path, channel_id, bot):
    """Send an image with a retry.

    Args:
        image_path (str): Path to the image to send.
        channel_id (str): Channel ID.
        bot (telegram.Bot): Bot to send the image with.
    """
    while True:
        try:
            send_image(image_path, channel_id, bot)
            logging.info(f"Published image: {image_path}")
            break
        except (NetworkError, requests.exceptions.ConnectionError) as e:
            logging.error(
                f"Network error encountered while sending {image_path}: {e}. Retrying in 1 second..."
            )
            sleep(1)


def main():
    """Publish space photos to a Telegram channel."""
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
        help="Path to image. If it is empty, will publish random image."
    )
    parser.add_argument(
        "--chat_id",
        type=str,
        help="Telegram chat ID for publishing messages"
    )

    args = parser.parse_args()
    bot = Bot(api_key)

    channel_id = args.chat_id if args.chat_id else os.environ['TELEGRAM_CHANNEL_ID']

    if args.image:
        if not os.path.exists(args.image):
            logging.error(f"Image {args.image} not found.")
            sys.exit(1)
        send_image_with_retry(args.image, channel_id, bot)
        logging.info("Image published.")
        return

    while True:
        images_directory = os.getenv("IMAGES_DIRECTORY", "images")
        if images_directory is None:
            raise ValueError("IMAGES_DIRECTORY environment variable must be set.")
        image_paths = get_shuffled_image_paths(images_directory)
        for image_path in image_paths:
            send_image_with_retry(image_path, channel_id, bot)
            sleep(args.hours * 3600)


if __name__ == "__main__":
    main()