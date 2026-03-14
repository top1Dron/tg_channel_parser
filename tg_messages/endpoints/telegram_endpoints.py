from fastapi import APIRouter
from fastapi import HTTPException
from loguru import logger

from tg_messages.api_clients.telegram_parser import get_channels, get_messages  # Import the function

telegram_router = APIRouter(prefix="/messages", tags=["messages"])


@telegram_router.get("/saved-messages")
async def list_videos(channel_url: str):
    """Lists videos from a Telegram channel."""
    try:
        await get_messages(channel_url)
        return {"message": "Video links retrieved successfully."}  # Or return the actual video links if you modify get_video_links
    except Exception as e:
        logger.error("Error retrieving video links: {error}", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@telegram_router.get("/list-channels")
async def list_channels():
    """Lists Telegram channels. Placeholder for actual implementation."""
    try:
        # Placeholder: Implement logic to list channels if needed
        return {"channels": await get_channels()}  # Return an empty list or actual channels if implemented
    except Exception as e:
        logger.error("Error listing channels: {error}", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))