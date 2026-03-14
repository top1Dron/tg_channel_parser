from core.models import TelegramMessage
from tg_messages.repositories.message_repository import MessageRepository


class MessageManager:
    def __init__(self):
        self.message_repository = MessageRepository()
        
    
    def process_message(self, message_data: dict) -> TelegramMessage | None:
        """Processes a message and saves it to the database."""
        # Here you can add any additional processing logic if needed
        return TelegramMessage(
            message_id=message_data.get("id"),
            channel_id=message_data.get("peer_id", {}).get("channel_id"),
            text=message_data.get("message")
        )
    
    def create_messages(self, messages_data: list[TelegramMessage]):
        """Creates multiple TelegramMessage instances in the database."""
        self.message_repository.create_messages(messages_data)