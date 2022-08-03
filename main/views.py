from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telebot import *
import telebot
from main.models import *
from datetime import datetime, timedelta
from .button import button_gen
from .text import AllText



bot = TeleBot("5543099680:AAEZe4bcFJ2dYMkv4pzokeU7hRxPSI4vE7o", parse_mode="HTML")


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
def start(message):
    markup = button_gen("O'zbek tili", "Rus tili", request_contact=True)
    text = AllText(first_name=message.from_user.first_name)
    bot.send_message(message.from_user.id, text.start(), reply_markup=markup)


@bot.message_handler(func=lambda message: True, content_types=['contact'])
def register_view(message):
    text = AllText(first_name=message.from_user.first_name)
    main_markup = button_gen("Joy buyurtma qilish", "Info")
    main_markup_ru = button_gen("Сотрудники", "Инфo")
    main_markup_admin = button_gen("Yangi xodim qo'shish", "E'lon jo'natish", "Xodimni o'chirish", "Statistika")
    main_markup_admin_ru = button_gen("Добавить нового сотрудника", "Разместить объявление", "Удалить сотрудника", "Статистика")
    if len(BotUser.objects.filter(user_id=message.from_user.id))>0:
        admin = BotUser.objects.get(user_id=message.from_user.id)
        if admin.permission == "admin":
            bot.send_message(message.from_user.id, "Hurmatli admin kerakli bo'limni tanlang:", reply_markup=main_markup_admin)
        else:
            bot.send_message(message.from_user.id, text.step2(), reply_markup=main_markup)
    else:
        bot_user = BotUser.objects.create(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            tel_number=message.contact.phone_number,
            permission='user',
        )
        bot_user.save()
        bot.send_message(message.from_user.id, "Kerakli bo'limni tanlang", reply_markup=main_markup)
        

@bot.message_handler(func=lambda message: True)
def register_view(message):
    users = BotUser.objects.all()
    form_main_markup = button_gen("Orqaga", "Bekor qilish")
    admin = BotUser.objects.get(user_id=message.from_user.id)
    main_markup = button_gen("Joy buyurtma qilish", "Info")
    info_markup = button_gen("Narxlar", "Stillar", "Xodimlar ro'yxati", "Bosh menu")
    employee = Employee.objects.all()
    message_step = MessageStep.objects.all().first()
    main_markup_admin = button_gen("Yangi xodim qo'shish", "E'lon jo'natish", "Xodimni o'chirish", "Statistika")
    new_employee = Employee.objects.filter(is_created=True).first()
    
    if message.text == "Joy buyurtma qilish":
        xodimlar_markup = types.InlineKeyboardMarkup(row_width=2)
        for i in employee:
            xodimlar_markup.add(types.InlineKeyboardButton(f"{i.full_name}", callback_data=f"{i.user_id}"))
        bot.send_message(message.from_user.id, "O`zingizga yoqqan sartaroshni tanlang:", reply_markup=xodimlar_markup)
    
    elif message.text == "Info":
        bot.send_message(message.from_user.id, "Kerakli bo'limni tanlang:", reply_markup=info_markup)
    
    elif message.text == "Narxlar":
        costs = ServiceCosts.objects.all()
        for cost in costs:bot.send_message(message.from_user.id, f"Turi: {cost.name}.\nNarxi: {cost.cost} so'm.")
    
    elif message.text == "Stillar":
        styles = Styles.objects.all()
        for style in styles:
            bot.send_message(message.from_user.id, f"Stil turi: {style.name}.")
    
    elif message.text == "Xodimlar ro'yxati":
        employees = Employee.objects.all()
        for employee in employees:
            bot.send_message(message.from_user.id, f"Ism Familiyasi: {employee.full_name}.\nTelefon raqami: {employee.tel_number}.\nIsh tajribasi: {employee.work_experience} yil.")
    
    elif message.text == "Bosh menu":
        bot.send_message(message.from_user.id, "Kerakli bo'limni tanlang", reply_markup=main_markup)

    elif admin.permission == "admin" and message.text == "E'lon jo'natish": # commands from the admin
        message_step.step = 1
        message_step.save()
        bot.send_message(message.from_user.id, "Xabarni jo'nating")
    
    elif message_step.step == 1:
        message_text = message.text # receive the message from the admin
        for user in users:
            bot.send_message(user.user_id, message_text) # send the message to each user
        message_step.step = 0
        message_step.save()
        # how to stop sending messages to the users who blocked or deleted the bot?
    
    elif message.text == "Orqaga":
        new_employee.step -= 1
        new_employee.save()
        cancel_func(message)

    elif message.text == "Bekor qilish":
        new_employee.delete()
        bot.send_message(message.from_user.id, "Bekor qilindi!", reply_markup=main_markup_admin)

    elif message.text == "Xodimni o'chirish":
        xodimlar_markup = types.InlineKeyboardMarkup(row_width=2)
        for i in employee:
            xodimlar_markup.add(types.InlineKeyboardButton(f"{i.full_name}", callback_data=f"{i.user_id} delete"))
        bot.send_message(message.from_user.id, "O'chirilishi kerak bo'lgan xodimni tanlang:", reply_markup=xodimlar_markup)
    
    elif message.text == "Statistika":
        orders = Order.objects.all().count()
        users = len(BotUser.objects.filter(permission="user"))
        bot.send_message(message.from_user.id, f"Barcha mijozlar soni {users} ta.\nBarcha buyurtmalar soni {orders} ta.")

    elif message.text == "Yangi xodim qo'shish": # adding employee
        form_markup = button_gen("Bekor qilish")
        new_employee = Employee.objects.create(
        step=1,
        user_id=123,
        is_created=True
        )
        new_employee.save()
        bot.send_message(message.from_user.id, "Ishchining ism familiyasini kiriting:", reply_markup=form_markup)

    elif new_employee.step == 1:
        new_employee.full_name = message.text
        new_employee.step += 1
        new_employee.save()
        bot.send_message(message.from_user.id, "Ishchining telegram id raqamini kiriting:", reply_markup=form_main_markup)
    
    elif new_employee.step == 2:
        if str(message.text).isdigit():
            new_employee.user_id = message.text
            new_employee.step += 1
            new_employee.save()
            bot.send_message(message.from_user.id, "Ishchining telefon raqamini kiriting:")
        else:
            bot.send_message(message.from_user.id,
                             'Iltimos to\'g\'ri ma\'lumot kiriting🙅‍♂️\nIshchining telegram id raqamini kiriting:')
    elif new_employee.step == 3:
        if str(message.text).isdigit():
            new_employee.tel_number = message.text
            new_employee.step += 1
            new_employee.save()
            bot.send_message(message.from_user.id, "Ishchining ish tajriba muddatini kiriting:")
        else:
            bot.send_message(message.from_user.id,
                             'Iltimos to\'g\'ri ma\'lumot kiriting🙅‍♂️\nIshchining telefon raqamini kiriting:')

    elif new_employee.step == 4:
        if str(message.text).isdigit():
            new_employee.work_experience = message.text
            new_employee.step = 0
            new_employee.is_created = False
            new_employee.save()
            bot.send_message(message.from_user.id, "Muvaffaqiyatli qo'shildi!", reply_markup=main_markup_admin)
        else:
            bot.send_message(message.from_user.id,
                                 'Iltimos to\'g\'ri ma\'lumot kiriting🙅‍♂️\nIshchining ish tajriba muddatini kiriting:')
    

