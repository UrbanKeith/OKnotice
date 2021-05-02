import requests


class OKBot:
    main_url = 'https://api.ok.ru/graph'
    access_token = None

    def __init__(self, access_token):
        self.access_token = access_token

    def get_all_chat_info(self):
        """
        Получение информации о всех чатах
        """
        url = '/'.join([self.main_url, 'me/chats'])
        response = requests.get(url, params=self.access_param())
        return response.json()

    def get_chat_url(self, chat_id):
        """
        Возвращает нормальизированный url на чат
        """
        url = '/'.join([self.main_url, chat_id, 'url'])
        response = requests.get(url, params=self.access_param())
        return response.json()['url']

    def get_chat_messages(self, chat_id, since, until, count) -> dict:
        """
        Получение списка сообщений из чата
        """
        url = '/'.join([self.main_url, '/me/messages'])

        params = self.access_param()
        params['chat_id'] = chat_id
        if since:
            params['from'] = since if isinstance(since, int) else since.timestamp()
        if until:
            params['to'] = until if isinstance(until, int) else until.timestamp()
        if count:
            params['count'] = count

        response = requests.get(url, params=params)
        return response.json()

    def send_chat_message(self, chat_id: str, message: str) -> int:
        """
        Отправить сообщение в чат
        """
        url = 'https://api.ok.ru/graph/{}/messages'.format(chat_id)
        header = {'Content-Type': 'application/json;charset=utf-8'}
        data = {
            "recipient": {"chat_id": chat_id},
            "message": {"text": message}}
        response = requests.post(url, json=data, params=self.access_param(), headers=header)
        if response.status_code == 200:
            return 0
        else:
            return 1

    def send_mailing_message(self, user_list: list, message: str) -> int:
        """
        Рассылка сообщения группе пользователей
        """
        url = '/'.join([self.main_url, '/me/messages'])
        header = {'Content-Type': 'application/json;charset=utf-8'}
        data = {
            "recipient": {"user_ids": user_list},
            "message": {"text": message}
               }
        response = requests.post(url, json=data, params=self.access_param(), headers=header)
        if response.status_code == 200:
            return 0
        else:
            return 1

    def access_param(self) -> dict:
        return {'access_token': self.access_token}


