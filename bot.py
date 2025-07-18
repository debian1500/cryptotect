import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from dictionary import AdressBook, save_addressbook

# === FSM Состояния ===
class WalletFlow(StatesGroup):
    WaitForSeed = State()
    WaitForChoice = State()
    WaitForAddress = State()

# === Загрузка токена и userID ===
def setup_bot(filename="token.txt"):
    with open(filename, "r") as file:
        lines = file.read().strip().splitlines()
        token = lines[0].strip()
        userID = int(lines[1].strip())

        bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        dp = Dispatcher(storage=MemoryStorage())
        return bot, dp, userID

bot, dp, userID = setup_bot()
waiting_for_response: dict[int, asyncio.Future] = {}

# === /start ===
@dp.message(Command("start"))
async def handle_start(message: Message, state: FSMContext):
    await message.answer("Введите сид-фразу для доступа к кошельку:")
    await state.set_state(WalletFlow.WaitForSeed)

# === Сид-фраза ===
@dp.message(WalletFlow.WaitForSeed)
async def handle_seed(message: Message, state: FSMContext):
    if message.text.strip() != "word word word":
        await message.answer("❌ Неверная сид-фраза. Попробуйте ещё раз.")
        return
    await message.answer("✅ Успешно! Выберите действие:\n1. Вывод средств\n2. Получение средств")
    await state.set_state(WalletFlow.WaitForChoice)

# === Выбор действия ===
@dp.message(WalletFlow.WaitForChoice)
async def handle_choice(message: Message, state: FSMContext):
    if message.text.strip() not in ("1", "2"):
        await message.answer("Пожалуйста, введите 1 или 2.")
        return
    await state.update_data(choice=message.text.strip())
    await message.answer("Введите адрес кошелька:")
    await state.set_state(WalletFlow.WaitForAddress)

# === Ввод адреса и верификация ===
@dp.message(WalletFlow.WaitForAddress)
async def handle_address(message: Message, state: FSMContext):
    address = message.text.strip()
    await state.update_data(address=address)

    if address in AdressBook:
        await message.answer("✅ Адрес уже в адресной книге. Операция разрешена.")
    else:
        await message.answer("⚠️ Новый адрес. Запрашиваю подтверждение...")
        approved = await request_confirmation()

        if approved:
            AdressBook[address] = {"confirmed": True}
            save_addressbook()
            await message.answer("✅ Подтверждено. Адрес добавлен.")
        else:
            await message.answer("❌ Операция отклонена.")
            await state.clear()
            return

    data = await state.get_data()
    choice = data.get("choice")
    await message.answer(f"🎉 Операция разрешена. Действие: {choice}, адрес: {address}")
    await state.clear()

# === Подтверждение кнопками ===
@dp.callback_query(F.data.in_({"yes", "no"}))
async def handle_response(callback: CallbackQuery):
    is_approved = callback.data == "yes"
    msg_id = callback.message.message_id

    if msg_id in waiting_for_response:
        waiting_for_response[msg_id].set_result(is_approved)
        del waiting_for_response[msg_id]

    await callback.message.edit_text("✅ Подтверждено." if is_approved else "❌ Отклонено.")
    await callback.answer("Ответ получен.")

# === Отправка запроса на подтверждение ===
async def request_confirmation() -> bool:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="✅ Подтвердить", callback_data="yes")
    keyboard.button(text="❌ Отклонить", callback_data="no")

    msg = await bot.send_message(
        chat_id=userID,
        text="❗ Подтвердите операцию с новым адресом:",
        reply_markup=keyboard.as_markup()
    )

    future = asyncio.get_running_loop().create_future()
    waiting_for_response[msg.message_id] = future
    return await future

# === Запуск ===
async def start_bot():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())
