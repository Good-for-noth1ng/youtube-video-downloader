import os
from pathlib import Path
from functools import partial
from typing import List, Dict, Tuple

from youtube_crawler.pytube.__main__ import YouTube
from youtube_crawler.pytube.contrib.playlist import Playlist
from telegram import ParseMode, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler


import tgbot.handlers.download_handler.conversation_state as conversation_state
import tgbot.handlers.download_handler.static_text as static_text
import tgbot.handlers.download_handler.keyboards as keyboards
from tgbot.handlers.utils.const import DOWNLOAD_DIRECTORY


def ask_put_url(update: Update, context: CallbackContext) -> str:
    update.message.reply_text(
        text=static_text.send_url_text, 
    )
    return conversation_state.PUT_URL_STATE

def is_playlist(url):
    if len(url) > 50:
        return True
    else:
        return False

def extract_video_format_and_quality(update: Update, context: CallbackContext) -> str:
    url: str = update.message.text
    if is_playlist(url):
        context.user_data["playlist_url"] = url
        update.message.reply_text(
            text=static_text.choose_res_for_playlist_text, 
            reply_markup=keyboards.make_keyboard_ask_quality_for_playlist()
        )
        return conversation_state.ASK_QUALITY_FOR_PLAYLIST_STATE
    else:
        context.user_data["url"] = url
        available_video_resolution = check_available_video_resolution(url)
        update.message.reply_text(
            text=static_text.choose_quality_text, 
            reply_markup=keyboards.make_keyboard_ask_quality(available_video_resolution)
        )
        return conversation_state.ASK_QUALITY_STATE

    
def check_available_video_resolution(url: str) -> List[str]:
    available_video_resolution = []
    yt = YouTube(url=url)
    streams = yt.streams.filter(progressive=True).all()
    for stream in streams:
        if yt.streams.get_by_resolution(stream.resolution) is not None:
            available_video_resolution.append(stream.resolution)
    return available_video_resolution

def download_playlist_videos(update: Update, context: CallbackContext):
    resolution = update.message.text
    playlist_url = context.user_data["playlist_url"]
    playlist = Playlist(playlist_url)
    for url in playlist.video_urls:
        try:
            if resolution == static_text.GET_AUDIO_BUTTON:
                yt = YouTube(url=url, on_complete_callback=partial(callback_for_audio_download, update=update, url=url))
                yt.streams.get_audio_only().download(output_path=DOWNLOAD_DIRECTORY)
            elif resolution == static_text.GET_LOWEST_RESOLUTION_BUTTON:
                yt = YouTube(url=url, on_complete_callback=partial(callback_for_video_download, update=update))
                yt.streams.get_lowest_resolution.download(output_path=DOWNLOAD_DIRECTORY)
            elif resolution == static_text.GET_HIGHEST_RESOLUTION_BUTTON:
                yt = YouTube(url=url, on_complete_callback=partial(callback_for_video_download, update=update))
                yt.streams.get_highest_resolution.download(output_path=DOWNLOAD_DIRECTORY)
        except Exception as e:
            update.message.reply_text(static_text.video_is_unavailable)
            continue
    update.message.reply_text(text=static_text.all_playlist_is_downloaded_text, reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END


def get_author_and_title(url: str) -> Tuple[str, str]:
    yt = YouTube(url)
    return yt.author, yt.title


def download(update: Update, context: CallbackContext):
    resolution = update.message.text
    url = context.user_data["url"]
    update.message.reply_text(text=static_text.download_started, reply_markup=ReplyKeyboardRemove())
    try:
        if resolution == static_text.GET_AUDIO_BUTTON:
            yt = YouTube(url=url, on_complete_callback=partial(callback_for_audio_download, update=update, url=url))
            yt.streams.get_audio_only().download(output_path=DOWNLOAD_DIRECTORY)
        else:
            yt = YouTube(url=url, on_complete_callback=partial(callback_for_video_download, update=update))
            yt.streams.get_by_resolution(resolution).download(output_path=DOWNLOAD_DIRECTORY)
    except:
        update.message.reply_text(static_text.video_is_unavailable)
    finally:
        context.user_data.clear()
        return ConversationHandler.END 


def callback_for_audio_download(stream: YouTube, path_to_audio: Path, update: Update, url: str):
    update.message.reply_text(text=static_text.download_is_sucessful_text)
    author, title = get_author_and_title(url)
    with open(path_to_audio, 'rb') as audio:
        update.message.reply_audio(audio, performer=author, title=title)
    os.remove(path_to_audio)
    return ConversationHandler.END 


def callback_for_video_download(stream: YouTube, path_to_video: Path, update: Update):
    update.message.reply_text(text=static_text.download_is_sucessful_text)
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
    return ConversationHandler.END