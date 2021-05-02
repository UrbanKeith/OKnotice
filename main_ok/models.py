from django.db import models


class MessageStatus(models.IntegerChoices):
    PENDING = 1
    SEND = 2
    REJECTED = 3
    ERROR = 4


class RecipientStatus(models.IntegerChoices):
    ACTIVE = 1
    REFUSAL = 2


class ChatStatus(models.IntegerChoices):
    ACTIVE = 1
    IGNORE = 2


class Chat(models.Model):
    """
    Модель для сохранения статусов
    """
    chat_id = models.CharField(max_length=50)
    url = models.URLField()
    status = models.PositiveIntegerField(choices=ChatStatus, default=ChatStatus.ACTIVE)


class Recipient(models.Model):
    """
    Модель для сохранения пользователей
    """
    user_id = models.CharField(max_length=50)
    url = models.URLField()
    chat = models.ForeignKey(Chat, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.PositiveIntegerField(choices=RecipientStatus, default=RecipientStatus.ACTIVE)


class Message(models.Model):
    """
    Модель для сохранения сообщений
    """
    text = models.CharField(max_length=1500)
    status = models.PositiveIntegerField(choices=MessageStatus, default=MessageStatus.PENDING)
    send_date = models.DateTimeField()

