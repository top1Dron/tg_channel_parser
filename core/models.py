
from django.db import models
from django.contrib.auth.models import User


class TelegramMessage(models.Model):
    message_id = models.CharField(max_length=255, unique=True)
    channel_id = models.CharField()
    text = models.TextField(blank=True, null=True)
    detected_year = models.IntegerField(null=True, blank=True)
    manual_year = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    @property
    def effective_year(self):
        return self.manual_year if self.manual_year else self.detected_year

    def __str__(self):
        return f"Msg {self.message_id} - {self.effective_year}"


class MessageVideo(models.Model):
    message = models.ForeignKey(TelegramMessage, related_name='videos', on_delete=models.CASCADE)
    # For private channels, use the 't.me/c/12345/678' format
    # Note: 12345 is the stripped channel ID (remove -100 prefix)
    video_url = models.URLField(max_length=500)
    thumbnail_url = models.URLField(max_length=500, null=True, blank=True)


class UserCabinet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    checked_messages = models.ManyToManyField(TelegramMessage, related_name="checked_by")

    def __str__(self):
        return f"Cabinet for {self.user.username}"

