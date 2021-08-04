import telebot
from bb_login import get_course_list
from models import User
from telebot import types


bot = telebot.TeleBot("1907064165:AAEWy1iEaYPgaKD1z2D0XuF6wYwUoM9M1LY", parse_mode=None)
all_Users = {}


@bot.message_handler(['start', 'help'])
def welcome_message(message):
    bot.reply_to(message, "Hello! Send /login to get logged in.")


@bot.message_handler(['login'])
def login_handler(message):
    new_user = User(message.chat.id)
    all_Users[message.chat.id] = new_user
    msg = bot.reply_to(message, "Send me your ID, please:")
    bot.register_next_step_handler(msg, get_id_ask_for_pass)


def get_id_ask_for_pass(message):
    all_Users[message.chat.id].bb_id = message.text
    msg = bot.reply_to(message, "Good! Now, send me your password:")
    bot.register_next_step_handler(msg, get_pass_save)


def get_pass_save(message):
    all_Users[message.chat.id].psw = message.text
    res = get_course_list(all_Users[message.chat.id])
    if res[0] != 200:
        bot.reply_to(message, "Something went wrong. Please try again with /login")
    else:
        bot.reply_to(message, "Thank you! You will get logged in soon...")
        all_Users[message.chat.id].update_course_list(res[1])
        course_list = "Courses:\n"
        for course in res[1]:
            course_list += course.name + "\n"
        bot.send_message(message.chat.id, course_list)


@bot.message_handler(["grades"])
def get_grades_handler(message):
    if (message.chat.id not in all_Users.keys()) or not all_Users[message.chat.id].bb_id or not all_Users[message.chat.id].psw:
        bot.send_message(message.chat.id, "Please, LOG IN first with /login command.")
    else:
        markup = types.ReplyKeyboardMarkup()
        for course in all_Users[message.chat.id].course_list:
            item_btn = types.KeyboardButton(course.name)
            markup.row(item_btn)
        bot.send_message(message.chat.id, "Choose course:", reply_markup=markup)
        types.ReplyKeyboardRemove(markup)


bot.polling()
