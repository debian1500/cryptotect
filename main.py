import os, asyncio
from dictionary import AdressBook, save_addressbook
from bot import request_confirmation, start_bot, bot

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

check = 'на вырост'


async def tgVerify():
    print("Отправка запроса в Telegram...")
    try:
        approved = await request_confirmation()
        return approved
    except Exception as e:
        print(f"Ошибка при подтверждении через Telegram: {e}")
        return False


async def verif(address: str):
    global check

    if address in AdressBook:
        print("✅ Адрес найден в адресной книге. Подтверждение не требуется.")
        check = 'verified'
        return

    print("⚠️ Новый адрес. Требуется подтверждение.")
    approved = await tgVerify()

    if approved:
        check = 'verified'
        AdressBook[address] = {"confirmed": True}
        save_addressbook()
        print("✅ Подтверждено. Адрес добавлен в адресную книгу.")
    else:
        check = 'denied'
        print("❌ Операция отклонена.")


def askSeed():
    seed = ''
    while seed != 'word word word':
        seed = ' '.join(input('Введите сид-фразу для входа в кошелек: ').split())
        if seed != 'word word word':
            print('Неверная сид-фраза. Повторите попытку.\n')
    return seed


def choice():
    choiceVar = input("""Выберите действие:
      1. Вывод средств
      2. Получение средств
      Ваш выбор: """)

    while choiceVar not in ["1", "2"]:
        print("Неверный ввод, попробуйте снова.\n")
        return choice()

    return int(choiceVar)


def inputAddress():
    address = input("Введите адрес кошелька: ").strip()
    print(f"Адрес получен: {address}")
    return address


async def main():
    global check

    bot_task = asyncio.create_task(start_bot())
    await asyncio.sleep(1)

    try:
        askSeed()
        user_choice = choice()
        address = inputAddress()

        await verif(address)

        if check != 'verified':
            print("🚫 Операция отклонена. Без подтверждения нельзя продолжить.")
            return

        print(f"✅ Операция разрешена. Выбранное действие: {user_choice}, адрес: {address}")

    finally:
        bot_task.cancel()
        await bot.session.close()  # корректное закрытие Telegram-сессии

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nЗавершено пользователем.")

