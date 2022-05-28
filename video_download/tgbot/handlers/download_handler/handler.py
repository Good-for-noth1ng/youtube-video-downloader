import re
from pathlib import Path
from functools import partial
from telegram import ParseMode, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler

import pytube

import tgbot.handlers.download_handler.conversation_state as conversation_state
import tgbot.handlers.download_handler.static_text as static_text
import tgbot.handlers.download_handler.keyboards as keyboards

VIDEO_DOWNLOAD_DIRECTORY = Path(__file__).resolve().parent.parent.parent / "downloaded_videos"

def ask_put_url(update: Update, context: CallbackContext) -> str:
    update.message.reply_text(
        text=static_text.send_url_text, 
    )
    return conversation_state.PUT_URL_STATE

    
def extract_video_format_and_quality(update: Update, context: CallbackContext) -> str:
    url: str = update.message.text
    yt = pytube.YouTube(url=url, on_complete_callback=partial(callback_for_video_download, update=update))
    yt.check_availability()
    yt.streams.get_highest_resolution().download(output_path=VIDEO_DOWNLOAD_DIRECTORY)
    return conversation_state.PUT_URL_STATE
    
def callback_for_video_download(stream: pytube.YouTube, path_to_video: Path, update: Update):
    update.message.reply_text(static_text.download_is_sucessful_text)
    video = open(path_to_video, 'rb')
    update.message.reply_video(video)
    return conversation_state.PUT_URL_STATE 


def not_youtube_domain(update: Update, context: CallbackContext):
    update.message.reply_text(text=static_text.not_youtube_domain_text)
    return conversation_state.PUT_URL_STATE

def ask_format(update: Update, context: CallbackContext):
    pass


def stop(update: Update, context: CallbackContext):
    context.user_data.clear()
    ConversationHandler.END