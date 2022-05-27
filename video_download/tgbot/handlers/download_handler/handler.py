from telegram import ParseMode, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler
import re

import pytube
import tgbot.handlers.download_handler.conversation_state as conversation_state
import tgbot.handlers.download_handler.static_text as static_text
import tgbot.handlers.download_handler.keyboards as keyboards

def check_youtube_domain(url: str) -> bool:
    regex_pattern = re.compile(r'https:\/\/youtube\.com')
    match = regex_pattern.search(url)
    if match:
        return True
    else:
        return False
    

def ask_video_or_playlist(update: Update, context: CallbackContext) -> str:
    pass
    # video_or_playlist = update.message.text
    # if video_or_playlist == static_text.VIDEO_BUTTON:
    #     context.user_data["video_or_playlist"] = "video"
    # else:
    #     context.user_data["video_or_playlist"] = "playlist"
    # update.message.reply_text(text)
    # return conversation_state.ASK_FORMAT_STATE

def ask_format(update: Update, context: CallbackContext):
    pass

def start_download(update: Update, context: CallbackContext):
    url = update.message.text
    is_youtube_domain = check_youtube_domain(url)
    if is_youtube_domain:
        update.message.reply_text(text=static_text.choose_video_format_text, reply_markup=keyboards.make_keyboard_ask_format())
    else:
        update.message.reply_text(text=static_text.not_youtube_domain_text)
