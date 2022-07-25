from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telethon import TelegramClient, sync
from telebot import *
import telebot
from main.models import *


bot = TeleBot("5528345879:AAHU03eY77ooS1xB9CbFGqFKO_NE3vXZGpI")


@csrf_exempt
def index(request):
    if request.method == 'GET':
        return HttpResponse("Bot Url My Page")
    elif request.method == 'POST':
        bot.process_new_updates([
            telebot.types.Update.de_json(
                request.body.decode("utf-8")
            )
        ])
        return HttpResponse(status=200)


@bot.message_handler(commands=['start'])
def greeting(message):
	main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	btn1 = types.KeyboardButton("O'zbek tili", request_contact=True)
	btn2 = types.KeyboardButton("Rus tili", request_contact=True)	
	main_markup.add(btn1, btn2)
	bot.send_message(message.from_user.id,
	              f"Xush kelibsiz {message.from_user.first_name}. \nTilni tanlang:", reply_markup=main_markup)


@bot.message_handler(content_types=['contact'])
def register_view(message):

	main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	btn1 = types.KeyboardButton("Xodimlar")
	btn2 = types.KeyboardButton("Info")	
	main_markup.add(btn1, btn2)
	
	if len(BotUser.objects.filter(user_id=message.from_user.id))>0:
		bot.send_message(message.from_user.id,
	              "Kerakli bo'limni tanlang", reply_markup=main_markup)

	else:
		bot_user = BotUser.objects.create(
			user_id=message.from_user.id,
			first_name=message.from_user.first_name,
			tel_number = message.contact.phone_number,
			permission='user',
			)
		bot_user.save()
		bot.send_message(message.from_user.id,
	              "Kerakli bo'limni tanlang", reply_markup=main_markup)



@bot.message_handler(func=lambda message: True)
def register_view(message):
	
	main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	btn1 = types.KeyboardButton("Xodimlar")
	btn2 = types.KeyboardButton("Info")	
	btn3 = types.KeyboardButton("Bosh menu")
	main_markup.add(btn1, btn2, btn3)

	info_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	btn1 = types.KeyboardButton("Narxlar")
	btn2 = types.KeyboardButton("Stillar")
	btn3 = types.KeyboardButton("Xodimlar ro'yxati")
	btn4 = types.KeyboardButton("Bosh menu")
	info_markup.add(btn1, btn2, btn3, btn4)

	if message.text == "Xodimlar":
		xodimlar = Employee.objects.all()
		xodimlar_markup = types.InlineKeyboardMarkup(row_width=2)
		for xodim in xodimlar:
			xodimlar_markup.add(types.InlineKeyboardButton(f"{xodim.full_name}", callback_data=f"{xodim.user_id}"))
		menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		btn1 = types.KeyboardButton("Bosh menu")
		# xodimlar_markup.add(btn1)
		bot.send_message(message.from_user.id, "Xodimlar ro'yxati:", reply_markup=xodimlar_markup)
	
	if message.text == "Info":
		bot.send_message(message.from_user.id, "Kerakli bo'limni tanlang:", reply_markup=info_markup)
	
	if message.text == "Narxlar":
		costs = ServiceCosts.objects.all()
		for cost in costs:
			bot.send_message(message.from_user.id, f"Turi: {cost.name}.\nNarxi: {cost.cost} so'm.")

	if message.text == "Stillar":
		styles = Styles.objects.all()
		for style in styles:
			bot.send_message(message.from_user.id, f"Stil turi: {style.name}.")

	if message.text == "Xodimlar ro'yxati":
		employees = Employee.objects.all()
		for employee in employees:
			bot.send_message(message.from_user.id, f"Ism Familiyasi: {employee.full_name}.\nTelefon raqami: {employee.tel_number}.\nIsh tajribasi: {employee.work_experience}.")

	if message.text == "Bosh menu":
		bot.send_message(message.from_user.id,
	              "Kerakli bo'limni tanlang", reply_markup=main_markup)

		