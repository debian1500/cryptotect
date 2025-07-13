import os
import asyncio
from dictionary import AdressBook
from bot import request_confirmation, start_bot, bot  # импортируем бота

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

check = 'на вырост'
smsVerify = None
emailVerify = None
secondWalletVerify = None

# ✅ Telegram-подтверждение
async def tgVerify():
    print("Отправка запроса в Telegram...")
    try:
        approved = await request_confirmation()
        return approved
    except Exception as e:
        print(f"Ошибка при подтверждении через Telegram: {e}")
        return False

# 🔐 Проверка и изменение статуса
async def verif():
    global check

    if check in ["verified", "denied"]:
        print(f"⚠️ Проверка уже пройдена ранее: {check}")
        return

    print("📡 Запрос подтверждения...")
    approved = await tgVerify()

    if approved:
        check = 'verified'
        print("✅ Доступ подтверждён.")
    else:
        check = 'denied'
        print("❌ Доступ отклонён.")

# 🔑 Ввод сид-фразы
def askSeed():
    seed = ''
    while seed != 'word word word':
        seed = ' '.join(input('Введите сид-фразу для входа в кошелек: ').split())
        if seed != 'word word word':
            print('Неверная сид-фраза. Повторите попытку.\n')
    return seed

# 💸 Выбор действия
def choice():
    choiceVar = input("""Выберите действие:
      1. Вывод средств
      2. Получение средств
      Ваш выбор: """)

    while choiceVar not in ["1", "2"]:
        print("Неверный ввод, попробуйте снова.\n")
        return choice()
    
    return int(choiceVar)

# 🧾 Ввод адреса
def inputAddress():
    address = input("Введите адрес кошелька: ").strip()
    # Здесь можно вставить анализ адреса через AdressBook
    print(f"Адрес получен: {address}")
    return address

# 🚀 Основной запуск
async def main():
    global check

    bot_task = asyncio.create_task(start_bot())
    await asyncio.sleep(1)

    askSeed()
    user_choice = choice()
    address = inputAddress()

    # Принудительно делаем check подозрительным (в будущем — анализ из AdressBook)
    check = 'suspicious'

    await verif()

    if check != 'verified':
        print("🚫 Операция отклонена. Без подтверждения нельзя продолжить.")
        await bot.session.close()
        return

    print(f"✅ Операция разрешена. Выбранное действие: {user_choice}, адрес: {address}")

    bot_task.cancel()
    await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nЗавершено пользователем.")
