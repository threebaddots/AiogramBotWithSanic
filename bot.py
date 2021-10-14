#!venv/bin/python
import logging
import datetime
from aiogram import Bot, Dispatcher, executor, types
from config import token
from work_with_db import push_data_to_db


class Memory:

    def __init__(self):
        self.users = dict()

    def get_user(self, chat):
        if chat['id'] not in self.users:
            user_object = {
                'telegram_id': int(chat['id']),
                'balance': 0,
                'last_use': datetime.datetime.now()
            }
            for key in ['first_name', 'last_name', 'username', 'phone']:
                if key in chat:
                    user_object[key] = chat[key]
                else:
                    user_object[key] = None  # если я не получил эту информацию, то она None
            user = User.from_user_object(user_object=user_object)
            self.users[chat['id']] = user
        else:
            user = self.users[chat['id']]

        return user


class User:

    def __init__(self, user_object):
        self.data = user_object
        self.action = None

    @staticmethod
    def from_user_object(user_object):
        return User(user_object)


# Объект бота
bot = Bot(token=token)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
memory = Memory()


@dp.message_handler()
async def get_info(message: types.Message):
    await message.answer("Отправьте лайв локацию")


@dp.message_handler(content_types=[types.ContentType.LOCATION])
async def take_location(message: types.Message):
    await push_data_to_db(message.chat['id'], [message.location["latitude"], message.location["longitude"]])
    await message.answer("Успешно")


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
