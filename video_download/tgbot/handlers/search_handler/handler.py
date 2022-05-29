from  pytube import YouTube, Search
from telegram import ParseMode, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler

from tgbot.handlers.search_handler import conversation_state 
from tgbot.handlers.search_handler import static_text
from tgbot.handlers.search_handler import keyboards

def ask_query(update: Update, context: CallbackContext):
    update.message.reply_text(text=static_text.put_query)
    return conversation_state.GET_SEARCH_QUERY_STATE

def search_by_query(update: Update, context: CallbackContext):
    query = update.message.text
    search = Search(query)
    results = search.results
    for result in results:
        video_title = f"{result.title}"
        update.message.reply_text(
            text=video_title, 
            reply_markup=keyboards.make_keyboard_to_ask_video(youtube_object=result)
        )
    return conversation_state.GET_SEARCH_QUERY_STATE

def download(update: Update, context: CallbackContext):
    print(update.callback_query)

def stop(update: Update, context: CallbackContext):
    return ConversationHandler.END