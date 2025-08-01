from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from handlers.stock import stock_price, stock_chart, compare_stocks
from handlers.news import news
from handlers.explain import explain
from handlers.kyc import (
    start_kyc, get_name, get_email, get_mobile, get_address,
    confirm, select_field, cancel,
    NAME, EMAIL, MOBILE, ADDRESS, CONFIRM, SELECT_EDIT
)
from handlers.welcome import start
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('stock', stock_price))
    dp.add_handler(CommandHandler('chart', stock_chart))
    dp.add_handler(CommandHandler('compare', compare_stocks))
    dp.add_handler(CommandHandler('news', news))
    dp.add_handler(CommandHandler('explain', explain))

    # KYC conversation handler
    conv_handler = ConversationHandler(
    entry_points=[CommandHandler('kyc', start_kyc)],
    states={
        NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
        EMAIL: [MessageHandler(Filters.text & ~Filters.command, get_email)],
        MOBILE: [MessageHandler(Filters.text & ~Filters.command, get_mobile)],
        ADDRESS: [MessageHandler(Filters.text & ~Filters.command, get_address)],
        CONFIRM: [MessageHandler(Filters.text & ~Filters.command, confirm)],
        SELECT_EDIT: [MessageHandler(Filters.text & ~Filters.command, select_field)],
    },
    fallbacks=[
        CommandHandler('cancel', cancel),
        MessageHandler(Filters.regex('^(❌ Cancel)$'), cancel),
    ],
)


    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
