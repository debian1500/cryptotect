import os, asyncio
from dictionary import AdressBook
from bot import request_confirmation, start_bot

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear') # Функция для очистки экрана

check = 'на вырост'
smsVerify = None
emailVerify = None
secondWalletVerify = None



# ✅ Асинхронная функция Telegram-подтверждения
async def tgVerify():
    print("Отправка запроса в Telegram...")
    try:
        approved = await request_confirmation()
        return approved
    except Exception as e:
        print(f"Ошибка при подтверждении через Telegram: {e}")
        return False



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




# Проверка подозрительности и вызов tgVerify
async def verif():
    global check
    if check == 'suspicious':
        approved = await tgVerify()

        if approved:
            check = 'verified'
            print("✅ Доступ подтверждён.")
        else:
            print("❌ Доступ отклонён.")
            exit(1)

    elif check == 'verified':
        print("✔️ Уже подтверждено.")

# 👇 Основной запуск
async def main():
    bot_task = asyncio.create_task(start_bot())  # фоновый запуск бота
    await asyncio.sleep(1)  # пауза на запуск polling

    askSeed()
    await verif()
    user_choice = choice()
    print(f"Вы выбрали: {user_choice}")

    bot_task.cancel()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nЗавершено пользователем.")
