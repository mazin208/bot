try:
    # Python 2
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    # Python 3
    from http.server import BaseHTTPRequestHandler, HTTPServer

import logging
import ssl
import pafy
import telebot
from telebot import types
from tqdm import tqdm 
import requests
import os

API_TOKEN = '<api_token>'

PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(TOKEN)
# add handlers
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook("https://makuzo.herokuapp.com/" + TOKEN)
updater.idle()

bot = telebot.TeleBot(API_TOKEN)


x = bot.get_me()

#handling commands - /start
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
 bot.send_message(message.chat.id, "Welcome user")

 
 
 
 #markup = types.ForceReply(selective=False)
 #markup = types.ReplyKeyboardMarkup()
 #itembtna = types.KeyboardButton('a')
 #itembtnv = types.KeyboardButton('v')
 #itembtnc = types.KeyboardButton('c')
 #itembtnd = types.KeyboardButton('d')
 #itembtne = types.KeyboardButton('e')
 #markup.row(itembtna, itembtnv)
 #markup.row(itembtnc, itembtnd, itembtne)
 #bot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)
 

#handling commands - /motivate
@bot.message_handler(commands=["motivate"])
def send_quotes(message):
 quote= requests.request(url="https://api.quotable.io/random",method='get')
 bot.reply_to(message, quote.json()["content"]) 
 
@bot.message_handler(commands=["down"])
def send_video(message):
 markup = types.ForceReply(selective=False)
 url = bot.send_message(message.chat.id, "Send me the URL:", reply_markup=markup)
 myvid = pafy.get_playlist(url)
 bot.reply_to(message, str(myvid))
 for i in tqdm (range (100), desc="Loading..."): 
    pass


print(x)
