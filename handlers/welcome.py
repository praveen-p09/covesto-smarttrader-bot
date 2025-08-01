from telegram import Update
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 *Welcome to Covesto SmartTrader Bot!*\n\n"
        "Here's what I can do for you:\n\n"
        "📊 *Stock Info*\n"
        "• /stock SYMBOL – Get stock details\n"
        "   _Example:_ /stock AAPL, /stock RELIANCE.NS\n\n"
        "📉 *Stock Chart*\n"
        "• /chart SYMBOL – View 30-day price chart\n"
        "   _Example:_ /chart TSLA, /chart TCS.NS\n\n"
        "📈 *Compare Stocks*\n"
        "• /compare SYMBOL1 SYMBOL2 ... – Compare multiple stocks visually\n"
        "   _Example:_ /compare INFY.NS WIPRO.NS or /compare AAPL MSFT\n\n"
        "📰 *Stock News*\n"
        "• /news SYMBOL – Latest news from Google Finance\n"
        "   _Example:_ /news HDFCBANK.NS\n\n"
        "💡 *Explain Financial Terms*\n"
        "• /explain TOPIC – Get a short explanation using AI\n"
        "   _Example:_ /explain stock split, /explain EPS\n\n"
        "🧾 *KYC Form*\n"
        "• /kyc – Fill out your KYC details (Name, Email, etc.)\n\n"
        "ℹ️ _Note: For Indian stocks, use .NS at the end of the symbol (e.g., RELIANCE.NS, TCS.NS)._\n\n"
        "Type any command above to begin!",
        parse_mode='Markdown'
    )
