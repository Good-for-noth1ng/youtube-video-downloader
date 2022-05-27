import re

from telegram import ParseMode, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler

import pytube

import tgbot.handlers.download_handler.conversation_state as conversation_state
import tgbot.handlers.download_handler.static_text as static_text
import tgbot.handlers.download_handler.keyboards as keyboards
   

def ask_put_url(update: Update, context: CallbackContext) -> str:
    update.message.reply_text(
        text=static_text.send_url_text, 
    )
    return conversation_state.PUT_URL_STATE

def extract_video_format_and_quality(update: Update, context: CallbackContext) -> str:
    url: str = update.message.text
    yt = pytube.YouTube(url=url)
    yt.streams.filter(file_extension='mp4')
    return conversation_state.PUT_URL_STATE
    # video_or_playlist = update.message.text
    # if video_or_playlist == static_text.VIDEO_BUTTON:
    #     context.user_data["video_or_playlist"] = "video"
    # else:
    #     context.user_data["video_or_playlist"] = "playlist"
    # update.message.reply_text(text)
    # return conversation_state.ASK_FORMAT_STATE

def not_youtube_domain(update: Update, context: CallbackContext):
    update.message.reply_text(text=static_text.not_youtube_domain_text)
    return conversation_state.PUT_URL_STATE

def ask_format(update: Update, context: CallbackContext):
    pass

def start_download(update: Update, context: CallbackContext):
    url = update.message.text
    is_youtube_domain = check_youtube_domain(url)
    if is_youtube_domain:
        update.message.reply_text(text=static_text.choose_video_format_text, reply_markup=keyboards.make_keyboard_ask_format())
    else:
        update.message.reply_text(text=static_text.not_youtube_domain_text)