class TimeReception:
    def __init__(self):
        self.now = datetime.now()
        self.start_time = int(self.now.strftime('%H'))

    def now_hour(self):
        return self.start_time

    def time_r(self, n):
        if int(self.now.strftime("%M")) > 30:
            return (self.now + timedelta(minutes=n * 30 + abs(60-int(self.now.strftime('%M'))))).strftime('%H:%M')
        else:
            return (self.now + timedelta(minutes=n * 30 + abs(30 - int(self.now.strftime('%M'))))).strftime('%H:%M')


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call): #'10:30'
    if 'delete' in call.data:
        employee_id = str(call.data).split(' ')[0]
        employee = Employee.objects.get(user_id=employee_id)
        employee.delete()
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id, text=f"{employee.full_name} bazadan o'chirildi!")    
    if ':30' in call.data or ':00' in call.data:
        employee_id = str(call.data).split('_')[3]
        order_time = str(call.data).split('_')[1]
        user = BotUser.objects.get(user_id=call.from_user.id)
        employee = Employee.objects.get(user_id=employee_id)
        order = Order.objects.create(
            bot_user=user,
            employee=employee,
            order_time=order_time
        )
        order.save()
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id, text="Buyurtmangiz qabul qilindi")
    elif Employee.objects.filter(user_id=call.data).exists():
        employee = Employee.objects.get(user_id=call.data)
        time_markup = types.InlineKeyboardMarkup(row_width=3)
        n = 0
        time_r = TimeReception()
        start = 9
        end = 21
        if time_r.now_hour() > 9:
            start = time_r.now_hour()
        if 8 < time_r.now_hour() < 22:
            for xodim in range(((end-start)//3)*2+1):
                time_markup.add(types.InlineKeyboardButton(f"{time_r.time_r(n+0)}", callback_data=f"time_{time_r.time_r(n+0)}_userid_{call.data}"), types.InlineKeyboardButton(f"{time_r.time_r(n+1)}", callback_data=f"time_{time_r.time_r(n+1)}_userid_{call.data}"), types.InlineKeyboardButton(f"{time_r.time_r(n+2)}", callback_data=f"time_{time_r.time_r(n+2)}_userid_{call.data}"))
                n += 3
            bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id, text=f"{employee.full_name}ni kun tartibi", reply_markup=time_markup)
        else:
            bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id, text="Bizda ish vaqti 09:00 dan 21:00 gacha")

    


def cancel_func(message):
    new_employee = Employee.objects.filter(is_created=True).first()
    form_markup = button_gen("Orqaga", "Bekor qilish")    
    if new_employee.step == 1: 
        bot.send_message(message.from_user.id, 'Ishchining ism familiyasini kiriting:', reply_markup=form_markup)
    elif new_employee.step == 2:
        bot.send_message(message.from_user.id, 'Ishchining telegram id raqamini kiriting:')  
    elif new_employee.step == 3: 
        bot.send_message(message.from_user.id, 'Ishchining telefon raqamini kiriting:')   
    elif new_employee.step == 4:
        bot.send_message(message.from_user.id, 'Ishchining ish tajriba muddatini kiriting:')
       