FROM python:3.11


WORKDIR /telegram-chatgpt

COPY requirements.txt .
COPY ./src ./src


RUN pip install -r requirements.txt

CMD ["python", "./src/telegram_ai.py"]