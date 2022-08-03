from telebot import *


def button_gen(*args, row_width=2, request_contact=False, request_location=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=row_width)
    if 1 < len(args) and len(args) % 2 == 0:
        for i in range(0, len(args), 2):
            btn1 = types.KeyboardButton(f"{args[i]}", request_contact=request_contact, request_location=request_location)
            btn2 = types.KeyboardButton(f"{args[i+1]}", request_contact=request_contact, request_location=request_location)
            markup.add(btn1, btn2)
    elif len(args) == 1:
        btn1 = types.KeyboardButton(f"{args[0]}", request_contact=request_contact, request_location=request_location)
        markup.add(btn1)
    else:
        for i in range(0, len(args) // 2, 2):
            btn1 = types.KeyboardButton(f"{args[i]}", request_contact=request_contact, request_location=request_location)
            btn2 = types.KeyboardButton(f"{args[i+1]}", request_contact=request_contact, request_location=request_location)
            markup.add(btn1, btn2)
        if len(args) % 2 == 1:
            btn1 = types.KeyboardButton(f"{args[-1]}", request_contact=request_contact, request_location=request_location)
            markup.add(btn1)
    return markup
