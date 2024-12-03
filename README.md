# Telegram Stock Management Bot

This Telegram bot helps manage stock and sales records by interacting with Google Sheets. It allows you to:
- Add stock and sales items.
- View stock and sales data for specific dates.

## Features
- **Add Stock:** `/addstock <item> <quantity> <price>`
- **Add Sales:** `/addsales <item> <quantity> <price>`
- **View Stock:** `/viewstock <YYYY-MM-DD>`
- **View Sales:** `/viewsales <YYYY-MM-DD>`
- **Help Command:** `/help` for a list of all commands.

## Requirements
- Python 3.x
- `python-telegram-bot` library
- `gspread` library
- Google Cloud API credentials for Google Sheets

## Setup Instructions

### 1. Clone the repository
`git clone https://github.com/yourusername/telegram-stock-bot.git`
`cd telegram-stock-bot`

### 2. Install the required libraries
`pip install -r requirements.txt`

### 3. Set up Google Sheets API
- Go to the Google Cloud Console.
- Create a project and enable the Google Sheets API and Google Drive API.
- Create a Service Account, download the JSON file with credentials, and save it as credentials/service_account.json in the project folder.

### 4. Set up your bot
- Create a new bot on Telegram via BotFather.
- Copy your bot’s token and paste it in the TOKEN variable in the bot's code.
- `TOKEN = "YOUR TELEGRAM API TOKEN"`

### 5. Run the bot
`python telBot.py`
The bot should now be running and ready to manage stock and sales.

### 6. Usage
- `/start` **: Start the bot and get a welcome message.**
- `/help` **: Get a list of available commands.**
- `/addstock <item> <quantity> <price>` **: Add a stock entry.**
- `/addsales <item> <quantity> <price>` **: Add a sales entry.**
- `/viewstock <YYYY-MM-DD>` **: View stock entries for a specific date.**
- `/viewsales <YYYY-MM-DD>` **: View sales entries for a specific date.**

### 7. Contributing
Feel free to fork the repository, make changes, and submit a pull request.