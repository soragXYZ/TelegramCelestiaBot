# TelegramCelestiaBot

## Description

This is a light Telegram bot, which can be use to pull data from your lightnode. The bot is written in Python and scraps data from Tiascan

## Usage
Contact the bot at https://t.me/Celestia_LightBot.  

Commands:  
+ /help Display the help message
+ /fetch: Enter a valid node ID (12D3KooW...) and pull its data
+ /register: Enter your node ID (12D3KooW...) register it
+ /update: Edit your registered node ID if any
+ /delete: Remove your node ID from the database
+ /info: Display your current registered node ID, if any
+ /get: Display data about your current registered node ID, if any

## Installation
Tested on Ubuntu 22.04 only

Create a virtual environment
```
python3 -m venv venv
```

Activate environment
```
source venv/bin/activate
```

Install dependencies
```
pip install -r requirements.txt
```

Create a .env with your BOT_TOKEN, given by the bot father when you create your bot
```
echo BOT_TOKEN="xxxxxxxx" > .env
```

Start the bot
```
nophup python3 bot.py &
```

Enjoy