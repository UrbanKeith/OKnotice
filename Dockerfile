FROM nginx:1.21.0-alpine

# Установка необходимых пакетов для проекта
RUN apk update && apk add  --no-cache postgresql-dev gcc python3-dev musl-dev python3 py3-pip


RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /app/

# Конфигурация Gunicorn
RUN systemctl start gunicorn

# Конфигурация Nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

EXPOSE 8001:5000

