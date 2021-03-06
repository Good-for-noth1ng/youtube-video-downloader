from telegram import KeyboardButton, ReplyKeyboardMarkup
import tgbot.handlers.download_handler.static_text as static_text

def build_menu(buttons, n_cols, header_buttons=None, bottom_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_button])
    if bottom_buttons:
        menu.append([bottom_buttons])
    return menu

def make_keyboard_ask_quality_for_playlist()->ReplyKeyboardMarkup:
    buttons = []
    buttons.append(static_text.GET_HIGHEST_RESOLUTION_BUTTON)
    buttons.append(static_text.GET_LOWEST_RESOLUTION_BUTTON)
    menu = build_menu(buttons=buttons, n_cols=2, bottom_buttons=static_text.GET_AUDIO_BUTTON)
    return ReplyKeyboardMarkup(keyboard=menu, resize_keyboard=True, one_time_keyboard=True)

def make_keyboard_ask_quality(available_video_resolution)-> ReplyKeyboardMarkup:
    menu = build_menu(buttons=available_video_resolution, n_cols=2, bottom_buttons=static_text.GET_AUDIO_BUTTON)
    return ReplyKeyboardMarkup(keyboard=menu, resize_keyboard=True, one_time_keyboard=True)
