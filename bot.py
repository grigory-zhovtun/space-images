from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
import os


def start_command(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я тестовый бот. Используй /help, чтобы увидеть список команд.")


def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("Список доступных команд:\n/start - начать\n/help - помощь")


def echo_message(update: Update, context: CallbackContext):
    text_received = update.message.text
    update.message.reply_text(f"Вы написали: {text_received}")


def main():
    load_dotenv()
    TOKEN = os.environ.get('TELEGRAM_API_KEY')

    bot = Bot(TOKEN)

    channel_id = "@space_images_learning_bot"

    bot.send_document(chat_id=channel_id, document=open('images/spacex/16763151866_35a0a4d8e1_o.jpg', 'rb'))
    # bot.send_message(chat_id=channel_id, text="Привет! Это тестовое сообщение в канал.")

if __name__ == "__main__":
    main()