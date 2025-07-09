import os, time
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear') # Функция для очистки экрана

from dictionary import AdressBook

check='на вырост'
smsVerify=None # сделать функцию, найти библиотеку с SMS и способ отправлять их
emailVerify=None # сделать функцию, найти библиотеку и способ отправлять их
secondWalletVerify=None # сделать функцию, найти библиотеку и способ отправлять их



def verif(): # функция удостоверения
    global check
    if check == 'suspicious':
        
        # отправляем запрос по СМС, почте или в интерфейс второго кошелька

        # доработать взаимодействие со всеми тремя, сейчас стоит заглушка True
        if smsVerify==True or emailVerify==True or secondWalletVerify==True: # если владелец подтвердил
            check='verified'
        
           
    elif check == 'verified':
        print('')



def askSeed():  # Функция запроса сид-фразы
    return ' '.join(input('Введите сид-фразу для входа в кошелек: ').split())

seed = askSeed()  # Функция проверки верности сид-фразы (не путать с предыдущей)
while seed != 'word word word':
    print('Неверная сид-фраза. Повторите попытку')
    seed = askSeed()



def caseSend(): # Кейс вывода
    sendTo = input('Введите адрес для вывода средств: ')
    if sendTo not in AdressBook:
        print('Этого адреса нет в вашей адресной книге. Пройдите проверку.')
        verif()
    else:
        print('✅ Вывод произведён успешно.')


def caseReceive(): # Кейс получения
    receiveFrom = input('Введите адрес, с которого получены средства: ')
    if receiveFrom not in AdressBook:
        print('Подозрительное поступление средств. Пройдите проверку.')
        verif()
    else:
        print('📥 Средства зачислены от известного адреса.')


def choice(): 
    input("""Выберите действие:
               1. Вывод средств
               2. Получение средств
    """)
    #while input not in [1,2]:

    # доделать