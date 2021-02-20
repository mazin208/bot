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

WEBHOOK_HOST = 'makuzo.herokuapp.com'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)


# WebhookHandler, process webhook calls
class WebhookHandler(BaseHTTPRequestHandler):
    server_version = "WebhookHandler/1.0"

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == WEBHOOK_URL_PATH and \
           'content-type' in self.headers and \
           'content-length' in self.headers and \
           self.headers['content-type'] == 'application/json':
            json_string = self.rfile.read(int(self.headers['content-length']))

            self.send_response(200)
            self.end_headers()

            update = telebot.types.Update.de_json(json_string)
            bot.process_new_messages([update.message])
        else:
            self.send_error(403)
            self.end_headers()



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

# Remove webhook, it fails sometimes the set if there is a previous webhook
#bot.remove_webhook()

# Set webhook
# Beacuse telegram bot api server will check webhook server is alive.
# Here we need set webhook after server started manually.
#bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
#                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Start server
httpd = HTTPServer((WEBHOOK_LISTEN, WEBHOOK_PORT),
                   WebhookHandler)

httpd.socket = ssl.wrap_socket(httpd.socket,
                               certfile=WEBHOOK_SSL_CERT,
                               keyfile=WEBHOOK_SSL_PRIV,
                               server_side=True)

httpd.serve_forever()
