from sanic import Sanic, response
import asyncio
import httpx
from aiogram import types
from bot import dp
from config import token
from work_with_db import get_data_from_db

app = Sanic(__name__)

# Логику тут не учитываем, просто то как должна быть асинхронность устроена
# и считаем, что ты уже все настроил, в переменной dp лежит диспатчер


@app.route('/')
async def _index(request):
    return response.text('OK')


@app.route('/get_location/<tid>')
async def get_location(request, tid):
    res = await get_data_from_db(tid)
    if res:
        return response.text(f"{str(res[0])} {str(res[1])}")
    return response.text(f"sorry, not found {str(tid)} in database.")


if __name__ == '__main__':
    app.add_task(
        dp.start_polling()
    )
    app.run(host='0.0.0.0', port='80')
