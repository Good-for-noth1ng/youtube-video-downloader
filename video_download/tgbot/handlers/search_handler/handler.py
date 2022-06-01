import re
import os
from pathlib import Path
from functools import partial
from typing import Dict

from telegram import ParseMode, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler

from  pytube import YouTube, Search

from tgbot.handlers.search_handler import conversation_state 
from tgbot.handlers.search_handler import static_text as search_st
from tgbot.handlers.search_handler import keyboards

from tgbot.handlers.download_handler import handler as download_handler
from tgbot.handlers.download_handler import static_text as download_st  
from tgbot.handlers.utils.const import DOWNLOAD_DIRECTORY
from tgbot.handlers.utils.change_type import to_dict, to_str

def ask_query(update: Update, context: CallbackContext):
    update.message.reply_text(text=search_st.put_query)
    return conversation_state.GET_SEARCH_QUERY_STATE


def get_video_length(length_in_seconds: int) -> str:
    return f"{length_in_seconds // 60} минут {length_in_seconds -  ((length_in_seconds // 60) * 60)} секунд"


def search_by_query(update: Update, context: CallbackContext):
    query = update.message.text
    search = Search(query)
    results = search.results
    for result in results:
        try:
            video_id = result.vid_info['videoDetails']['videoId']
        except KeyError:
            continue
        video_title = result.title
        video_author = result.author
        video_length = get_video_length(result.length)
        message_text = f"🧑 {video_author}: ▶️ {video_title}, 🕐 {video_length}"
        update.message.reply_text(
            text=message_text, 
            reply_markup=keyboards.make_keyboard_to_ask_video(video_id=video_id)
        )
    return conversation_state.ASK_QUALITY_AND_FORMAT_BY_SEARCH_STATE


def is_resolution(query_data: str) -> bool:
    regex = re.compile(r"^\d\d\dp$")
    match = regex.match(query_data)
    if match:
        return True
    else:
        return False


def ask_format_and_quality(update: Update, context: CallbackContext):
    query = update.callback_query
    query_data = query.data
    query.answer()
    query_data = to_dict(query_data)
    if query_data["resolution"] == download_st.GET_AUDIO_BUTTON:
        update.callback_query.edit_message_text(text=download_st.download_started)
        video_id = query_data["video_id"]
        url = f"https://youtube.com/watch?v={video_id}"
        title, author = download_handler.get_author_and_title(url)
        yt = YouTube(
            url=url, 
            on_complete_callback=partial(
                callback_for_audio_download, 
                update=update, 
                query_data=query_data,
                author=author,
                title=title
            )
        )
        yt.streams.get_audio_only().download(output_path=DOWNLOAD_DIRECTORY)
    elif is_resolution(query_data["resolution"]):
        update.callback_query.edit_message_text(text=download_st.download_started)
        video_id = query_data["video_id"]
        url = f"https://youtube.com/watch?v={video_id}"
        yt = YouTube(url=url, on_complete_callback=partial(callback_for_video_download, update=update))
        yt.streams.get_by_resolution(query_data["resolution"]).download(output_path=DOWNLOAD_DIRECTORY)
    else:
        video_id = query_data["video_id"]
        url = f"https://youtube.com/watch?v={video_id}"
        available_resolution = download_handler.check_available_video_resolution(url=url)
        update.callback_query.edit_message_text(
            text=download_st.choose_quality_text, 
            reply_markup=keyboards.make_inline_keyboard_ask_quality(available_resolution, query_data)
        )
    return conversation_state.ASK_QUALITY_AND_FORMAT_BY_SEARCH_STATE


def callback_for_audio_download(stream: YouTube, path_to_audio: Path, update: Update, query_data: Dict, author, title):
    update.callback_query.edit_message_text(text=download_st.download_is_sucessful_text)
    with open(path_to_audio, 'rb') as audio:
        update.callback_query.message.reply_audio(
            audio, 
            performer=author, 
            title=title
        )
    os.remove(path_to_audio) 


def callback_for_video_download(stream: YouTube, path_to_video: Path, update: Update):
    update.callback_query.edit_message_text(text=download_st.download_is_sucessful_text)
    with open(path_to_video, 'rb') as video:
        update.callback_query.message.reply_video(video)
    os.remove(path_to_video)


def stop(update: Update, context: CallbackContext):
    context.user_data.clear()
    return ConversationHandler.END