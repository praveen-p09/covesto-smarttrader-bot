from telegram import Update, InputFile
from telegram.ext import CallbackContext
from utils.formatting import human_readable_number
import yfinance as yf
import datetime
import io
import matplotlib.pyplot as plt
from utils.currency import get_price_in_inr

# 📈 /stock command using yfinance
def stock_price(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("⚠️ Please provide a stock symbol. Example: `/stock AAPL`", parse_mode='Markdown')
        return

    symbol = context.args[0].upper()

    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        if 'regularMarketPrice' not in info or info['regularMarketPrice'] is None:
            update.message.reply_text(f"❌ No data found for symbol: {symbol}")
            return

        # Get currency
        currency = info.get('currency', 'USD')
        symbol_map = {
            'INR': '₹', 'USD': '$', 'EUR': '€', 'JPY': '¥', 'GBP': '£'
        }
        currency_symbol = symbol_map.get(currency, f"{currency} ")

        price = info['regularMarketPrice']
        price_in_inr = None

        # Convert to INR if not already INR
        if currency != 'INR':
            try:
                price_in_inr = get_price_in_inr(price, currency)
            except Exception:
                price_in_inr = None

        msg = (
            f"📊 *{info.get('shortName', symbol)} ({symbol})*\n"
            f"• Current Price: {currency_symbol}{price}"
        )

        if price_in_inr:
            msg += f"  (≈ ₹{price_in_inr})\n"
        else:
            msg += "\n"

        msg += (
            f"• Open: {currency_symbol}{info.get('open', 'N/A')}, "
            f"Prev Close: {currency_symbol}{info.get('previousClose', 'N/A')}\n"
            f"• Day Range: {currency_symbol}{info.get('dayLow', 'N/A')} - {currency_symbol}{info.get('dayHigh', 'N/A')}\n"
            f"• Volume: {human_readable_number(info.get('volume', 'N/A'))}\n"
            f"• Exchange: {info.get('exchange', 'N/A')}\n"
            f"• Market Cap: {human_readable_number(info.get('marketCap', 'N/A'))} {currency}\n"
            f"• PE Ratio: {info.get('trailingPE', 'N/A')}\n"
            f"• EPS: {info.get('trailingEps', 'N/A')}\n"
            f"• Dividend Yield: {info.get('dividendYield', 'N/A')}%\n"
            f"• ROE: {info.get('returnOnEquity', 'N/A')}\n"
            f"• Debt to Equity: {info.get('debtToEquity', 'N/A')}"
        )

        update.message.reply_text(msg, parse_mode='Markdown')

    except Exception as e:
        update.message.reply_text(f"⚠️ Error fetching stock data: {e}")


# 📉 /chart command using yfinance + matplotlib
def stock_chart(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("⚠️ Please provide a stock symbol. Example: `/chart AAPL`", parse_mode='Markdown')
        return

    symbol = context.args[0].upper()

    try:
        # Fetch data
        end = datetime.datetime.now()
        start = end - datetime.timedelta(days=30)
        data = yf.download(symbol, start=start, end=end)

        if data.empty:
            update.message.reply_text(f"❌ No chart data found for: {symbol}")
            return

        # Fetch currency info
        info = yf.Ticker(symbol).info
        currency = info.get('currency', 'USD')
        symbol_map = {'INR': '₹', 'USD': '$', 'EUR': '€', 'JPY': '¥', 'GBP': '£'}
        currency_symbol = symbol_map.get(currency, f"{currency} ")

        # Try converting to INR
        # price_in_inr = None
        # if currency != 'INR':
        #     try:
        #         close_vals = data['Close']
        #         data['INR'] = close_vals.apply(lambda x: round(c.convert(currency, 'INR', x), 2))
        #         price_in_inr = True
        #     except Exception:
        #         price_in_inr = False

        # Plot
        plt.figure(figsize=(10, 5))
        plt.plot(data.index, data['Close'], label=f"{currency_symbol} Close Price", marker='o')
        # if price_in_inr:
        #     plt.plot(data.index, data['INR'], label="₹ Price", linestyle='--')

        plt.title(f"{symbol} - Closing Price (Last 30 Days)")
        plt.xlabel("Date")
        plt.ylabel(f"Price ({currency_symbol})")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        # Save to memory
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        update.message.reply_photo(photo=InputFile(buf, filename=f"{symbol}_chart.png"))

    except Exception as e:
        update.message.reply_text(f"⚠️ Error generating chart: {e}")

def compare_stocks(update: Update, context: CallbackContext):
    symbols = context.args

    if len(symbols) < 2:
        update.message.reply_text("⚠️ Please provide at least 2 stock symbols to compare.\nExample: `/compare AAPL TSLA`", parse_mode='Markdown')
        return

    try:
        start = datetime.datetime.now() - datetime.timedelta(days=30)
        end = datetime.datetime.now()

        data_dict = {}
        currency_dict = {}

        for symbol in symbols:
            stock = yf.Ticker(symbol)
            hist = stock.history(start=start, end=end)

            if hist.empty:
                update.message.reply_text(f"❌ No data found for: {symbol}")
                continue

            info = stock.info
            currency = info.get("currency", "USD")
            currency_dict[symbol] = currency
            data_dict[symbol] = hist["Close"]

        if not data_dict:
            update.message.reply_text("❌ No valid data to compare.")
            return

        # Plot
        plt.figure(figsize=(10, 6))
        for symbol, close_series in data_dict.items():
            plt.plot(close_series.index, close_series.values, label=f"{symbol} ({currency_dict[symbol]})")

        plt.title("📊 Stock Comparison (Last 30 Days)")
        plt.xlabel("Date")
        plt.ylabel("Closing Price")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Send plot
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        update.message.reply_photo(photo=InputFile(buf, filename="comparison.png"))

    except Exception as e:
        update.message.reply_text(f"⚠️ Error comparing stocks: {e}")
