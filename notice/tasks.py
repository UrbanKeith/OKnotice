from celery import shared_task
from django.utils import timezone

from OKnotice.settings import BOT
from notice.models import Message, MessageStatus, Recipient, Chat


@shared_task()
def check_message():
    """
    Проверяет отложенные сообщения и отправляет не отправленые сообщения
    """
    pending_message = Message.objects.prefetch_related('recipients').filter(status=MessageStatus.PENDING,
                                                                            send_date__lte=timezone.now())
    for message in pending_message:
        send_message.delay(message)


@shared_task()
def send_message(message: Message):
    """
    Функция отправки сообщения
    """
    if not message:
        return
    recipients = message.recipients.values_list('user_id', flat=True)
    is_sending = BOT.send_mailing_message(recipients, message.text)
    if not is_sending:
        message.status = MessageStatus.ERROR
        print('Ошибка при отправке сообщения "{}". Плановая отправка в {}'.format(message.text, str(message.send_date)))
    else:
        message.status = MessageStatus.SEND
    message.save()


@shared_task()
def check_recipients():
    """
    Проверка новых участников группы. Проверяет список индивидуальных чатов в группе и сохраняет новых пользователей
    """
    recipients_list = Recipient.objects.values_list('user_id', flat=True)

    chats_list = BOT.get_all_chat_info()
    for chat in chats_list:
        if chat.get('type') == "GROUP_CHAT" and chat.get('owner_id') not in recipients_list:

            chat_entry = Chat.objects.get_or_create(chat_id=chat.get('chat_id'),
                                                    defaults={'url': BOT.get_chat_url(chat.get('chat_id'))})

            user_id = chat.get('owner_id')
            Recipient.objects.create(user_id=user_id,
                                     url='/'.join(['https://ok.ru/profile/', user_id.split(':')[-1]]),
                                     chat=chat_entry)

