import datetime

from django.utils import timezone
from telegram import ParseMode, Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from tgbot.handlers.start_handler import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from tgbot.models import User

def command_start(update: Update, context: CallbackContext):
    u, created = User.get_user_and_created(update, context)
    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)
    update.message.reply_text(text=text)

def make_keyboard_to_start() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(text=static_text.github_button, url="https://github.com/Good-for-noth1ng")
    ]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)