from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from utils.validations import is_valid_email, is_valid_mobile
from utils.sheets import save_user_data

NAME, EMAIL, MOBILE, ADDRESS, CONFIRM, SELECT_EDIT = range(6)

# Form Conversation
def start_kyc(update: Update, context: CallbackContext):
    context.user_data.clear()
    update.message.reply_text(
        "🧾 Let's begin your KYC.\n\nPlease enter your *Name*:",
        parse_mode='Markdown',
        reply_markup=ReplyKeyboardRemove()  # remove any previous keyboards
    )
    return NAME


def get_name(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text
    if context.user_data.get('editing'):
        context.user_data['editing'] = False
        return show_confirmation(update, context)
    update.message.reply_text("Enter your *Email*:", parse_mode='Markdown')
    return EMAIL

def get_email(update: Update, context: CallbackContext):
    email = update.message.text
    if not is_valid_email(email):
        update.message.reply_text("❌ Invalid email. Please enter a valid one (e.g., example@domain.com).")
        return EMAIL
    context.user_data['email'] = email
    if context.user_data.get('editing'):
        context.user_data['editing'] = False
        return show_confirmation(update, context)
    update.message.reply_text("Enter your *Mobile Number*:", parse_mode='Markdown')
    return MOBILE

def get_mobile(update: Update, context: CallbackContext):
    mobile = update.message.text
    if not is_valid_mobile(mobile):
        update.message.reply_text("❌ Invalid mobile number. Enter 10–13 digit number only.")
        return MOBILE
    context.user_data['mobile'] = mobile
    if context.user_data.get('editing'):
        context.user_data['editing'] = False
        return show_confirmation(update, context)
    update.message.reply_text("Enter your *Address*:", parse_mode='Markdown')
    return ADDRESS

def get_address(update: Update, context: CallbackContext):
    context.user_data['address'] = update.message.text
    if context.user_data.get('editing'):
        context.user_data['editing'] = False
        return show_confirmation(update, context)
    return show_confirmation(update, context)

def show_confirmation(update: Update, context: CallbackContext):
    user_data = context.user_data
    summary = (
        f"📋 *Please confirm your details:*\n\n"
        f"*Name:* {user_data['name']}\n"
        f"*Email:* {user_data['email']}\n"
        f"*Mobile:* {user_data['mobile']}\n"
        f"*Address:* {user_data['address']}\n"
    )
    reply_keyboard = [['✅ Confirm', '🛠️ Edit'], ['❌ Cancel']]
    update.message.reply_text(
        summary + "\nChoose an option:",
        parse_mode='Markdown',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return CONFIRM

def confirm(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    if 'confirm' in text:
        save_user_data(  
            context.user_data['name'],
            context.user_data['email'],
            context.user_data['mobile'],
            context.user_data['address']
        )
        update.message.reply_text("✅ Your details have been saved!", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    elif 'edit' in text:
        reply_keyboard = [['Name', 'Email'], ['Mobile', 'Address']]
        update.message.reply_text(
            "Which field do you want to edit?",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        )
        return SELECT_EDIT
    elif 'cancel' in text:
        return cancel(update, context)


def select_field(update: Update, context: CallbackContext):
    field = update.message.text.lower()
    context.user_data['editing'] = True
    if field == 'name':
        update.message.reply_text("Enter your *Name*:", parse_mode='Markdown')
        return NAME
    elif field == 'email':
        update.message.reply_text("Enter your *Email*:", parse_mode='Markdown')
        return EMAIL
    elif field == 'mobile':
        update.message.reply_text("Enter your *Mobile Number*:", parse_mode='Markdown')
        return MOBILE
    elif field == 'address':
        update.message.reply_text("Enter your *Address*:", parse_mode='Markdown')
        return ADDRESS
    else:
        update.message.reply_text("❗ Please choose a valid field.")
        return SELECT_EDIT

def cancel(update: Update, context: CallbackContext):
    # Reset user data (optional)
    context.user_data.clear()
    
    # Send cancel message
    update.message.reply_text(
        "❌ Operation cancelled. You can /kyc again anytime.",
        reply_markup=ReplyKeyboardRemove()
    )
    
    return ConversationHandler.END
