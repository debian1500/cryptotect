# main.py
import asyncio
from bot import request_confirmation, start_bot

async def logic():
    print("▶ Запрос на подтверждение отправлен...")
    approved = await request_confirmation()

    if approved:
        print("✅ Пользователь подтвердил.")
        # логика перевода/транзакции
    else:
        print("❌ Пользователь отклонил.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())  # Запускаем бота
    loop.run_until_complete(logic())  # Параллельно запускаем свою логику
