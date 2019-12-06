#!/usr/bin/env python

import telebot
import requests
import os
import random
import Sheetsprocess as SP
import BTCcurs as BC
import TimeBtc as TB
import datetime

global id1


bot = telebot.TeleBot('910383229:AAHAMJTe1pgWgfom0kJVxWpDVYNXPZAGFqY')

keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
bt1 = telebot.types.KeyboardButton('Я угадаю курс')
bt2 = telebot.types.KeyboardButton('Посмотреть результаты')
bt3 = telebot.types.KeyboardButton('Посмотреть баланс')
keyboard1.add(bt1, bt2, bt3)

keyboard2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
bt4 = telebot.types.KeyboardButton('Сделать ставку')
bt5 = telebot.types.KeyboardButton('Назад')
keyboard2.add(bt4, bt5)

keyboard3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
bt6 = telebot.types.KeyboardButton('Подтверждаю')
bt7 = telebot.types.KeyboardButton('Исправить')
keyboard3.add(bt6, bt7)

@bot.message_handler(commands=['start'])
def start_message(message):
    nm = message.from_user.first_name


    id1 = message.from_user.id

    if SP.UserList(id1,nm) == True:
        bot.send_message(message.chat.id, 'Здравствуйте, ' +str(nm)+ ' , проверим Ваши навыки!', reply_markup=keyboard1);
    elif SP.UserList(id1,nm) == False:
        bot.send_message(message.from_user.id, 'Вы добавлены', reply_markup=keyboard1)
    else:
        bot.send_message(message.from_user.id, 'Вы добавлены', reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def send_text(message):


    if message.text.lower() == 'я угадаю курс':
        id1 = message.from_user.id
        nm = message.from_user.first_name
        bit = BC.get_latest_bitcoin_price()
        n=random.randint(5,50)
        d = datetime.datetime.today()
        gt = TB.game_time(d)
        bot.send_message(message.from_user.id,'Текущий курс BTC: \n '+str(bit)+' USD\n Текущее количество участников '+str(n)+'\n Начало через '+str(gt)+'. \n Желаете принять участие?  ', reply_markup=keyboard2)

    elif message.text.lower() == 'посмотреть результаты':
        bot.send_message(message.from_user.id, 'В разработке))', reply_markup=keyboard1);


    elif message.text.lower() == 'посмотреть баланс':
        id1 = message.from_user.id
        btc = str(SP.CheckBalance(id1))
        bot.send_message(message.from_user.id, 'Ваш баланс составляет '+btc+' BTC',reply_markup=keyboard1)
    elif message.text.lower() == 'сделать ставку':
        start(message);


    elif message.text.lower() == 'назад':
        bot.send_message(message.from_user.id, 'Осторожность хорошее качество!', reply_markup=keyboard1)





# Обработка ставки

@bot.message_handler(content_types=['text'])
def start(message):
        bot.send_message(message.from_user.id, "Введите сумму ставки");

        bot.register_next_step_handler(message, get_course_num); #следующий шаг – функция get_course_num


def get_course_num(message): #получаем фамилию
    global Btsum;
    Btsum = message.text;
    id1 = message.from_user.id
    btc = str(SP.CheckBalance(id1))


    try:
        Btsum = float(message.text);
        if float(btc) > float(Btsum):


            bit = BC.get_latest_bitcoin_price()
            d = datetime.datetime.today()
            gt = TB.game_time(d)
            bot.send_message(message.chat.id, 'Текущий курс '+str(bit)+'\n Игра начнется через '+str(gt)+'\n По истечению времени ставка автоматически \n принимается на следующую игру \n Укажите ожидаемый размер курса!');
            bot.register_next_step_handler(message, get_course_stavka);
        else:
            bot.send_message(message.chat.id, 'Ваша ставка превышает сумму Вашего банка!\n Попробуйте уменьшить сумму или пополните счет!', reply_markup=keyboard1)
    except Exception:
        bot.send_message(message.from_user.id, 'Ставка должна содержать только цифры')
        start(message)


def get_course_stavka(message): #получаем фамилию
    global course;
    global id1
    id1 = message.from_user.id
    course = message.text;
    try:
        course = float(message.text)
        id1 = message.from_user.id
        nm = message.from_user.first_name
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(telebot.types.InlineKeyboardButton('Да', callback_data='yes'),
                     telebot.types.InlineKeyboardButton('Нет', callback_data='no'))
        bot.send_message(message.from_user.id, '' + nm + ', вы подтверждаете ставку ' +str(Btsum)+ 'BTC,\n на то что курс изменится до '+ str(course) +' ?', reply_markup=keyboard)


    except Exception:
        bot.send_message(message.from_user.id, 'Курс должен содержать только цифры')
        start(message)


# Проверка колбэк условий
@bot.callback_query_handler(func=lambda call: True)
def callback_key(message):
    if message.data == 'yes':

        id1 = message.from_user.id




        bot.answer_callback_query(message.id, text='Ваша ставка принята',show_alert=True)
        bot.send_message(message.from_user.id, "Дождитесь окончания игры чтобы узнать результат!", reply_markup=keyboard1)

        #SP.Stavka(course, Btsum, id1)
        #DB.Stavka(id1, Btsum,course)
        TB.Countdown(id1,course,Btsum)
        if TB.Countdown(id1,course,Btsum) == False:
            bot.send_message(message.chat_id,'Вы были единственным участником, \n попробуйте еще раз чуть позже!' )
        #task1 = Thread(target=TB.Countdown(id1,course,Btsum))
        #task2 = Thread(target=SP.Results(d2, c))
        #task1.start()
        #task1.join()
        else:
            a = SP.final(id1)
            bot.send_message(message.chat_id,''+str(a)+'' )




    elif message.data == 'no':
        bot.answer_callback_query(message.id, text='данные не сохранены',show_alert=True)
        bot.send_message(message.from_user.id, "Пожалуйста введите данные заново.", reply_markup=keyboard1)








if __name__ == '__main__':
    bot.polling()

