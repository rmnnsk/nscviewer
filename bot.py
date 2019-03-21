# -*- coding: utf-8 -*-
import time
import telebot
import config
from raspis import rasp
from telebot import types
from dbwork import DBWorker
import nsc
import requests
bot = telebot.TeleBot(config.token)

user_id = 10

dbw = DBWorker(config.database_name)
session = requests.Session()
	
@bot.message_handler(commands = ['Расписание'])
def rasp_msg(message):
	day = time.strftime("%A",time.localtime(time.time()+86400))
	bot.send_message(message.chat.id,rasp[day])

@bot.message_handler(commands = ['Сообщения'])
def get_messages(message):
	global session
	global user_id
	AT = dbw.get_AT(user_id)
	VER = dbw.get_VER(user_id)
	bot.send_message(message.chat.id, get_message((AT, VER),session))	


def klav_msg(message):
	markup = types.ReplyKeyboardMarkup()
	markup.row('1','2','3?','/Расписание','/Выход','/Сообщения')
	bot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)

@bot.message_handler(commands = ['Выход'])
def exit(message):
	global session
	global user_id
	print("Выход user_id: ",user_id)
	AT = dbw.get_AT(user_id)
	VER = dbw.get_VER(user_id)
	print("Выход АТ и ВЕР: ",AT,VER)
	try:
		nsc.exit((AT,VER),session)
		markup = types.ReplyKeyboardRemove(selective = False)
		bot.send_message(message.chat.id, "Выход выполнен", reply_markup = markup)
	except TypeError:
		bot.send_message(message.chat.id,"Выход не выполнен")

@bot.message_handler(commands = ['Вход'])
def enter_request(message):
	bot.send_message(message.chat.id,'Введите логин и пароль: ')

@bot.message_handler(func=lambda message: True, content_types=['text'])
def netsch_ent(message):
	answer = message.text
	anslist = answer.split()
	if len(anslist) == 2:
		login,passw = anslist
		bot.send_message(message.chat.id,"1 стадия:Комплитед")
		global session
		data = nsc.enter(login,passw,session) 
		if data != 0:
			print(login,passw,data)
			ATB,VERB,session = data
			dbw.write_user(login,passw,ATB,VERB)
			global user_id 
			user_id = dbw.get_user_id(VERB)[0]
			bot.send_message(message.chat.id,"Succ(ess) "+str(user_id))
			klav_msg(message)
		else:
			bot.send_message(message.chat.id,"Succ")

if __name__ == '__main__':
    bot.polling(none_stop=True)
