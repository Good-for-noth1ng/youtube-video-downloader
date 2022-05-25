import datetime

from django.utils import timezone
from telegram import ParseMode, Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

def command_start(update: Update, context: CallbackContext):
    pass

def make_keyboard_to_start() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(text="hey, sup?", url="https://github.com/Good-for-noth1ng/ScheduleBot")
    ]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)