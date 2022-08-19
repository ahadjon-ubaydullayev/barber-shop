from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telebot import *
import telebot
from main.models import *
from datetime import datetime, timedelta, date
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
    markup = button_gen("Begin", request_contact=True)
    text = AllText(first_name=message.from_user.first_name)
    bot.send_message(message.from_user.id, text.start(), reply_markup=markup)


@bot.message_handler(func=lambda message: True, content_types=['contact'])
def register_view(message):
    markup = button_gen("🇺🇿O'zbek tili🇺🇿", "🇷🇺Rus tili🇷🇺")
    if len(BotUser.objects.filter(user_id=message.from_user.id)) == 0:
        bot_user = BotUser.objects.create(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            tel_number=message.contact.phone_number,
            permission='user',
        )
        
        bot_user.save()
        tel_number = message.contact.phone_number
        if '+' in tel_number:
            tel_number = message.contact.phone_number[1:]
        if Employee.objects.filter(tel_number=tel_number).exists():
            print("foydalanishingiz")
            employee = Employee.objects.get(tel_number=tel_number)
            employee.user_id = int(message.from_user.id)
            employee.active = True
            employee.save()
            bot_user.permission = 'employee'
            bot_user.save()
    bot.send_message(message.from_user.id, f"Hurmatli {message.from_user.first_name} Tilni tanlang👇",
                     reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def register_view(message):
    users = BotUser.objects.all()
    form_main_markup = button_gen("Orqaga⬅️", "Bekor qilish❌")
    admin = BotUser.objects.get(user_id=message.from_user.id)
    info_markup = button_gen("Narxlar💰", "Stillar💇‍♂️", "Xodimlar ro'yxati🤵‍♂️", "Bosh menu📊")
    info_markup_ru = button_gen("Цены💰", "Стили💇‍♂️", "Список сотрудников 🤵‍♂️", "Главное меню📊")
    employee = Employee.objects.all()
    message_step = MessageStep.objects.all().first()
    main_markup_user = button_gen("Joy buyurtma qilish✏️", "Info📕", "Buyurtmalarim🛎")
    main_markup_admin = button_gen("Yangi xodim qo'shish👨‍💼", "E'lon jo'natish🗣", "Xodimni o'chirish🙅‍♂️", "Statistika📈")
    main_markup_employee = button_gen("Kunlik Mijozlar👨🏻‍⚖️", "Ish vaqti⏰", "Reyting📈")
    main_markup_user_ru = button_gen("Сделать заказ✏️", "Информация📕", "Мои заказы🛎")
    main_markup_admin_ru = button_gen("Добавить нового сотрудника👨‍💼", "Подать объявление🗣", "Удалить сотрудника🙅‍♂️", "Статистика📈")
    main_markup_employee_ru = button_gen("Ежедневные клиенты👨🏻‍⚖️", "Время работы⏰", "Рейтинг📈")
    new_employee = Employee.objects.filter(is_created=True).first()
    if len(EmployeeSchedule.objects.filter(status=True)) > 0:
        new_schedule = EmployeeSchedule.objects.filter(status=True).first()
    if message.text == "🇺🇿O'zbek tili🇺🇿":
        admin.language = 'uz'
        admin.save()
        if admin.permission == 'employee':
            bot.send_message(message.from_user.id,
                             "Hurmatli Xodim,\nsiz uchun yaratilgan\nqulayliklardan foydalanishingiz mumkin👇:",
                             reply_markup=main_markup_employee)
        elif admin.permission == 'admin':
            bot.send_message(message.from_user.id,
                             "Hurmatli Admin,\nsiz uchun yaratilgan\nqulayliklardan foydalanishingiz mumkin👇:",
                             reply_markup=main_markup_admin)
        else:
            bot.send_message(message.from_user.id,
                             f"Hurmatli {message.from_user.first_name}\nsiz uchun yaratilgan\nqulayliklardan foydalanishingiz mumkin👇:",
                             reply_markup=main_markup_user)
    elif message.text == "🇷🇺Rus tili🇷🇺":
        admin.language = 'ru'
        admin.save()
        if admin.permission == 'employee':
            bot.send_message(message.from_user.id,
                             "Уважаемый сотрудник,\n вы можете\nпользоваться созданными для вас удобствами.👇:",
                             reply_markup=main_markup_employee_ru)
        elif admin.permission == 'admin':
            bot.send_message(message.from_user.id,
                             "Уважаемый админ,\n вы можете\nпользоваться созданными для вас объектами👇:",
                             reply_markup=main_markup_admin_ru)
        else:
            bot.send_message(message.from_user.id,
                             f"Уважаемый {message.from_user.first_name},\n вы можете\nпользоваться удобствами, созданными для вас.👇:",
                             reply_markup=main_markup_user_ru)

    elif message.text == "Joy buyurtma qilish✏️" or message.text == "Сделать заказ✏️":
        xodimlar_markup = types.InlineKeyboardMarkup(row_width=2)
        for i in employee:
            xodimlar_markup.add(types.InlineKeyboardButton(f"{i.full_name}", callback_data=f"{i.user_id}"))
        if admin.language == 'uz':
            bot.send_message(message.from_user.id, "O`zingizga maqul kelgan sartaroshni tanlang va buyurtma bering:",
                             reply_markup=xodimlar_markup)
        else:
            bot.send_message(message.from_user.id, "Выберите парикмахера, который вам нравится:",
                             reply_markup=xodimlar_markup)


    elif message.text == "Orqaga↩️":
        message_step.step = 0
        message_step.save()
        bot.send_message(message.from_user.id, "Bekor qilindi!", reply_markup=main_markup_admin)

    elif message.text == "Info📕" or message.text == "Информация📕":
        if admin.language == 'uz':
            bot.send_message(message.from_user.id, "Kerakli bo'limni tanlang:", reply_markup=info_markup)
        else:
            bot.send_message(message.from_user.id, "Выберите нужный раздел:", reply_markup=info_markup_ru)

    elif message.text == "Narxlar💰" or message.text == "Цены💰":
        costs = ServiceCosts.objects.all()
        if admin.language == 'uz':
            for cost in costs:
                bot.send_message(message.from_user.id, f"Turi: {cost.name}.\nNarxi: {cost.cost} so'm.")
        else:
            for cost in costs:
                bot.send_message(message.from_user.id, f"Тип: {cost.name}.\nРасходы: {cost.cost} сум.")

    elif message.text == "Stillar💇‍♂️" or message.text == "Стили💇‍♂️":
        styles = Styles.objects.all()
        if admin.language == 'uz':
            for style in styles:
                bot.send_message(message.from_user.id, f"Stil turi: {style.name}.")
        else:
            for style in styles:
                bot.send_message(message.from_user.id, f"Тип стиля: {style.name}.")

    elif message.text == "Xodimlar ro'yxati🤵‍♂️" or message.text == "Список сотрудников 🤵‍♂️":
        employees = Employee.objects.all()
        if admin.language == 'uz':
            for employee in employees:
                bot.send_message(message.from_user.id,
                                 f"Ism Familiyasi: {employee.full_name}.\nTelefon raqami: {employee.tel_number}.\nIsh tajribasi: {employee.work_experience} yil.")
        else:
            for employee in employees:
                bot.send_message(message.from_user.id,
                                 f"Имя Фамилия: {employee.full_name}.\nНомер телефона: {employee.tel_number}.\nОпыт работы: {employee.work_experience} год.")

    elif message.text == "Bosh menu📊" or message.text == "Главное меню📊":
        if admin.language == 'uz':
            bot.send_message(message.from_user.id, "Kerakli bo'limni tanlang", reply_markup=main_markup_user)
        else:
            bot.send_message(message.from_user.id, "Выберите нужный раздел", reply_markup=main_markup_user_ru)

    elif admin.permission == "employee" and message.text == "Reyting📈":
        bot.send_message(message.from_user.id, "Har 10 kunlik reyting xisobga olinadi")

    elif admin.permission == "user" and message.text == "Buyurtmalarim🛎" or message.text == "Мои заказы🛎":  # commands from the admin ("Kunlik Mijozlar", "Ish vaqti", "Reyting")
        order = Order.objects.filter(date=date.today().strftime("%Y-%m-%d"), bot_user__user_id=message.from_user.id)
        if order.exists():
            if admin.language == 'uz':
                markup = types.InlineKeyboardMarkup(row_width=2)
                btn = types.InlineKeyboardButton('❌ o`chirish', callback_data=f'del_or_time_{order.get().id}')
                btn1 = types.InlineKeyboardButton('✏ taxrirlash',
                                                  callback_data=f'edit_{order.get().id}_time_emp_{order.get().employee.user_id}')
                markup.add(btn, btn1)
                order = order.get()
                if order.status == False:
                    text = f'<b>Sana:</b> <i>{date.today().strftime("%Y-%m-%d")}</i>\n----------------------------------\n🔴 | {order.employee.full_name} | {order.order_time} | ☑️\n-------------------\n<b>Statusi:</b> <i>Qabul qilinmagan</i>\n-------------------\n'
                else:
                    text = f'<b>Sana:</b> <i>{date.today().strftime("%Y-%m-%d")}</i>\n----------------------------------\n🟢 | {order.employee.full_name} | {order.order_time} | ✅️\n-------------------\n<b>Statusi:</b> <i>Qabul qilindi</i>\n-------------------\n'
                bot.send_message(message.from_user.id, text, reply_markup=markup)
            else:
                markup = types.InlineKeyboardMarkup(row_width=2)
                btn = types.InlineKeyboardButton('❌ удалить', callback_data=f'del_or_time_{order.get().id}')
                btn1 = types.InlineKeyboardButton('✏ редактирование',
                                                  callback_data=f'edit_{order.get().id}_time_emp_{order.get().employee.user_id}')
                markup.add(btn, btn1)
                order = order.get()
                if order.status == False:
                    text = f'<b>Дата:</b> <i>{date.today().strftime("%Y-%m-%d")}</i>\n----------------------------------\n🔴 | {order.employee.full_name} | {order.order_time} | ☑️\n-------------------\n<b>Статус:</b> <i>Не принял</i>\n-------------------\n'
                else:
                    text = f'<b>Дата:</b> <i>{date.today().strftime("%Y-%m-%d")}</i>\n----------------------------------\n🟢 | {order.employee.full_name} | {order.order_time} | ✅️\n-------------------\n<b>Статус:</b> <i>принятие</i>\n-------------------\n'
                bot.send_message(message.from_user.id, text, reply_markup=markup)
        else:
            if admin.language == 'uz':
                bot.send_message(message.from_user.id, "Sizda hozircha kunlik buyurtma mavjud emas 🤷🏻‍♂️")
            else:
                bot.send_message(message.from_user.id, "У вас есть ежедневный заказ 🤷🏻‍♂️")

    elif admin.permission == "employee" and message.text == "Kunlik Mijozlar👨🏻‍⚖️":  # commands from the admin ("Kunlik Mijozlar", "Ish vaqti", "Reyting")
        order = Order.objects.filter(date=date.today().strftime("%Y-%m-%d"), employee__user_id=message.from_user.id)
        if order.exists():
            text = f'<b>Sana:</b> <i>{date.today().strftime("%Y-%m-%d")}</i>\n----------------------------------\n' \
                   f'<b>Mijozlarimiz:</b>\n----------------------------------\n'
            for i in order:
                text += f'🟢 | 🧔🏻‍♂️{i.bot_user.first_name} | 📱 {i.bot_user.tel_number} | ⌚️{i.order_time}\n-------------------\n'
            bot.send_message(message.from_user.id, text)
        else:
            bot.send_message(message.from_user.id, "Sizda hozircha kunlik mijoz mavjud emas yo'q 🤷🏻‍♂️")

    elif admin.permission == "employee" and message.text == "Ish vaqti⏰":  # commands from the admin ("Kunlik Mijozlar", "Ish vaqti", "Reyting")
        bot.send_message(message.from_user.id, "Kunlik ish vaqtlarini kiritishingiz mumkin ⏰:")
        bot.send_message(message.from_user.id, "Ish boshlash vaqtingizni kiriting ⏰:\n")
        emp = button_gen("❌ Bekor qilish ❌")
        current_employee = Employee.objects.filter(user_id=message.from_user.id).first()
        print(current_employee)
        if len(EmployeeSchedule.objects.filter(employee=current_employee)) > 0:
            new_schedule = EmployeeSchedule.objects.filter(employee=current_employee).first()
            new_schedule.status = True
            new_schedule.step = 1
            new_schedule.save()
            print(new_schedule.step)
        else:
            new_schedule = EmployeeSchedule.objects.create(
                employee=current_employee,
                start_time='8',
                end_time='22',
                step=1,
                status=True)
            new_schedule.save()
    
    elif admin.permission == "employee" and new_schedule.step == 1:
        if str(message.text).isdigit():
            new_schedule.start_time = message.text
            new_schedule.step += 1
            new_schedule.save()
            bot.send_message(message.from_user.id, "Ishni tugatish vaqtingizni kiriting⏰:")
        else:
            bot.send_message(message.from_user.id, "Iltimos, vaqtni soat hisobida, raqam holatida kiriting⏰:")

    elif admin.permission == "employee" and new_schedule.step == 2:
        if str(message.text).isdigit():
            new_schedule.end_time = message.text
            new_schedule.step = 0
            new_schedule.status = False
            new_schedule.save()
            bot.send_message(message.from_user.id, "Ish vaqti bazaga kiritildi ✅")
        else:
            bot.send_message(message.from_user.id, "Iltimos, vaqtni soat hisobida, raqam holatida kiriting⏰:")


    elif admin.permission == "admin" and message.text == "E'lon jo'natish🗣":  # commands from the admin
        message_step.step = 1
        ann_markup = button_gen("Orqaga↩️")
        message_step.save()
        bot.send_message(message.from_user.id, "Mijozlarga yuborilishi kerak bo'lgan xabarni jo'nating 📃:", reply_markup=ann_markup)


    elif admin.permission == "admin" and message.text == "Orqaga↩️":
        message_step.step = 0
        message_step.save()
        bot.send_message(message.from_user.id, "Bekor qilindi!", reply_markup=main_markup_admin)

    elif admin.permission == "admin" and message_step.step == 1:
        message_text = message.text  # receive the message from the admin
        for user in users:
            bot.send_message(user.user_id, message_text)  # send the message to each user
        message_step.step = 0
        message_step.save()
        bot.send_message(message.from_user.id, "Xabar mijozlarga muvaffaqiyatli jo'natildi ✅",
                         reply_markup=main_markup_admin)


    elif admin.permission == "admin" and message.text == "Orqaga⬅️":# the bug maybe here
        new_employee.step -= 1
        new_employee.save()
        cancel_func(message)  

    elif admin.permission == "admin" and message.text == "Bekor qilish❌":
        new_employee.delete()

        bot.send_message(message.from_user.id, "Bekor qilindi!", reply_markup=main_markup_admin)

    elif admin.permission == "admin" and message.text == "Xodimni o'chirish🙅‍♂️":
        xodimlar_markup = types.InlineKeyboardMarkup(row_width=2)
        if len(employee) > 0:
            for i in employee:
                xodimlar_markup.add(types.InlineKeyboardButton(f"{i.full_name}", callback_data=f"{i.tel_number} delete"))
            bot.send_message(message.from_user.id, "O'chirilishi kerak bo'lgan xodimni tanlang:",
                             reply_markup=xodimlar_markup)
        else:
            bot.send_message(message.from_user.id, "Hozirda xodim mavjud emas🤷🏻‍♂️", reply_markup=main_markup_admin)

    elif admin.permission == "admin" and message.text == "Statistika📈":
        if len(Order.objects.all()) > 0:
            orders = Order.objects.all().count()
            users = len(BotUser.objects.filter(permission="user"))
            bot.send_message(message.from_user.id,
                             f"Barcha mijozlar soni {users} ta.\nBarcha buyurtmalar soni {orders} ta.")
        else:
            bot.send_message(message.from_user.id, "Hozirda buyurtmalar mavjud emas!")

    elif admin.permission == "admin" and message.text == "Yangi xodim qo'shish👨‍💼":  # adding employee
        form_markup = button_gen("Bekor qilish❌")
        new_emp = Employee.objects.create(
            step=1,
            user_id=123,
            is_created=True
        )
        new_emp.save()
        bot.send_message(message.from_user.id, "Xodimning ism familiyasini kiriting 🤵:", reply_markup=form_markup)

    elif admin.permission == "admin" and new_employee.step == 1:
        new_employee.full_name = message.text
        new_employee.step += 1
        new_employee.save()
        bot.send_message(message.from_user.id, "Xodimning telefon raqamini 998xxxxxxxxx ko'rinishida kiriting 📱:",
                         reply_markup=form_main_markup)

    elif admin.permission == "admin" and new_employee.step == 2:
        if str(message.text).isdigit():
            new_employee.tel_number = message.text
            new_employee.step += 1
            new_employee.save()
            bot.send_message(message.from_user.id, "Xodimning ish tajriba muddatini kiriting 🤵:")
        else:
            bot.send_message(message.from_user.id,
                             "Iltimos to\'g\'ri ma\'lumot kiriting🙅‍♂️\nXodimning telefon raqamini 998xxxxxxxxx ko'rinishida kiriting 📱:")

    elif admin.permission == "admin" and new_employee.step == 3:
        if str(message.text).isdigit():
            new_employee.work_experience = message.text
            new_employee.step = 0
            new_employee.is_created = False
            new_employee.active = True
            new_employee.save()
            bot.send_message(message.from_user.id, "Muvaffaqiyatli qo'shildi ✅ ", reply_markup=main_markup_admin)
        else:
            bot.send_message(message.from_user.id,
                             'Iltimos to\'g\'ri ma\'lumot kiriting🙅‍♂️\nIshchining ish tajriba muddatini kiriting 🤵:')


class TimeReception:
    def __init__(self):
        self.now = datetime.now()
        self.start_time = int(self.now.strftime('%H'))
        self.today = date.today()

    def now_hour(self):
        return self.start_time

    def day(self):
        return self.today.strftime("%Y-%m-%d")

    def time_r(self, n):
        if int(self.now.strftime("%M")) > 30:
            return (self.now + timedelta(minutes=n * 30 + abs(60 - int(self.now.strftime('%M'))))).strftime('%H:%M')
        else:
            return (self.now + timedelta(minutes=n * 30 + abs(30 - int(self.now.strftime('%M'))))).strftime('%H:%M')


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):  # '10:30'
    bot_user = BotUser.objects.get(user_id=call.from_user.id)
    if call.data == 'dislike':
        if bot_user.language == 'uz':
            bot.answer_callback_query(callback_query_id=call.id, text='Kechirasiz bu vaqt band qilingan!')
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Извините, занят!')
    elif 'del_or_time' in call.data:
        or_id = str(call.data).split('_')[3]
        order = Order.objects.get(id=int(or_id))
        order.delete()
        if bot_user.language == 'uz':
            bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id,
                                  text=f"Buyurtmangiz o'chirildi!")
        else:
            bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id, text=f"Ваш заказ удален!")
    elif 'accept' in call.data:
        or_id = str(call.data).split('_')[1]
        order = Order.objects.get(id=int(or_id))
        order.status = True
        order.save()
        if bot_user.language == 'uz':
            bot.send_message(order.bot_user.user_id,
                             text=f"Buyurtmangiz qabul qilindi tanlagan\nvaqtingizga borishingiz mumkin 🙂")
        else:
            bot.send_message(order.bot_user.user_id,
                             text=f"Ваш заказ принят, и вы можете идти в удобное для вас время 🙂")
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id, text=f"Mijoz qabul qilindi!")
    elif 'rejected' in call.data:
        or_id = str(call.data).split('_')[1]
        order = Order.objects.get(id=int(or_id))
        order.delete()
        if bot_user.language == 'uz':
            bot.send_message(order.bot_user.user_id, text=f"Iltimos qaytadan urinib ko'ring 🙂")
        else:
            bot.send_message(order.bot_user.user_id, text=f"Пожалуйста, попробуйте еще раз 🙂")
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id,
                              text=f"Buyurtmangiz bekor qilindi!")
    elif 'delete' in call.data:
        employee_id = str(call.data).split(' ')[0]
        employee = Employee.objects.get(tel_number=employee_id)
        employee.delete()
        if len(BotUser.objects.filter(tel_number=employee_id)) > 0:
            bot_user = BotUser.objects.get(tel_number=employee_id)
            bot_user.delete()
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id,
                              text=f"{employee.full_name} bazadan o'chirildi!")
    elif ':30' in call.data or ':00' in call.data:
        employee_id = str(call.data).split('_')[3]
        order_time = str(call.data).split('_')[1]
        user = BotUser.objects.get(user_id=call.from_user.id)
        employee = Employee.objects.get(user_id=employee_id)
        orders = Order.objects.filter(date=date.today().strftime("%Y-%m-%d"), bot_user__user_id=call.from_user.id)
        if orders.exists():
            if bot_user.language == 'uz':
                bot.answer_callback_query(callback_query_id=call.id, text='Kechirasiz, sizda allaqachon buyurtma bor!')
            else:
                bot.answer_callback_query(callback_query_id=call.id, text='Извините, у вас уже есть заказ')
        else:
            order = Order.objects.create(
                bot_user=user,
                employee=employee,
                order_time=order_time
            )
            order.save()
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn = types.InlineKeyboardButton('✅ qabul qilish', callback_data=f'accept_{order.id}')
            btn1 = types.InlineKeyboardButton('❌ rad etish', callback_data=f'rejected_{order.id}')
            markup.add(btn, btn1)
            bot.send_message(employee_id, f"Sizga ⌚️{order.order_time} ga mijoz murojaat qildi", reply_markup=markup)
            if bot_user.language == 'uz':
                bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id,
                                      text="Buyurtmangiz qabul qilindi✅")
            else:
                bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id, text="Ваш заказ принят✅")

    elif '_time_emp_' in call.data or Employee.objects.filter(user_id=call.data).exists():
        if '_time_emp_' in call.data:
            or_id = str(call.data).split('_')[1]
            emp_id = str(call.data).split('_')[4]
            order = Order.objects.get(id=or_id)
            order.delete()
            call.data = emp_id
        employee = Employee.objects.get(user_id=int(call.data))
        new_schedule = EmployeeSchedule.objects.filter(employee=employee).first()
        time_markup = types.InlineKeyboardMarkup(row_width=3)
        n = 0
        time_r = TimeReception()
        start = int(new_schedule.start_time) # start time 
        end = int(new_schedule.end_time) # end time     
        if start < time_r.now_hour() < end:
            if time_r.now_hour() > 8:
                start = time_r.now_hour()
            if end - start % 3 == 0:
                full_time = ((end - start)*2)//3
            else:
                full_time = (((end - start)*2)//3) + 1 
            for xodim in range(full_time):
                btn = f"{time_r.time_r(n + 0)}"
                btn_back = f"time_{time_r.time_r(n + 0)}_userid_{call.data}"
                btn1 = f"{time_r.time_r(n + 1)}"
                btn_back1 = f"time_{time_r.time_r(n + 1)}_userid_{call.data}"
                btn2 = f"{time_r.time_r(n + 2)}"
                btn_back2 = f"time_{time_r.time_r(n + 2)}_userid_{call.data}"
                if Order.objects.filter(order_time=btn, date=time_r.day(), employee__user_id=call.data).exists():
                    btn = f"🟢 {time_r.time_r(n + 0)}"
                    btn_back = f"dislike"
                if Order.objects.filter(order_time=btn1, date=time_r.day(), employee__user_id=call.data).exists():
                    btn1 = f"🟢 {time_r.time_r(n + 1)}"
                    btn_back1 = f"dislike"
                if Order.objects.filter(order_time=btn2, date=time_r.day(), employee__user_id=call.data).exists():
                    btn2 = f"🟢 {time_r.time_r(n + 2)}"
                    btn_back2 = f"dislike"
                if int(time_r.time_r(n + 0)[0:2]) == end:
                    break
                elif int(time_r.time_r(n + 1)[0:2]) == end:
                    time_markup.add(types.InlineKeyboardButton(btn, callback_data=btn_back))
                    break
                elif int(time_r.time_r(n + 2)[0:2]) == end:
                    time_markup.add(types.InlineKeyboardButton(btn, callback_data=btn_back),
                                    types.InlineKeyboardButton(btn1, callback_data=btn_back1))
                    break
                else:
                    time_markup.add(types.InlineKeyboardButton(btn, callback_data=btn_back),
                                    types.InlineKeyboardButton(btn1, callback_data=btn_back1),
                                    types.InlineKeyboardButton(btn2, callback_data=btn_back2))
                n += 3
            if bot_user.language == 'uz':
                bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id,
                                      text=f"{employee.full_name} ni kun tartibi", reply_markup=time_markup)
            else:
                bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id,
                                      text=f"{employee.full_name} повестка дня", reply_markup=time_markup)
        else:
            if bot_user.language == 'uz':
                bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id,
                                      text="Bizda ish vaqti 08:00 dan 21:00 gacha.")
            else:
                bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id,
                                      text="Наше рабочее время с 08:00 до 21:00.")


def cancel_func(message):
    new_employee = Employee.objects.filter(is_created=True).first()
    form_markup = button_gen("Orqaga", "Bekor qilish")
    if new_employee.step == 1:
        bot.send_message(message.from_user.id, 'Xodimning ism familiyasini kiriting 🤵:', reply_markup=form_markup)
    elif new_employee.step == 2:
        bot.send_message(message.from_user.id, "Xodimning telefon raqamini 998xxxxxxxxx ko'rinishida kiriting 📱:")
    elif new_employee.step == 3:
        bot.send_message(message.from_user.id, 'Xodimning ish tajriba muddatini kiriting 🤵:')