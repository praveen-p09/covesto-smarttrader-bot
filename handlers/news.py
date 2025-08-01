from telegram import Update
from telegram.ext import CallbackContext
from urllib.parse import quote
import feedparser

def get_news_links_from_rss(stock_symbol: str, count: int = 10) -> str:
    # Encode properly for the RSS URL
    query = quote(f"{stock_symbol} stock")  # e.g., "GOOG stock" becomes "GOOG%20stock"
    url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"

    # Parse RSS feed
    feed = feedparser.parse(url)
    if not feed.entries:
        return "❌ No recent news articles found."

    # Collect headlines with links
    headlines = [
        f"• [{entry.title}]({entry.link})"
        for entry in feed.entries[:count]
    ]
    return "\n".join(headlines)

def news(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("⚠️ Please provide a stock symbol. Example: `/news GOOG`", parse_mode='Markdown')
        return

    symbol = context.args[0].upper()

    try:
        news_links = get_news_links_from_rss(symbol)
        update.message.reply_text(f"📰 *Latest News for {symbol}*:\n{news_links}", parse_mode='Markdown', disable_web_page_preview=True)
    except Exception as e:
        update.message.reply_text(f"⚠️ Error fetching news: {e}")