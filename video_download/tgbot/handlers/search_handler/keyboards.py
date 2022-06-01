from typing import Dict
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import tgbot.handlers.search_handler.static_text as static_text
import tgbot.handlers.download_handler.static_text as download_st
from tgbot.handlers.utils.change_type import to_str, to_dict

def build_menu(buttons, n_cols, header_buttons=None, bottom_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_button])
    if bottom_buttons:
        menu.append([bottom_buttons])
    return menu


def make_keyboard_to_ask_video(video_id) -> InlineKeyboardMarkup:
    button_text = static_text.download_video_text
    menu = [[InlineKeyboardButton(text=button_text, callback_data=video_id)]]
    return InlineKeyboardMarkup(inline_keyboard=menu)

def make_inline_keyboard_ask_quality(available_video_resolution: list, button_data: Dict) -> InlineKeyboardButton:
    buttons = []
    for resolution in available_video_resolution:
        button_data["resolution"] = resolution
        print(button_data)
        button_data = to_str(button_data)
        print(button_data)
        print(len(button_data.encode('utf-8')))
        buttons.append([InlineKeyboardButton(text=resolution, callback_data=button_data)])
        button_data = to_dict(button_data)
    button_data["resolution"] = download_st.GET_AUDIO_BUTTON
    button_data = to_str(button_data)
    buttons.append([InlineKeyboardButton(download_st.GET_AUDIO_BUTTON, callback_data=button_data)])
    return InlineKeyboardMarkup(inline_keyboard=buttons)