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
    context.user_data["url"] = url
    available_video_resolution = check_available_video_resolution(url)
    update.message.reply_text(
        text=static_text.choose_quality_text, 
        reply_markup=keyboards.make_keyboard_ask_quality(available_video_resolution)
    )
    return conversation_state.ASK_QUALITY_STATE
    # yt = pytube.YouTube(url=url)
    # yt = pytube.YouTube(url=url, on_complete_callback=partial(callback_for_audio_download, update=update))
    
    
    # is_audio_available = streams.get_audio_only()
    # if available_video_resolution != None and is_audio_available != None:
    #     update.message.reply_text(
    #         text=static_text.choose_quality_text, 
    #         reply_markup=keyboards.make_keyboard_ask_quality(available_video_resolution)
    #     )
    # else:
    #     update.message.reply_text(text=static_text.video_is_unavailable)
    #     return ConversationHandler.END


    # low_audio = yt.streams.get_audio_only().download(output_path=DOWNLOAD_DIRECTORY)
    # return conversation_state.PUT_URL_STATE

def check_available_video_resolution(url: str) -> list:
    available_video_resolution = []
    yt = pytube.YouTube(url=url)
    streams = yt.streams.filter(progressive=True).all()
    for stream in streams:
        available_video_resolution.append(stream.resolution)
    return available_video_resolution

def download(update: Update, context: CallbackContext):
    resolution = update.message.text
    url = context.user_data["url"]
    try:
        if resolution == static_text.GET_AUDIO_BUTTON:
            yt = pytube.YouTube(url=url, on_complete_callback=partial(callback_for_audio_download, update=update))
            yt.streams.get_audio_only().download(output_path=DOWNLOAD_DIRECTORY)
        else:
            yt = pytube.YouTube(url=url, on_complete_callback=partial(callback_for_video_download, update=update))
            yt.streams.get_by_resolution(resolution).download(output_path=DOWNLOAD_DIRECTORY)
        return ConversationHandler.END
    except Exception as e:
        update.message.reply_text(static_text.video_is_unavailable)
        print(e)
        return ConversationHandler.END

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

def resolution_is_required(update: Update, context: CallbackContext):
    update.message.reply_text(text=static_text.not_youtube_domain_text)
    return conversation_state.ASK_QUALITY_STATE

def stop(update: Update, context: CallbackContext):
    context.user_data.clear()
    ConversationHandler.END