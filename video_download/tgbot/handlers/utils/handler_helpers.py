from telegram import ParseMode, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler

from tgbot.handlers.utils import keyboards

def get_video_length(length_in_seconds: int) -> str:
    return f"{length_in_seconds // 60} минут {length_in_seconds -  ((length_in_seconds // 60) * 60)} секунд"

def init_video_params(video, update):
    video_title = video.title
    video_author = video.author
    video_length = get_video_length(video.length)
    message_text = f"🎥 {video_author}: ▶️ {video_title}, 🕐 {video_length}"
    update.message.reply_text(
        text=message_text, 
        reply_markup=keyboards.make_keyboard_to_ask_video(video_id=video_id)
    )

def ask_format_and_quality_by_query(update: Update, context: CallbackContext):
    query = update.callback_query
    query_data = query.data
    query.answer()
    query_data = to_dict(query_data)
    if query_data["resolution"] == download_st.GET_AUDIO_BUTTON:
        context.dispatcher.run_async(partial(start_audio_download, update, query_data))
    elif is_resolution(query_data["resolution"]):
        context.dispatcher.run_async(partial(start_video_download, update, query_data))
    else:
        context.dispatcher.run_async(partial(get_available_resolution, update, query_data), update=update)