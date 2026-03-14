from core.models import TelegramMessage, MessageVideo, UserCabinet


class MessageRepository:
    """Repository for managing TelegramMessage and related data."""
    
    async def create_message(self, message_id: int, channel_id: int, text: str = None) -> TelegramMessage:
        """Creates a new TelegramMessage record."""
        message = TelegramMessage.objects.create(
            message_id=message_id,
            channel_id=channel_id,
            text=text
        )
        return message
    
    def create_messages(self, messages_data: list) -> list:
        """Creates multiple TelegramMessage records."""
        messages = [TelegramMessage(**data) for data in messages_data]
        TelegramMessage.objects.bulk_create(messages, ignore_conflicts=True)
        return messages
