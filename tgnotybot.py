import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
import re

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Вставьте сюда ваш токен
API_TOKEN = ''

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Функция для парсинга времени из сообщения
def parse_time(time_str: str) -> int:
    """
    Парсит строку времени (например, "10min", "1h", "30s") и возвращает количество секунд.
    """
    time_units = {
        "s": 1,          # секунды
        "sec": 1,       # секунды
        "m": 60,        # минуты
        "min": 60,      # минуты
        "h": 3600,      # часы
        "hour": 3600,   # часы
    }

    # Используем регулярное выражение для извлечения числа и единицы измерения
    match = re.match(r"(\d+)\s*([a-zA-Z]+)", time_str)
    if not match:
        raise ValueError("Некорректный формат времени")

    number, unit = match.groups()
    unit = unit.lower()

    if unit not in time_units:
        raise ValueError("Неподдерживаемая единица измерения времени")

    return int(number) * time_units[unit]

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.reply(
        "Привет! Я бот-напоминалка.\nИспользуй команду /set <время> <текст>, "
        "чтобы установить напоминание.\nНапример: /set 10min еда разогрелась."
        "\nФормат времени: 1sec | 1min | 1h"
    )

# Обработчик команды /set
@dp.message(Command("set"))
async def set_timer(message: Message):
    try:
        # Разделяем сообщение на время и текст
        args = message.text.split(maxsplit=2)
        if len(args) < 3:
            await message.reply("Использование: /set <время> <текст>")
            return

        time_str = args[1]  # Время (например, "10min")
        reminder_text = args[2]  # Текст напоминания

        # Парсим время
        seconds = parse_time(time_str)

        # Отправляем подтверждение
        await message.reply(f"Напоминание установлено на {time_str}: {reminder_text}")

        # Ждем указанное количество секунд
        await asyncio.sleep(seconds)

        # Отправляем напоминание
        await message.answer(f"🔔 Напоминание: {reminder_text}")
    except ValueError as e:
        await message.reply(f"Ошибка: {e}")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())