import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import re
from datetime import datetime
import time

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
mat = ['гей','ука','бл','еба','долб','конч']
listans = {} 
msg = '📜 Список созданных ответов пользователями:\n '
token = "6a9c267cd469388709a9e9acaddbe0aa81a0abbf12239b3e597a31729ffbddb9c88e80a443554c918b8f7"

with open(r"C:\Users\valer\OneDrive\Рабочий стол\ \Программирование\Python\Проектики\AnoBot\score.txt", "r") as reader:
    tlines = reader.readlines()
    score = int(tlines[0])

def write_msg(user_id, message):
    global score
    score+=random.randint(2,7)
    vk.method('messages.send', {'peer_id': user_id, 'random_id': score, 'message': message})
    print("Сообщение по счету:", score)
    writescore()

def icase(case):
    case = case[0].upper() + case[1:]
    return case

def writescore():
    with open(r"C:\Users\valer\OneDrive\Рабочий стол\ \Программирование\Python\Проектики\AnoBot\score.txt", "w") as file:
        file.write(str(score))

vk = vk_api.VkApi(token='0707c7c59d5db25b3a306653c9ebc8c5ad9538249eea5f9365a149564886186f92b1d928a666889a76305')
longpoll = VkLongPoll(vk)
print("Сессия запущена.")

for event in longpoll.listen():
    dict_keys = list(listans.keys())
    dict_values = list(listans.values())

    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:

            groupid = '-140876144'
            request = event.text
            print("Полученное сообщение:\n", request)

            if "Собеседник найден" in request:
                write_msg(groupid, "🤠 Привет. Я великий и неподрожаемый Маркус, бот всего анонимного чата.\nМеня можно доработать, или пообщаться со мной.\n⚙️ Добавить свои ответы на сообщения: /добавить 'сообщение' 'ответ'\n🎲 Узнать ссылку на создателя бота: /создатель\n👀 Показать ответы созданные пользователями: /список\n При возникновении технических неполадок и подобного, пишите сразу в лс.")

            elif '/список' in request or request == '👀':
                for num in range(len(dict_keys)):
                    msg += 'фраза "' + dict_keys[num] + '" | ответ "' + dict_values[num] + '"\n'
                write_msg(groupid, msg)

            elif '/добавить' in request:
                if re.match(r"/добавить\s'.*'\s'.*'", request):
                    no_space = request.split("'")
                    listans[no_space[1]] = no_space[3]
                    write_msg(groupid, "✔️ Успешно добавлено!")
                else:
                    write_msg(groupid, "Правильное написание: /добавить 'сообщение' 'ответ'")

            elif '/создатель' in request or request == '🎲':
                write_msg(groupid, "!мояссылка vk.com/lovelygalaxy")
            
            elif 'прив' in request or icase('прив') in request:
                write_msg(groupid, "Приветик еще раз :3")

            elif 'хах' in request or icase('хах') in request:
                write_msg(groupid, "Действительно смешно...")
                
            elif '?' in request:
                print(icase('прив'))
                write_msg(groupid, "Что?")

            elif 'нет' in request or icase('нет') in request:
                write_msg(groupid, "Ну почему нет-то?!")

                write_msg(groupid, "Действительно смешно...")
            elif 'как дела' in request or icase('как дела') in request:
                write_msg(groupid, "Меня вот только недавно сделали, наслаждаюсь общением с людьми;)")

            elif "остановлен" in request:
                write_msg(groupid, "!н")

            else:
                num = 0
                switched = False
                for i in dict_keys:
                    if i == request:
                        write_msg(groupid, dict_values[num])
                        switched = True
                    num+=1
                if "Вы добавлены" in request or "Вы можете оставить" in request or "Вы добавлены" in request:
                    pass
                else:
                    write_msg(groupid, "Я тебя не понял 🙁")

            #for i in mat:
            #    if i in request or i[0].upper() + i[1:] in request:
            #         angry = True
            #if angry == True:
            #    write_msg(groupid, "Ты как посмел, вон отсюда!")
            #    angry = False
                
            

            
                