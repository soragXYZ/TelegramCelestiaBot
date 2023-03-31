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
    CallbackContext,
    ContextTypes,
    MessageHandler,
    PicklePersistence,
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


async def register(update: Update, context: CallbackContext):
    try:
        _, nodeID = update.message.text.split(' ', 1)
    except:
        await update.message.reply_text("Send me a correct node ID")
        return

    if not re.match(r'12D3KooW[a-zA-Z0-9]{44}$', nodeID):
        await update.message.reply_text("Send me a correct node ID")
        return

    context.user_data["nodeID"] = nodeID.split()
    await update.message.reply_text('Your node ID has been registered 💾')


async def delete(update: Update, context: CallbackContext):
    context.user_data.pop("nodeID")
    await update.message.reply_text('Your node ID has been removed 🫡')


async def update(update: Update, context: CallbackContext):

    if not "nodeID" in context.user_data:
        await update.message.reply_text('Your node ID has not been registered yet, please add one')
        return

    try:
        _, nodeID = update.message.text.split(' ', 1)
    except:
        await update.message.reply_text("Send me a correct node ID")
        return

    if not re.match(r'12D3KooW[a-zA-Z0-9]{44}$', nodeID):
        await update.message.reply_text("Send me a correct node ID")
        return

    context.user_data["nodeID"] = text.split()
    await update.message.reply_text('Your node ID has been updated 🫡')


async def info(update: Update, context: CallbackContext):
    if "nodeID" in context.user_data:
        await update.message.reply_text('NodeID : ' + context.user_data["nodeID"][0])
    else:
        await update.message.reply_text('Your node ID has not been registered yet, please add one')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hi! 🤚\n"
        "I am the Celestia Light Node bot checker.\n"
        "Here are the command you can use:\n"
        "/help: Display this message\n"
        "/fetch: Enter a valid node ID (12D3KooW...) and I will display its data\n"
        "/register: Enter your node ID (12D3KooW...) and I will register it in my database. I will warn you if your node goes offline\n"
        "/update: Edit your registered node ID if any. Please enter a valid node ID (12D3KooW...)\n"
        "/delete: Remove your node ID from my database. You will not receive alerts anymore if your node goes offline\n"
        "/info: Display your current registered node ID, if any\n"
        "/get: Display data about your current registered node ID, if any"
    )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I did not recognized this command 😢. Please use /help")


async def fetch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    try:
        _, nodeID = update.message.text.split(' ', 1)
    except:
        await update.message.reply_text("Send me a correct node ID")
        return

    if not re.match(r'12D3KooW[a-zA-Z0-9]{44}$', nodeID):
        await update.message.reply_text("Send me a correct node ID")
        return

    browser = webdriver.Chrome(options=chrome_options)

    browser.get("https://tiascan.com/light-node/" + nodeID)
    content = browser.find_element(By.ID, "root").text
    content = browser.find_element(By.XPATH, '//*[@id="root"]/main/section/div/div[2]/div[2]').text
    browser.quit()

    if not content:
        await update.message.reply_text("Node ID not found, please retry")
        return

    await update.message.reply_text(content)


async def get(update: Update, context: CallbackContext):

    if not "nodeID" in context.user_data:
        await update.message.reply_text('Your node ID has not been registered yet, please add one')
        return

    nodeID = context.user_data["nodeID"][0]
    browser = webdriver.Chrome(options=chrome_options)

    browser.get("https://tiascan.com/light-node/" + nodeID)
    content = browser.find_element(By.ID, "root").text
    content = browser.find_element(By.XPATH, '//*[@id="root"]/main/section/div/div[2]/div[2]').text
    browser.quit()

    if not content:
        await update.message.reply_text("Node ID not found, please retry")
        return

    await update.message.reply_text(content)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    BOT_TOKEN = os.getenv('BOT_TOKEN')

    persistence = PicklePersistence(filepath="tgBotDB")
    application = Application.builder().token(BOT_TOKEN).persistence(persistence).build()

    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('get', get))
    application.add_handler(CommandHandler('register', register))
    application.add_handler(CommandHandler('delete', delete))
    application.add_handler(CommandHandler('update', update))
    application.add_handler(CommandHandler('info', info))
    application.add_handler(CommandHandler('fetch', fetch))
    application.add_handler(MessageHandler(filters.TEXT | filters.COMMAND, unknown))

    application.run_polling()


if __name__ == "__main__":
    main()