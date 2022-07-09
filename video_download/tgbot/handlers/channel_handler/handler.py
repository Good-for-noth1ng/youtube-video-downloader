from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler 

from youtube_crawler.pytube.contrib.channel import Channel

import tgbot.handlers.channel_handler.static_text as st
import tgbot.handlers.channel_handler.conversation_states as cs
from tgbot.handlers.search_handler.handler import get_video_length
from tgbot.handlers.search_handler import keyboards as search_keyboards

def ask_channel(update: Update, context: CallbackContext):
    update.message.reply_text(st.send_chanel_url_text)
    return cs.SEND_CHANNEL_STATE

def extract_channel_video(update: Update, context: CallbackContext):
    url: str = update.message.text
    channel = Channel(url)
    for video in channel.videos:
        video_id = video.video_id
        author = video.author
        title = video.title
        video_length = get_video_length(length_in_seconds=video.length)
        message_text = f"🎥 {author}: ▶️ {title}, 🕐 {video_length}"   
        update.message.reply_text(
            text=message_text, 
            reply_markup=search_keyboards.make_keyboard_to_ask_video(video_id)
        )
    return cs.ASK_QUALITY_CHANNEL_VIDEO     
    
