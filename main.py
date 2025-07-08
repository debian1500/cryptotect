import os, time
clear = lambda: os.system('cls') # Функция для очистки экрана

from dictionary import AdressBook

check='на вырост'
smsVerify='на вырост'
emailVerify='на вырост'
secondWalletVerify='на вырост'


#def smsVerify():





def verificationSystem(): # функция удостоверения
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

input('Верно. Нажмите Enter для продолжения. ')



def case1():
    sendTo = input('Введите адрес для вывода средств: ')
    if sendTo not in AdressBook:
        print('Этого адреса нет в вашей адресной книге. Пройдите проверку.')
        verificationSystem()
    else:
        print('✅ Вывод произведён успешно.')


def case2():
    receiveFrom = input('Введите адрес, с которого получены средства: ')
    if receiveFrom not in AdressBook:
        print('Подозрительное поступление средств. Пройдите проверку.')
        verificationSystem()
    else:
        print('📥 Средства зачислены от известного адреса.')
