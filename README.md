# Matatu Route Bot 2026

A Telegram bot that provides Nairobi matatu route information, boarding points, and real-time (estimated) fare prices based on peak/off-peak hours.

## Setup
1. Install dependencies: `pip install python-telegram-bot`
2. Get a Bot Token from [@BotFather](https://t.me/botfather) on Telegram.
3. Open `bot.py` and replace `YOUR_BOT_TOKEN_HERE` with your actual token.
4. Run the script: `python bot.py`

## Commands
- `/start`: Initialize the bot
- `/routes`: Show list of available matatu numbers
- `/fare <number>`: Check current fare for a route
- `/search <destination>`: Find a route number by area name

## Disclaimer
Fare data is mocked for demonstration purposes and reflects general Nairobi trends.