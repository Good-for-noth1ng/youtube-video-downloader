import logging
import traceback
import html

import telegram
from telegram import Update
from telegram.ext import CallbackContext

from pytube.exceptions import VideoPrivate, VideoRegionBlocked, VideoUnavailable, MembersOnly

from tgbot.models import User
from video_download.settings import TELEGRAM_LOGS_CHAT_ID

def sent_tracebak_into_chat(update: Update, context: CallbackContext):
    u = User.get_user(update, context)

    logging.error("Exception while handling an update:", exc_info=context.error)

    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    if context.error == VideoPrivate:
        user_message = "Видео приватное"
    elif context.error == VideoRegionBlocked:
        user_message = "Из этого региона видео недоступно"
    elif context.error == MembersOnly:
        user_message = "Это видео только для участников сообщества"
    elif context.error == VideoUnavailable:
        user_message = "Видео недоступно"
    else:
        user_message = """
            😔 Что-то пошло не так.
            Вся информация по ошибке получена, скоро всё будет исправлено.
            Вернуться: /start
        """
    context.bot.send_message(
        chat_id=u.user_id,
        text=user_message,
    )

    admin_message = f"⚠️⚠️⚠️ for {u.tg_str}:\n{message}"[:4090]
    if TELEGRAM_LOGS_CHAT_ID:
        context.bot.send_message(
            chat_id=TELEGRAM_LOGS_CHAT_ID,
            text=admin_message,
            parse_mode=telegram.ParseMode.HTML,
        )
    else:
        logging.error(admin_message)
