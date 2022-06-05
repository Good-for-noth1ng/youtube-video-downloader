import sys
import logging
from typing import Dict

import telegram.error
from telegram import Bot, Update, BotCommand
from telegram.ext import (
    Updater, Dispatcher,
    CommandHandler, Filters,
    MessageHandler, ConversationHandler,
    CallbackQueryHandler, BaseFilter,
    CallbackContext
)
from video_download.settings import PORT, HEROKU_APP_NAME, TELEGRAM_TOKEN, DEBUG
from tgbot.handlers.utils import error
from tgbot.handlers.start_handler import handler as start_handler

from tgbot.handlers.download_handler import handler as download_handler
from tgbot.handlers.download_handler import conversation_state as download_cs
from tgbot.handlers.download_handler import static_text as download_st

from tgbot.handlers.search_handler import conversation_state as search_cs
from tgbot.handlers.search_handler import handler as search_handler

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
                        Filters.regex(r'^https:\/\/m.youtube\.com\/.*'), 
                        download_handler.extract_video_format_and_quality
                    ),
                    MessageHandler(
                        Filters.regex(r'^https:\/\/youtu.be\/.*'), 
                        download_handler.extract_video_format_and_quality
                    ),
                    MessageHandler(Filters.all, download_handler.not_youtube_domain)
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

    dp.add_error_handler(error.sent_tracebak_into_chat)
    return dp

def run_pooling():
    """ Run bot in pooling mode """
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    #Run with webhook
    # updater.start_webhook(
    #     listen="0.0.0.0", 
    #     port=PORT, 
    #     url_path=TELEGRAM_TOKEN,
    #     webhook_url='https://' + HEROKU_APP_NAME +'.herokuapp.com/' + TELEGRAM_TOKEN
    # )
    
    #Run in pooling mode
    bot_info = Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/" + bot_info["username"]
    print(f"Pooling of '{bot_link}' started")
    updater.start_polling()

    updater.idle()

bot = Bot(TELEGRAM_TOKEN)

try:
    TELEGRAM_BOT_USERNAME = bot.get_me()["username"]
except telegram.error.Unauthorized:
    logging.error(f"Invalid telegram token")
    sys.exit(1)

# @app.task(ignore_result=True)
# def process_telegram_event(update_json):
#     update = Update.de_json(update_json, bot)
#     dispatcher.process_update(update)

def set_up_commands(bot_instance: Bot) -> None:
    langs_with_commands: Dict[str, Dict[str, str]] = {
        'en': {
            'start': 'Bot informations 🚀',
            'download': 'Download video 🕹️',
            'search': 'Search for video 🔍'
        },
        'ru': {
            'start': 'Узнать о боте 🚀',
            'download': 'Скачать видео 🕹️',
            'search': 'Найти видео 🔍'
        }
    }
    
    bot_instance.delete_my_commands()
    language_code='ru'
    bot_instance.set_my_commands(
        language_code=language_code,
        commands=[
            BotCommand(command, description) for command, description in langs_with_commands[language_code].items()
        ]
    )


# WARNING: it's better to comment the line below in DEBUG mode.
# Likely, you'll get a flood limit control error, when restarting bot too often
set_up_commands(bot)

n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))