import asyncio

from django.conf import settings
from loguru import logger
from telethon import TelegramClient
from telethon.sessions import StringSession

from tg_messages.managers.message_manager import MessageManager


async def get_messages(channel_url):
    """
    Iterates a Telegram channel, finds videos, and saves their t.me links without downloading.
    """
    try:
        async with TelegramClient(
            StringSession(settings.TELEGRAM_SESSION_NAME),
            settings.TELEGRAM_API_ID,
            settings.TELEGRAM_API_HASH
        ) as client:
        
            if not await client.is_user_authorized():
                logger.error("Telegram client is not authorized. Please ensure the session is set up correctly.")
                return
            
            # 1. Обов'язково завантажуємо діалоги, щоб Telethon "пізнав" канал
            dialogs = await client.get_dialogs()
            
            # 2. Шукаємо потрібний канал у списку діалогів за ID
            target_entity = None
            for dialog in dialogs:
                if dialog.id == int(channel_url):
                    target_entity = dialog.entity
                    break
            
            if not target_entity:
                logger.error(f"Канал з ID {channel_url} не знайдено у ваших діалогах.")
                return

            messages_to_create = []
            manager = MessageManager()
            total_processed = 0
            while total_processed < 100:
                async for message in client.iter_messages(target_entity, limit=10):
                    # process each message
                    processed_message = manager.process_message(message.to_dict())
                    messages_to_create.append(processed_message)
                    if message.media and message.media.type == 'video':
                        print(f"Video found: {message.link}")  # Prints the t.me link
                    total_processed += 1
            manager.create_messages(messages_to_create)

    except Exception as e:
        print(f"An error occurred: {e}")


async def get_channels():
    """
    Placeholder function to list Telegram channels. Implement as needed.
    """
    try:
        async with TelegramClient(
            StringSession(settings.TELEGRAM_SESSION_NAME),
            settings.TELEGRAM_API_ID,
            settings.TELEGRAM_API_HASH
        ) as client:
            if not await client.is_user_authorized():
                logger.error("Telegram client is not authorized. Please ensure the session is set up correctly.")
                return
            channel_names = []
            dialogs = await client.get_dialogs(limit=10000)
            for dialog in dialogs:
                entity = dialog.entity
                # Create the link: use username if available, otherwise the ID
                if getattr(entity, 'username', None):
                    url = f"https://t.me/{entity.username}"
                else:
                    url = f"https://t.me/c/{entity.id}" # Private channel format
                
                channel_names.append({
                    "name": dialog.name,
                    "url": url,
                    "id": dialog.id
                })
            return channel_names
    except Exception as e:
        print(f"An error occurred while listing channels: {e}")