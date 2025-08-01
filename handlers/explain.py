from telegram import Update
from telegram.ext import CallbackContext
from utils.gemini import ask_gemini
import google.generativeai as genai

# Ask Gemini to explain or summarize
def ask_gemini(prompt: str) -> str:
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text.strip() if response else "❌ No response from Gemini."


def explain(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("⚠️ Please provide a stock symbol or topic to explain.\n\nExample: `/explain stock split`", parse_mode='Markdown')
        return

    topic = ' '.join(context.args)

    prompt = f"Explain the following in 3-5 lines as if you're speaking to a retail stock trader in India: {topic}"
    try:
        response = ask_gemini(prompt)
        update.message.reply_text(f"💡 *Explanation for:* `{topic}`\n\n{response}", parse_mode='Markdown')
    except Exception as e:
        update.message.reply_text(f"⚠️ Error: {e}")