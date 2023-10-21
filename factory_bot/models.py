from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class TelegramUser(User):
    name = models.CharField(validators=[RegexValidator(r'^[a-zA-Z]+$')])


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_sent = models.DateTimeField(auto_now_add=True)
    message_text = models.TextField()
