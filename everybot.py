# coding=utf-8
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import re
import time
import threading
from datetime import datetime

from tkinter import *
from tkinter.scrolledtext import *
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk

global groupid, request, proceed, welcome_message, newchat, stopchat, ansdict, anskeys, ansvals, vk, longpull, scorepath, mainacc
groupid = '-140876144' #Айди группы,анонимного чата, с которой в данной случае происходит вся переписка
request = '' #Сообщение собеседника по умолчанию
proceed = True #Разморозка программы по умолчанию
welcome_message = 'Привет!' #Приветственное сообщения для кажого нового диалога
newchat = '!поиск' #Сообщение для поиска нового собеседника
stopchat = '!с' #Сообщение для остановки текущего диалога
vktoken = 'token' #Токен Вконтакте
scorepath = r"score.txt" #Название/путь файла со счетом сообщений
mainacc = '397514037' #Айди аккаунта на который происходит пересылка всех фото 

ansdict = {
    #Ответы по умолчанию
    'собеседник найден':welcome_message,
    'вы не в диалоге':'',
    'вы добавлены':'',
    'ваш собеседник заблокировал':stopchat,
    'остановлен':newchat,
    
    #Дополнительные ответы
    'удачи':stopchat,
}

anskeys = list(ansdict.keys())
ansvals = list(ansdict.values())

#Подключение аккаунта Вконтакте
vk = vk_api.VkApi(token=vktoken)
longpoll = VkLongPoll(vk)

#Создание размещение, и настройка окна программ
root = ThemedTk(theme="arc") 
root.title("DBot")
root.resizable(False, False)
root.geometry("700x450")

#Метод для отправки сообщения в диалог
def write_msg(user_id, message, attach=''):
    global score, request, write_msg, score
    score+=random.randint(2,7)
    if attach: #Отправка сообщения с фото
        vk.method('messages.send', {'peer_id': user_id, 'random_id': score, 'message': message, 'attachment':attach})
    else: #Отправка сообщения без фото
        vk.method('messages.send', {'peer_id': user_id, 'random_id': score, 'message': message})
    insert("\nОтправленное сообщение:\n", message)
    writescore()

#Отправка сообщения для завершения диалога
def sendstop():
    write_msg(groupid, "!с")

#Отправка сообщения для начала нового диалога
def sendnew():
    write_msg(groupid, newchat)

#Заморозка и разморозка программы
def freezechat():
    global proceed
    if proceed == True:
        proceed = False
        insert("\n$ Бот был выключен.")
    else:
        proceed = True
        insert("\n$ Бот был включен.")

#Отправка сообщения в диалог
def sendcustom():
    global sendtext
    message = sendtext.get()
    if message.replace('\n', ''):
        write_msg(groupid, message)
        sendtext.delete(0, END)
    else:
        messagebox.showerror("DBot", "Пустое сообщение.")

#Вывод в "консоль" текста в окне программы
def insert(text, text2=''):
    text = str(text) + str(text2) 
    cons.insert(END, text)

#Функция для игнора регистра букв
def icase(case):
    case = case[0].upper() + case[1:]
    return case

#Запись счета сообщений в отдельный файл
def writescore():
    with open(scorepath, "w") as file:
        file.write(str(score))

#Основной метод первого потока
def oponent(threadName):
    while True: 
        insert("$ Сессия EveryBot запущена.")
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    if proceed == True:
                        try:
                            if event.group_id == 140876144:
                                request = event.text
                                insert("\nПолученное сообщение:\n", request + '\n')

                                #При получении каких либо фотографий их пересылка на основной аккаунт
                                if event.attachments:
                                    photo = list(event.attachments.values())
                                    if photo:
                                        for i in photo:
                                            Pgen = 'photo' + i
                                            write_msg(mainacc, '&#12;', Pgen)
                                    insert("$ Фото переслано на основной аккаунт.")

                                for i in range(len(anskeys)):
                                        if anskeys[i] in request or icase(anskeys[i]) in request:
                                                if ansvals[i] != '':
                                                        write_msg(groupid, ansvals[i])
                        except:
                            insert("$ Вам написали, но сработал фильтр.")
       
#Основной метод второго потока
def timer(threadName):
    while True:
        if request != "":
            current_time = datetime.now() 
            current_time = current_time.strftime("%H %M")
            current_time = current_time.split(" ") 
            prerequest = request
            while prerequest == request or re.match(r"^\s*$", request):
                current_time2 = datetime.now() 
                current_time2 = current_time2.strftime("%H %M")
                current_time2 = current_time2.split(" ")
                if int(current_time2[1]) - int(current_time[1]) >= 5:
                    write_msg(groupid, "!с")
                    timer(thread2)

#Инициализация интерфейса tkinter
cons = ScrolledText(root, width=75, height=20, relief="flat", wrap=WORD)
cons.place(x=50, y=15)

sendtext = ttk.Entry(root, width=20)
sendtext.place(x=150, y=403)

bt_clear = ttk.Button(root, text='Остановить диалог', command=sendstop)
bt_clear.place(x=50, y=350)

bt_new = ttk.Button(root, text='Новый диалог', command=sendnew)
bt_new.place(x=200, y=350)

bt_custom = ttk.Button(root, text='Вкл/Выкл', width=10, command=freezechat)
bt_custom.place(x=570, y=350)

bt_custom = ttk.Button(root, text='Отправить', command=sendcustom)
bt_custom.place(x=50, y=400)

#Инициализация потоков и их методов
class myThread1 (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        insert("Запуск 1-ого потока. " + self.name + '\n')
        oponent(self.name)

class myThread2 (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name 

    def run(self):
        insert("Запуск 2-ого потока. " + self.name + '\n')
        timer(self.name)
        
#Получение счета сообщений при новой сессии бота
with open(scorepath, "r") as reader:
    tlines = reader.readlines()
    score = int(tlines[0])

#Запуск и соединение потоков
thread1 = myThread1("Поток - 1")
thread2 = myThread2("Поток - 2")

thread1.start()
thread2.start()

root.mainloop()
thread1.join()
thread2.join()
