from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
import os
import argparse
from time import sleep
from utils import get_shuffled_image_paths


def start_command(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я тестовый бот. Используй /help, чтобы увидеть список команд.")


def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("Список доступных команд:\n/start - начать\n/help - помощь")


def echo_message(update: Update, context: CallbackContext):
    text_received = update.message.text
    update.message.reply_text(f"Вы написали: {text_received}")


def main():
    """
        Main entry point for publishing space photos to a Telegram channel.

        This function loads environment variables and retrieves the Telegram API key.
        It parses a command-line argument specifying the delay between image publications,
        with a default value of 4.0 hours. The function then enters an infinite loop where it:

        1. Retrieves a shuffled list of image file paths from the 'images' directory.
        2. Sends each image (as a document) to a designated Telegram channel.
        3. Waits for the specified delay (converted from hours to seconds) before sending the next image.

        Environment Variables:
            TELEGRAM_API_KEY (str): API key for the Telegram bot.

        Command-line Arguments:
            hours (float): Delay in hours between sending images. Defaults to 4.0 if not provided.
    """
    load_dotenv()
    api_key = os.environ.get('TELEGRAM_API_KEY')
    default_delay_hours = 4.0

    parser = argparse.ArgumentParser(
        description="Publish space photos to Telegram Channel"
    )
    parser.add_argument('hours', type=float, default=default_delay_hours)
    delay = parser.parse_args()

    bot = Bot(api_key)

    channel_id = "@space_images_learning_bot"

    while True:
        image_paths = get_shuffled_image_paths()

        for image_path in image_paths:
            bot.send_document(chat_id=channel_id, document=open(image_path, 'rb'))
            sleep(delay.hours * 3600)

if __name__ == "__main__":
    main()