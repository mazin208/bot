#required packages
import telebot
import requests
import os
import json#Config vars
with open("config.json") as f:
 token = json.load(f)#initialise bot
bot = telebot.TeleBot(token["telegramToken"])
x = bot.get_me()

#handling commands - /start
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
 bot.send_message(message.chat.id, "Welcome user")
 

#handling commands - /motivate
@bot.message_handler(commands=["motivate"])
def send_quotes(message):
 quote= requests.request(url="https://api.quotable.io/random",method='get')
 bot.reply_to(message, quote.json()["content"]) 
 
print(x)#pool~start the bot
bot.polling()
