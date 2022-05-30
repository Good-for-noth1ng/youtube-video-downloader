from  pytube import YouTube, Search
from telegram import ParseMode, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler

from tgbot.handlers.search_handler import conversation_state 
from tgbot.handlers.search_handler import static_text
from tgbot.handlers.search_handler import keyboards

from tgbot.handlers.download_handler import handler as download_handler

def ask_query(update: Update, context: CallbackContext):
    update.message.reply_text(text=static_text.put_query)
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

def ask_format_and_quality(update: Update, context: CallbackContext):
    video_id = update.callback_query['data']
    url = f"https://youtube.com/watch?v={video_id}"
    download_handler.ask_video_format_and_quality(url=url, update=update, context=context)
    return conversation_state.DOWNLOAD_BY_SEARCH_STATE

def stop(update: Update, context: CallbackContext):
    return ConversationHandler.END