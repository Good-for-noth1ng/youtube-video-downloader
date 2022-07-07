from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler 

from youtube_crawler.pytube.contrib.channel import Channel

import tgbot.handlers.channel_handler.static_text as st
import tgbot.handlers.channel_handler.conversation_states as cs

def ask_channel(update: Update, context: CallbackContext):
    update.message.reply_text(st.send_chanel_url_text)
    return cs.SEND_CHANNEL_STATE

def extract_channel_video(update: Update, context: CallbackContext):
    url: str = update.message.text
    channels = Channel(url)
    for channel in channels:
        pass
