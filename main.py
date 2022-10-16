import constants as keys
import telebot

bot = telebot.TeleBot(keys.TELE_API_KEY)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "What's good my guy, sned /update to pull port")