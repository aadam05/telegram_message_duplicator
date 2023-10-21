import os
import requests
import environ
from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters

environ.Env.read_env()
load_dotenv()


tele_token = os.environ.get('TELEGRAM_TOKEN')
bot = Bot(token=tele_token)

# Глобальная переменная для хранения токена авторизации
token = None

# Константы для управления состоянием
ENTER_TOKEN, WAITING_FOR_INPUT = range(2)


async def start(update, context):
    print('we are in start')
    user = update.effective_user
    global token

    if token is None:
        await update.message.reply_text(f"Привет {user.first_name}! Пожалуйста, введите ваш токен:")
        return ENTER_TOKEN
    else:
        await update.message.reply_text(f"Привет {user.first_name}! Введите сообщение для отправки на сервер")
        return WAITING_FOR_INPUT


async def change_token(update, context):
    print('we are in change token')
    global token
    token = None
    await update.message.reply_text("Пожалуйста, введите новый токен:")
    return ENTER_TOKEN


async def set_token(update, context):
    print('we are in set token')
    global token
    token = update.message.text
    await update.message.reply_text(f"Токен успешно сохранен, можете отправлять сообщения")
    return WAITING_FOR_INPUT


async def send_message(update, context):
    print('we are in send message')
    global token
    user_message = update.message.text

    api_url = 'http://127.0.0.1:8000/factory_bot/create_message/'
    data = {'message': user_message}
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code in [200, 201]:
        await update.message.reply_text(f"{update.message.from_user.first_name}, я получил от тебя сообщение: \n{user_message}")
    else:
        await update.message.reply_text("Произошла ошибка при отправке сообщения на ваш API")


async def get_all_messages(update, context):
    print('we are in all messa')
    global token

    api_url = 'http://127.0.0.1:8000/factory_bot/all_mesages/'
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(api_url, headers=headers)

    if response.status_code in [200, 201]:
        result = response.json()
        await update.message.reply_text(f"Список ваших сообщений: \n{result}")
    else:
        await update.message.reply_text("Произошла ошибка при запросе ваших сообщений")


def main():
    application = Application.builder().token(token=tele_token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ENTER_TOKEN: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_token),
            ],
            WAITING_FOR_INPUT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, send_message),
                CommandHandler("all_messages", get_all_messages),
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CommandHandler('change_token', change_token),
        ]
    )
    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
