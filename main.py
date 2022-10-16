import constants as keys
import telebot

bot = telebot.TeleBot(keys.TELE_API_KEY)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "What's good my guy, sned /update to pull port")

@bot.message_handler(commands=['update'])
def update_port(message):
	if message.chat.id == keys.chatID1 or keys.chatID2:
		bot.send_message(message.chat.id, "Portfolio goes here soon")
	else:
		bot.send_message(message.chat.id, "sorry buddy, only true degens are allowed here")

bot.polling()