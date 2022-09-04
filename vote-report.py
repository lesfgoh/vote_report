


import time
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from telegram import *
from telegram.ext import *
from requests import *


def findvote(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://finder.kujira.app/harpoon-4/address/'+url)
##    try:
##        elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located(By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[3]/div/div/table/tbody/tr[1]/td[3]/span"))
##    finally:
    time.sleep(2)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    if soup.find(class_="tag").text[:-1]== 'MsgVote':
        return True
    else:
        return False
    driver.close()



API_KEY = 'insert token here'



# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
# Best practice would be to replace context with an underscore,
# since context is an unused local variable.

def start(update: Update, context: CallbackContext) -> None:
    """Sends explanation on how to use the bot."""
    update.message.reply_text('Hi! I\'m a bot run by Les F Goh. Click /info to learn more.')

def info (update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send command /report <address> to check whether the validator you\'ve chosen has voted recently. If no address is given, I\'ll default to the kujiDAO wallet.')

def report(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Loading...')
    if context.args:
        update.message.reply_text(findvote(context.args[0]))
    else:
        update.message.reply_text(findvote('kujira1546l88y0g9ch5v25dg4lmfewgelsd3v9a0npdt'))
    
def messageHandler(update: Update, context: CallbackContext):
    update.message.reply_text('Sorry, this message isn\'t recognised.')

def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(API_KEY)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("report", report))
    dispatcher.add_handler(CommandHandler("info", info))
    dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()










