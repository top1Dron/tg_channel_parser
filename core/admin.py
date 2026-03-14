from django.contrib import admin

from .models import TelegramMessage, MessageVideo, UserCabinet


@admin.register(TelegramMessage)
class TelegramMessageAdmin(admin.ModelAdmin):
    list_display = ("message_id", "channel_id", "effective_year", "created_at", "is_processed")
    list_filter = ("detected_year", "manual_year", "is_processed")
    search_fields = ("message_id", "text")


@admin.register(MessageVideo)
class MessageVideoAdmin(admin.ModelAdmin):
    list_display = ("message_id", "video_url")
    search_fields = ("video_url",)


@admin.register(UserCabinet)
class UserCabinetAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username",)
