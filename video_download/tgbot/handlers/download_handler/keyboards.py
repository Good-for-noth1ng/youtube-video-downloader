from telegram import KeyboardButton, ReplyKeyboardMarkup
import tgbot.handlers.download_handler.static_text as static_text

def build_menu(buttons, n_cols, header_buttons=None, bottom_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_button])
    if bottom_buttons:
        menu.append([bottom_buttons])
    return menu

def make_keyboard_ask_video_or_playlist()->ReplyKeyboardMarkup:
    buttons = []

def make_keyboard_ask_format()->ReplyKeyboardMarkup:
    buttons = []

def make_keyboard_ask_quality()-> ReplyKeyboardMarkup:
    pass
