#required packages
import telebot
import requests
import os
import json
from time import sleep

#Config vars
with open('config.json') as f:
  token = json.load(f)

#initialise  bot
bot = telebot.TeleBot(token['telegramToken'])
x = bot.get_me()

#handling /commands
@bot.message_handler(commands=['motivate'])
def send_quotes(message):
        quote = requests.request(url='https://api.quotable.io/random',method='get')
        bot.send_message(message.chat.id, quote.json()['content'])

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  bot.send_message(message.chat.id, "Welcome user")
#Intitialize YouTube downloader
ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

# works when /ytdl <link> is given
@bot.message_handler(commands=['ytdl'])
def down(msg):
    args = msg.text.split()[1]
    try:
        with ydl:
            result = ydl.extract_info(
                args,
                download=False  # We just want to extract the info
            )

        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result
        
        for i in video['formats']:
            link = '<a href=\"' + i['url'] + '\">' + 'link' + '</a>'
            if i.get('format_note'):
                bot.reply_to(msg, 'Quality-' + i['format_note'] + ': ' + link, parse_mode='HTML')
            else:
                bot.reply_to(msg, link, parse_mode='HTML', disable_notification=True)
    except:
        bot.reply_to(msg, 'This can\'t be downloaded by me')
print(x)
#pool~start the bot
bot.polling()
