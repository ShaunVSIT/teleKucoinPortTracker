import constants as keys
from telegram import ParseMode
from telegram.ext import *
import port

# I'm using constants.py to store my keys, you'll need to add your own keys in that file
TELE_API_KEY = keys.TELE_API_KEY # Your bot API Key goes here

# Storing chat IDs so only my accounts can use the bot
chatID1 = int(keys.chatID1)
chatID2 = int(keys.chatID2)

print('Bot Started...')


def start_command(update, context):
  update.message.reply_text(
    "Hello! Only cool kids allowed beyond this point ;)")


def help_command(update, context):
  response = ""
  response += "What's good my guy"
  response += "\n\n"
  response += "sned /portfolio to pull portfolio"
  response += "\n\n"
  response += "Or sned /price <<ticker>> for coin price"
  response += "\n\n"
  response += "/price with no args returns BTC and ETH only"
  update.message.reply_text(response)


def port_command(update, context):

  if update.message.chat_id == chatID1:
    response = port.getPort()
    update.message.reply_text(f'<pre>{response}</pre>',parse_mode=ParseMode.HTML)
  elif update.message.chat_id == chatID2:
    response = port.getPort()
    update.message.reply_text(f'<pre>{response}</pre>', parse_mode=ParseMode.HTML)
  else:
    response = "ACCESS DENIED, SELF DESTRUCT SEQUENCE INITIATED"
    # update.message.reply_text(f'```{response}```', parse_mode=ParseMode.MARKDOWN_V2)
    update.message.reply_text(f'<pre>{response}</pre>',parse_mode=ParseMode.HTML)

def price_command(update, context):
  if update.message.chat_id == chatID1 or chatID2:
    if len(context.args) == 0:
      response = port.getPrice()
      update.message.reply_text(f'<pre>{response}</pre>',parse_mode=ParseMode.HTML)
    else:
      ticker = str(context.args[0]).upper()
      response = port.getPrice(ticker)
      update.message.reply_text(f'<pre>{response}</pre>',parse_mode=ParseMode.HTML)
  else:
    response = "ACCESS DENIED, SELF DESTRUCT SEQUENCE INITIATED"
    update.message.reply_text(f'<pre>{response}</pre>',parse_mode=ParseMode.HTML)

def chatID_command(update, context):
  chatID = update.message.chat_id
  update.message.reply_text(chatID)


def userID_command(update, context):
  userID = update.message.from_user.first_name
  update.message.reply_text(userID)

#Lil easter egg for my gf
def bbEE(update, context):
  update.message.reply_text("Hi Bubs, me is a pro coder now huehuehue")


def main():
  updater = Updater(TELE_API_KEY, use_context=True)
  dp = updater.dispatcher
  dp.add_handler(CommandHandler("start", start_command))
  dp.add_handler(CommandHandler("help", help_command))
  dp.add_handler(CommandHandler("portfolio", port_command))
  dp.add_handler(CommandHandler("price", price_command))
  dp.add_handler(CommandHandler("chatID", chatID_command))
  dp.add_handler(CommandHandler("userID", userID_command))
  dp.add_handler(CommandHandler("bb", bbEE))
  updater.start_polling()
  updater.idle()


main()