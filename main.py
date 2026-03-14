import os

import django
from fastapi import FastAPI

# 1. Set the environment variable to your project's settings
# Replace 'config.settings' with the actual path to your settings.py (e.g., 'myproject.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 2. Initialize Django
django.setup()

# 3. NOW you can safely import your routers/models
from tg_messages.endpoints.telegram_endpoints import telegram_router
from users.endpoints import user_router

app = FastAPI()


app.include_router(telegram_router)
app.include_router(user_router)

@app.get("/")
async def root():
    return {"status": "FastAPI is running with Django ORM"}