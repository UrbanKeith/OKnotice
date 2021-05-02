from datetime import datetime

from main_ok.models import Recipient, Chat, ChatStatus, RecipientStatus, Message, MessageStatus
from OKBot.bot import OKBot


def check_recipients(bot: OKBot):
    """
    Проверка новых участников группы. Проверяет список индивидуальных чатов в группе и сохраняет новых пользователей
    """
    recipients_list = Recipient.objects.values_list('user_id', flat=True)

    chats_list = bot.get_all_chat_info()
    for chat in chats_list:
        if chat.get('type') == "GROUP_CHAT" and chat.get('owner_id') not in recipients_list:

            chat_entry = Chat.objects.get_or_create(chat_id=chat.get('chat_id'),
                                                    defaults={'url': bot.get_chat_url(chat.get('chat_id'))})

            user_id = chat.get('owner_id')
            Recipient.objects.create(user_id=user_id,
                                     url='/'.join(['https://ok.ru/profile/', user_id.split(':')[-1]]),
                                     chat=chat_entry)


def check_pending_message(bot: OKBot):
    """
    Проверка отложенных сообщений. Проверяет сообщения на наличие сообщение со статусом PENDING
    Если  находит сообщения с превышенной датой ожидания, отправляет их
    """
    message_list = Message.objects.filter(status=MessageStatus.PENDING, send_date__lte=datetime.now())
    if message_list.count():
        for message in message_list:
            user_list = Recipient.objects.filter(status=RecipientStatus.ACTIVE).values_list('user_id', flat=True)
            is_not_send = bot.send_mailing_message(user_list, message.text)
            if is_not_send:
                message.status = MessageStatus.ERROR
            else:
                message.status = MessageStatus.SEND
            message.save()
