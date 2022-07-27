import sys
import logging
from typing import Dict

import telegram.error
from telegram import Update, BotCommand

from telegram.ext import (
    Updater, Dispatcher,
    CommandHandler, Filters,
    MessageHandler, ConversationHandler,
    CallbackQueryHandler, BaseFilter,
    CallbackContext
)

from tgbot.handlers.utils import error
from tgbot.handlers.start_handler import handler as start_handler

from tgbot.handlers.download_handler import handler as download_handler
from tgbot.handlers.download_handler import conversation_state as download_cs
from tgbot.handlers.download_handler import static_text as download_st

from tgbot.handlers.search_handler import conversation_state as search_cs
from tgbot.handlers.search_handler import handler as search_handler

from tgbot.handlers.channel_handler import conversation_states as channel_cs
from tgbot.handlers.channel_handler import handler as channel_handler

VIDEO_RESOLUTION_FORMATS = [
    "144p", "360p", "240p", "480p", "720p", "1080p"
]

def setup_dispatcher(dp):
    dp.add_handler(
        CommandHandler("start", start_handler.command_start)
    )

    dp.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler("download", download_handler.ask_put_url)
            ], 
            states={
                download_cs.PUT_URL_STATE: [
                    MessageHandler(
                        Filters.regex(r'^https:\/\/youtube\.com\/.*'), 
                        download_handler.extract_video_format_and_quality
                    ),
                    MessageHandler(
                        Filters.regex(r'^https:\/\/m\.youtube\.com\/.*'), 
                        download_handler.extract_video_format_and_quality
                    ),
                    MessageHandler(
                        Filters.regex(r'^https:\/\/youtu\.be\/.*'), 
                        download_handler.extract_video_format_and_quality
                    ),
                    MessageHandler(Filters.all & ~Filters.command, download_handler.not_youtube_domain)
                ],
                download_cs.ASK_QUALITY_FOR_PLAYLIST_STATE: [
                    MessageHandler(
                        Filters.text(download_st.GET_AUDIO_BUTTON), 
                        download_handler.download_playlist_videos,
                        run_async=True
                    ),
                    MessageHandler(
                        Filters.text(download_st.GET_HIGHEST_RESOLUTION_BUTTON), 
                        download_handler.download_playlist_videos,
                        run_async=True
                    ),
                    MessageHandler(Filters.text(
                        download_st.GET_LOWEST_RESOLUTION_BUTTON), 
                        download_handler.download_playlist_videos,
                        run_async=True
                    ),
                    MessageHandler(Filters.all, download_handler.resolution_is_required)
                ],
                download_cs.ASK_QUALITY_STATE: [
                    MessageHandler(Filters.text(VIDEO_RESOLUTION_FORMATS), download_handler.download),
                    MessageHandler(Filters.regex(r'^Аудио$'), download_handler.download),
                    MessageHandler(Filters.all, download_handler.resolution_is_required)
                ]
            }, 
            fallbacks=[
                MessageHandler(Filters.command, download_handler.stop)
            ]
        )
    )

    dp.add_handler(ConversationHandler(
            entry_points=[
                CommandHandler("search", search_handler.ask_query)
            ], 
            states={
                search_cs.GET_SEARCH_QUERY_STATE: [
                    MessageHandler(Filters.text, search_handler.search_by_query)
                ],
                search_cs.ASK_QUALITY_AND_FORMAT_BY_SEARCH_STATE: [
                    CallbackQueryHandler(search_handler.ask_format_and_quality, run_async=True)
                ],
            }, 
            fallbacks=[
                MessageHandler(Filters.command, search_handler.stop)
            ], 
        )
    )

    dp.add_handler(ConversationHandler(
            entry_points=[
                CommandHandler("channel", channel_handler.ask_channel)
            ], 
            states={
                channel_cs.SEND_CHANNEL_STATE: [
                    MessageHandler(
                        Filters.regex(r'^https:\/\/youtube\.com\/.*'), 
                        channel_handler.extract_channel_video
                    ),
                    MessageHandler(
                        Filters.regex(r'^https:\/\/m\.youtube\.com\/.*'), 
                        channel_handler.extract_channel_video
                    ),
                    MessageHandler(
                        Filters.regex(r'^https:\/\/youtu\.be\/.*'), 
                        channel_handler.extract_channel_video
                    ),
                    MessageHandler(Filters.all & ~Filters.command, download_handler.not_youtube_domain)
                ],
                channel_cs.ASK_QUALITY_CHANNEL_VIDEO: [

                ]
            }, 
            fallbacks=[
                MessageHandler(Filters.command, search_handler.stop)
            ]
        )
    )

    dp.add_error_handler(error.sent_tracebak_into_chat)
    return dp

