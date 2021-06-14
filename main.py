import telebot    # Телеграм-бот
import time       # Задержка
from sms_bomb import bomber   # Бомбер

services = bomber.loadservices("services.txt")    # Подгружаем сервисы

token = 'Тут токен'
bot = telebot.TeleBot(token)

sleepp = 0    # Задержка
cnt = 0       # Кол-во повторений
number = ''   # Номер телефона

@bot.message_handler(commands=['start'])
def start_func(message):
  bot.send_message(message.chat.id, 'Добро пожаловать в "Нирвана". Чтобы начать, напишите "1". Чтобы получить список команд, напишите "help"')

@bot.message_handler(content_types=['text'])
def intro_handler(message):
  if message.text == '1':
    bot.send_message(message.from_user.id, 'Напишите номер телефона.\nФормат: 79123456789')
    bot.register_next_step_handler(message,action_handler)
  elif message.text == 'help':
    bot.send_message(message.from_user.id, 'Доступные команды:\n"help" - узнать список команд\n"1" - начать.')
  else:
    bot.send_message(message.from_user.id, 'Неизвестная команда, напишите "help", чтобы узнать доступные команды.')

def action_handler(message):
  if message.text[0] == '7':
    if len(message.text) == 11:
      global number
      number = message.text
      bot.send_message(message.from_user.id, 'Введите время задержки в секундах (5-10)')
      bot.register_next_step_handler(message,sleepp_handler)
    else:
      bot.send_message(message.from_user.id, 'Некорректный номер.\nПовторите попытку.')
      bot.register_next_step_handler(message,action_handler)
  elif message.text[0] == '8':
    bot.send_message(message.from_user.id, 'Номер не может начинаться с "8". Повторите попытку.')
    bot.register_next_step_handler(message,action_handler)
  else:
    bot.send_message(message.from_user.id, 'Это не номер. Повторите попытку.')
    bot.register_next_step_handler(message,action_handler)
def sleepp_handler(message):
  if int(message.text)>=5 and int(message.text)<=10:
    global sleepp
    sleepp = int(message.text)
    bot.send_message(message.from_user.id, 'Введите количество повторений (1-5)')
    bot.register_next_step_handler(message,count_handler)  
  else:
    bot.send_message(message.from_user.id, 'Время задержки должно находиться в диапазоне от 5 до 10 сек.\nПовторите попытку.')
    bot.register_next_step_handler(message,sleepp_handler)
def count_handler(message):
  if int(message.text)>=1 and int(message.text)<=5:
    global cnt
    cnt = int(message.text)
    bot.send_message(message.from_user.id, 
                     f'''
Все готово. \nПроверьте правильность введенных данных:
Номер телефона: {number}\nЗадержка: {sleepp} сек.\nКол-во повторений: {cnt}
Если все верно, напишите "+", если хотите начать сначала, напишите "-"
                     ''')
    bot.register_next_step_handler(message,bomber_handler)
  else:
    bot.send_message(message.from_user.id, 'Кол-во повторений должно находиться в диапазоне от 5 до 10 сек.\nПовторите попытку.')
    bot.register_next_step_handler(message,count_handler)
def bomber_handler(message):
  if message.text == '-':
    bot.send_message(message.from_user.id, 'Хорошо. Начинаем сначала.')
    bot.send_message(message.from_user.id, 'Напишите номер телефона.\nФормат: 79123456789')
    bot.register_next_step_handler(message,action_handler)
    return None
  elif message.text == '+':
    bot.send_message(message.from_user.id, 'Поехали.')
    for _ in range(cnt):
      bot.send_message(message.from_user.id, f'Проход № {_+1}')
      bomber.run(services, number)
      time.sleep(sleepp)
    bot.send_message(message.from_user.id, f'Бот окончил свою работу.\nЧтобы повторить, напишите "1"')
    bot.register_next_step_handler(message,intro_handler)
  else:
    bot.send_message(message.from_user.id, 'Пожалуйста, подтвердите правильность введенных данных.')
    bot.register_next_step_handler(message,bomber_handler)
bot.polling()
