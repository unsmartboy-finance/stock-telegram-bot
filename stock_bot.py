import yfinance as yf
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with the token you got from BotFather
TELEGRAM_BOT_TOKEN = '7608250984:AAFvr06bPNTjAz5IQMgIK_kN6Sq3OnRUgzM'

from telegram import ReplyKeyboardMarkup

# Command handler for the /start command with a custom keyboard
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = """
    🚀 Welcome to StockPriceBot! 🚀

    Here are the commands you can use:
    /start - Start the bot
    /price <ticker> - Get the current price of a stock (e.g., /price AAPL)
    /news <ticker> - Get the latest news about a stock (e.g., /news AAPL)
    /help - Show this help message

    To get started, try typing:
    /price AAPL
    """
    # Create a custom keyboard
    keyboard = [["/price AAPL", "/news AAPL"], ["/help"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# Command handler for the /price command
async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Extract the stock ticker from the user's message
        ticker = context.args[0].upper()
        
        # Fetch stock data using yfinance
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")['Close'].iloc[-1]
        
        # Send the price back to the user
        await update.message.reply_text(f"The current price of {ticker} is ${price:.2f}")
    except IndexError:
        await update.message.reply_text("Please provide a stock ticker. Example: /price AAPL")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

import requests

# Replace 'YOUR_NEWSAPI_KEY' with your actual NewsAPI key
NEWSAPI_KEY = 'd3d6886a2f7b417b8df34ef2dca1aa21'

# Command handler for the /news command
async def get_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        ticker = context.args[0].upper()
        url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={NEWSAPI_KEY}"
        response = requests.get(url)
        news_data = response.json()

        if news_data['status'] == 'ok' and news_data['totalResults'] > 0:
            message = f"📰 Latest news for {ticker}:\n\n"
            for article in news_data['articles'][:5]:  # Show top 5 news articles
                title = article.get('title', 'No title available')
                url = article.get('url', 'No link available')
                message += f"• {title}\n{url}\n\n"
        else:
            message = f"No news found for {ticker}."
        await update.message.reply_text(message)
    except IndexError:
        await update.message.reply_text("Please provide a stock ticker. Example: /news AAPL")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# Command handler for the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    Welcome to StockPriceBot! Here are the commands you can use:
    /start - Start the bot
    /price <ticker> - Get the current price of a stock (e.g., /price AAPL)
    /news <ticker> - Get the latest news about a stock (e.g., /news AAPL)
    /help - Show this help message
    """
    await update.message.reply_text(help_text)

# Main function to start the bot
def main():
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("price", get_price))
    application.add_handler(CommandHandler("news", get_news))
    application.add_handler(CommandHandler("help", help_command))

    # Start the bot
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
'7608250984:AAFvr06bPNTjAz5IQMgIK_kN6Sq3OnRUgzM'
