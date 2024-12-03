

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your bot token
TOKEN = "YOUR_TELEGRAM_BOT_API_KEY"


# Define the /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the command /start is issued."""
    await update.message.reply_text("Hello! I am here to assist with stock management.")


# Define the /help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_message = (
        "📋 *Available Commands:*\n\n"
        "🛒 *Command to add stock:*\n"
        "Format: `/addstock <item> <quantity> <price>`\n"
        "Mfano: `/addstock maziwa 10 2000`\n\n"
        "💸 *Command to add sales:*\n"
        "Format: `/addsales <item> <quantity> <price>`\n"
        "Mfano: `/addsales soda 10 3000`\n\n"
        "📦 *Command to view stocks:*\n"
        "Format: `/viewstock <review-date(Y:M:D)>`\n"
        "Mfano: `/viewstock 2024-11-19`\n\n"
        "📈 *Command to view sales:*\n"
        "Format: `/viewsales <review-date(Y:M:D)>`\n"
        "Mfano: `/viewsales 2024-11-23`\n"
    )
    await update.message.reply_text(help_message, parse_mode="Markdown")


#add stock
async def add_stock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Extract arguments from the command
        args = context.args
        if len(args) != 3:
            await update.message.reply_text("Usage: /add <item> <quantity> <price>")
            return
        
        item, quantity, price = args
        
         # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Connect to Google Sheets
        import gspread
        from google.oauth2.service_account import Credentials

        SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 
                  'https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file(
            'YOUR_JSON_FILE.json', scopes=SCOPES
        )
        client = gspread.authorize(credentials)
        sheet = client.open("sheet_name").sheet1

        # Add a row to the Google Sheet
        sheet.append_row([item, quantity, price, timestamp, "Added via bot"])
        await update.message.reply_text(f"Stock added: {item}, {quantity}, {price} , {timestamp}")

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
        
 
 #add sales
async def add_sales(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Extract arguments from the command
        args = context.args
        if len(args) != 3:
            await update.message.reply_text("Usage: /add <item> <quantity> <price>")
            return
        
        item, quantity, price = args
        
         # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Connect to Google Sheets
        import gspread
        from google.oauth2.service_account import Credentials

        SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 
                  'https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file(
            'YOUR_JSON_FILE.json', scopes=SCOPES
        )
        client = gspread.authorize(credentials)
        sheet = client.open("sheet_name").get_worksheet(1)

        # Add a row to the Google Sheet
        sheet.append_row([item, quantity, price, timestamp, "Added via bot"])
        await update.message.reply_text(f"Sales added: {item}, {quantity}, {price} , {timestamp}")

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
        


#view stock
async def view_stock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Extract arguments
        args = context.args
        if len(args) != 1:
            await update.message.reply_text("Usage: /viewstock <YYYY-MM-DD>")
            return

        filter_date = args[0]
        try:
            filter_date_obj = datetime.strptime(filter_date, "%Y-%m-%d")
        except ValueError:
            await update.message.reply_text("Invalid date format. Use YYYY-MM-DD.")
            return

        # Connect to Google Sheets
        import gspread
        from google.oauth2.service_account import Credentials

        SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 
                  'https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file(
            'YOUR_JSON_FILE.json', scopes=SCOPES
        )
        client = gspread.authorize(credentials)
        sheet = client.open("sheet_name").sheet1

        # Get all records
        records = sheet.get_all_records()
        if not records:
            await update.message.reply_text("No stock entries found.")
            return

        # Filter records by date
        filtered_records = []
        for record in records:
            timestamp = record.get('Date', '')
            if timestamp:
                record_date = datetime.strptime(timestamp.split(' ')[0], "%Y-%m-%d")
                if record_date == filter_date_obj:
                    filtered_records.append(record)

        if not filtered_records:
            await update.message.reply_text(f"No stock entries found for {filter_date}.")
            return

        # Format and send the filtered records
        response = f"📦 *Stock Entries for {filter_date}:*\n"
        for record in filtered_records:
            item = record.get('Item', 'N/A')
            quantity = record.get('Quantity', 'N/A')
            price = record.get('Price', 'N/A')
            timestamp = record.get('Date', 'N/A')  # Ensure Timestamp is included
            
            response += f"- {item} | Quantity: {quantity} | Price: {price} | Added on: {timestamp}\n"

        await update.message.reply_text(response, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


#view sales
async def view_sales(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Extract arguments
        args = context.args
        if len(args) != 1:
            await update.message.reply_text("Usage: /viewsales <YYYY-MM-DD>")
            return

        filter_date = args[0]
        try:
            filter_date_obj = datetime.strptime(filter_date, "%Y-%m-%d")
        except ValueError:
            await update.message.reply_text("Invalid date format. Use YYYY-MM-DD.")
            return

        # Connect to Google Sheets
        import gspread
        from google.oauth2.service_account import Credentials

        SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 
                  'https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file(
            'YOUR_JSON_FILE.json', scopes=SCOPES
        )
        client = gspread.authorize(credentials)
        sheet = client.open("sheet_name").get_worksheet(1)

        # Get all records
        records = sheet.get_all_records()
        if not records:
            await update.message.reply_text("No Sales entries found.")
            return

        # Filter records by date
        filtered_records = []
        for record in records:
            timestamp = record.get('Date', '')
            if timestamp:
                record_date = datetime.strptime(timestamp.split(' ')[0], "%Y-%m-%d")
                if record_date == filter_date_obj:
                    filtered_records.append(record)

        if not filtered_records:
            await update.message.reply_text(f"No Sales entries found for {filter_date}.")
            return

        # Format and send the filtered records
        response = f"📦 *Sales Entries for {filter_date}:*\n"
        for record in filtered_records:
            item = record.get('Item', 'N/A')
            quantity = record.get('Quantity', 'N/A')
            price = record.get('Price', 'N/A')
            timestamp = record.get('Date', 'N/A')  # Ensure Timestamp is included
            
            response += f"- {item} | Quantity: {quantity} | Price: {price} | Added on: {timestamp}\n"

        await update.message.reply_text(response, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


# Define the text message handler
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user text messages."""
    user_message = update.message.text
    # Example: Respond to specific input
    if user_message.lower() == "hello":
        await update.message.reply_text("Hi there! How can I assist you?")
    elif user_message.lower() == "stock report":
        await update.message.reply_text("Please provide the stock details.")
    else:
        await update.message.reply_text(
            f"You said: '{user_message}'. How can I help you with that?"
        )


# Define an unknown command handler
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle unknown commands."""
    await update.message.reply_text("Sorry, I didn't understand that command.")


def main():
    """Run the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("addstock", add_stock))
    application.add_handler(CommandHandler("addsales", add_sales))
    application.add_handler(CommandHandler("viewstock", view_stock))
    application.add_handler(CommandHandler("viewsales", view_sales))


    # Add a text message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Add a handler for unknown commands
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Start the bot
    application.run_polling()


if __name__ == "__main__":
    main()
