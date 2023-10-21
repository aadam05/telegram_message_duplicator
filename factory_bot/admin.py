from django.contrib import admin
from . import models


@admin.register(models.TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'name',
    ]


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'date_sent',
        'message_text',
    ]
