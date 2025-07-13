# bot.py
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties

# === Настройка ===
def setup_bot(filename="token.txt"):
    try:
        with open(filename, "r") as file:
            lines = file.read().strip().splitlines()
            token = lines[0].strip()
            userID = int(lines[1].strip())

            bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
            dp = Dispatcher()
            return bot, dp, userID

    except Exception as error:
        print(f"❌ Ошибка: не удалось загрузить token.txt\n{error}")
        exit(1)

bot, dp, userID = setup_bot()
waiting_for_response: dict[int, asyncio.Future] = {}

@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer("Бот запущен. Готов принимать запросы на подтверждение.")

@dp.callback_query(F.data.in_({"yes", "no"}))
async def handle_response(callback: CallbackQuery):
    is_approved = callback.data == "yes"
    msg_id = callback.message.message_id

    if msg_id in waiting_for_response:
        waiting_for_response[msg_id].set_result(is_approved)
        del waiting_for_response[msg_id]

    text = "✅ Подтверждено." if is_approved else "❌ Отклонено."
    await callback.message.edit_text(text)
    await callback.answer("Ответ получен.")

# — Эта функция будет вызываться из main.py —
async def request_confirmation() -> bool:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="✅ Подтвердить", callback_data="yes")
    keyboard.button(text="❌ Отклонить", callback_data="no")

    msg = await bot.send_message(
        chat_id=userID,
        text="❗ Запрос на вывод средств. Подтвердить?",
        reply_markup=keyboard.as_markup()
    )

    future = asyncio.get_running_loop().create_future()
    waiting_for_response[msg.message_id] = future
    return await future

# — Запускать polling только вручную —
async def start_bot():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())




__all__ = ["request_confirmation", "start_bot"]
