#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position

import logging
import os
from dotenv import load_dotenv
load_dotenv()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import re


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


chrome_options = Options()
chrome_options.add_argument("no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Hi! 🤚\nSend me your node ID (12D3KooW...) and I will fetch data for you !")

# async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Send a message when the command /help is issued."""
#     await update.message.reply_text("Hi! 🤚\nSend me your node ID (12D3KooW...) and I will fetch data for you !")

# async def key_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Send a message when the command /help is issued."""
#     await update.message.reply_text("Hi! 🤚\nSend me your node ID (12D3KooW...) and I will fetch data for you !")

# async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Send a message when the command /help is issued."""
#     await update.message.reply_text("Hi! 🤚\nSend me your node ID (12D3KooW...) and I will fetch data for you !")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    nodeID = update.message.text
    #chat_id = update.effective_message.chat_id

    if not re.match(r'12D3KooW[a-zA-Z0-9]{44}$', nodeID):
        await update.message.reply_text("Send me a correct node ID")
        return

    browser = webdriver.Chrome(options=chrome_options)

    browser.get("https://tiascan.com/light-node/" + nodeID)
    content = browser.find_element(By.ID, "root").text
    content = browser.find_element(By.XPATH, '//*[@id="root"]/main/section/div/div[2]/div[2]').text
    browser.quit()

    if not content:
        await update.message.reply_text("node ID not found")
        return

    await update.message.reply_text(content)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    BOT_TOKEN = os.getenv('BOT_TOKEN')

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()