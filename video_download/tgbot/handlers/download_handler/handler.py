import os
from pathlib import Path
from functools import partial

import pytube
from telegram import ParseMode, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler


import tgbot.handlers.download_handler.conversation_state as conversation_state
import tgbot.handlers.download_handler.static_text as static_text
import tgbot.handlers.download_handler.keyboards as keyboards

DOWNLOAD_DIRECTORY = Path(__file__).resolve().parent.parent.parent / "downloaded_videos"

def ask_put_url(update: Update, context: CallbackContext) -> str:
    update.message.reply_text(
        text=static_text.send_url_text, 
    )
    return conversation_state.PUT_URL_STATE

    
def extract_video_format_and_quality(update: Update, context: CallbackContext) -> str:
    url: str = update.message.text
    yt = pytube.YouTube(url=url)
    # yt = pytube.YouTube(url=url, on_complete_callback=partial(callback_for_audio_download, update=update))
    streams = yt.streams.filter(progressive=True)
    available_video_resolution = check_availablevideo_resolution(streams)
    is_audio_available = streams.get_audio_only()
    if available_video_resolution != None and is_audio_available != None:
        update.message.reply_text(
            text=static_text.choose_quality_text, 
            reply_markup=keyboards.make_keyboard_ask_quality(available_video_resolution)
        )
    else:
        update.message.reply_text(text=static_text.video_is_unavailable)
        return ConversationHandler.END
    # low_audio = yt.streams.get_audio_only().download(output_path=DOWNLOAD_DIRECTORY)
    return conversation_state.PUT_URL_STATE

def check_availablevideo_resolution(streams: pytube.YouTube) -> list:
    RESOLUTION = ["720p", "480p", "360p", "240p", "144p"]
    available_video_resolution = []
    for res in RESOLUTION: 
        does_exist = streams.get_by_resolution(res)
        if does_exist != None:
            available_video_resolution.append(res)
    context.user_data["video_resolution"] = available_video_resolution
    return available_video_resolution

def download(update: Update, context: CallbackContext):
    try:
        yt.streams.get_highest_resolution().download(output_path=DOWNLOAD_DIRECTORY)
    except:
        update.message.reply_text(static_text.video_is_unavailable)
    return conversation_state.PUT_URL_STATE

def callback_for_audio_download(stream: pytube.YouTube, path_to_audio: Path, update: Update):
    update.message.reply_text(static_text.download_is_sucessful_text)
    with open(path_to_audio, 'rb') as audio:
        update.message.reply_audio(audio)
    os.remove(path_to_audio)
    return ConversationHandler.END 

def callback_for_video_download(stream: pytube.YouTube, path_to_video: Path, update: Update):
    update.message.reply_text(static_text.download_is_sucessful_text)
    with open(path_to_video, 'rb') as video:
        update.message.reply_video(video)
    os.remove(path_to_video)
    return ConversationHandler.END 


def not_youtube_domain(update: Update, context: CallbackContext):
    update.message.reply_text(text=static_text.not_youtube_domain_text)
    return conversation_state.PUT_URL_STATE

def ask_format(update: Update, context: CallbackContext):
    pass


def stop(update: Update, context: CallbackContext):
    context.user_data.clear()
    ConversationHandler.END