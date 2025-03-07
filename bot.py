"""Bot for publish to Telegram Channel.

Module for publishing space photos to a Telegram channel
using a Telegram bot.
"""

from telegram import Bot
from dotenv import load_dotenv
import os
import sys
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
    api_key = os.environ.get("TELEGRAM_API_KEY")
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

    args = parser.parse_args()

    bot = Bot(api_key)

    channel_id = "@space_images_learning_bot"

    if args.image:
        if not os.path.exists(args.image):
            print(f"Image {args.image} not found.")
            sys.exit(1)
        with open(args.image, "rb") as doc:
            bot.send_document(chat_id=channel_id, document=doc)
        print("Image published.")
        return

    while True:
        image_paths = get_shuffled_image_paths()
        for image_path in image_paths:
            with open(image_path, "rb") as doc:
                bot.send_document(chat_id=channel_id, document=doc)
            sleep(args.hours * 3600)


if __name__ == "__main__":
    main()