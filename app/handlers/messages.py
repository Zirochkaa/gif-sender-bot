from aiogram import types

from app.bot import dp
from app.config import settings
from app.loggers import handlers_messages_log as logger


@dp.message_handler()
async def all_text(message: types.Message):
    logger.error(f"message:\n{message}\n---")

    if message.from_user.username in settings.telegram_usernames:
        with open(f"app/media/gif.mp4", "rb") as f:
            await message.reply_document(document=f)
