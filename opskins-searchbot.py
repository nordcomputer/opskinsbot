#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.
Simple Bot to get prices for items from opskins
"""
from __future__ import division
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler, InlineQueryHandler)

import urllib.request as urllib2
import json
import requests
import logging
global appid
global supportedgames
global contextid
global waxurl
global opskinskey
global bottoken
waxurl='https://api.coinmarketcap.com/v2/ticker/2300/?convert=USD'
bottoken="TOKEN-FROM-YOUR-TELEGRAM-BOT"
opskinskey='YOUR-OPSKINS-KEY'

contextid='2'
supportedgames=list()
appid='227300'
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def remove_duplicates(values):
    output = []
    seen = set()
    response = urllib2.urlopen(waxurl)
    html = response.read();
    parsed_json=json.loads(html)

    for value in values:

        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Just type /games to get a List of supported games and choose one. After that, you can search for your favorite item!')





def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Hi! Just type /games to get a List of supported games and choose one. After that, you can search for your favorite item!')

def echo(update,context):
    empfangen=update.message.text
    # getItem(update, empfangen)
    # print(empfangen)
    getItem(update,empfangen)



def getItem(update, context):
    empfangen=context
    #print(empfangen)
    appid='730'
    # contents = 'https://api.opskins.com/ISales/Search/v2/?app='+appid+'&search_item='+empfangen+'&key='+opskinskey
    contents = 'https://api.opskins.com/ISales/Search/v2/?app='+appid+'_'+contextid+'&search_item='+empfangen+'&key='+opskinskey

    #update.message.reply_text(contents)
    response = urllib2.urlopen(contents)
    html = response.read()
    # print(contents)
    response.close() # best practice to close the file'
    parsed_json = json.loads(html)
    sales=parsed_json['response']['sales']
    x=0
    global chat
    chat=str(update.message.chat_id)
    #print(chat)
    my_list=None
    my_list=list()
    pic={}
    for f in sales:
        name=f['market_name']
        pic.update({name:f['img']})
        #print(pic[name])
        my_list.append(name)
        x=x+1
    my_list=list(set(my_list))
    for g in my_list:
        keyboard = [[InlineKeyboardButton(g, callback_data=g)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Found this:', reply_markup=reply_markup)
        # bot.sendPhoto(chat_id=chat, photo=pic[g])
        # bot.send_photo(pic[g])
        #update.send_photo(chat_id=chat, photo='https://telegram.org/img/t_logo.png')
    y=0

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def button_callback(update,context):
    # data is the callback_data where you declared in the buttons
    query = update.callback_query
    name=query.data
    item=name
    #tname=update.callback_query.message

    if item in supportedgames:
        global appid
        appid=str(item)
        gamesurl='https://api.opskins.com/ISales/GetSupportedSteamApps/v1?key='+opskinskey
        response = urllib2.urlopen(gamesurl)
        html = response.read();
        parsed_json=json.loads(html)
        gameslistjson=parsed_json['response']['apps']
        # print(item)
        for f in gameslistjson:
            if f['appid']==item:

                global contextid
                contextid=str(f['contextid'])
        # update.message.reply_text('OK')
    return

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def games(update, context):
    global chat
    chat=str(update.message.chat_id)
    # chat=str('test')
    # print(chat)
    gamesurl='https://api.opskins.com/ISales/GetSupportedSteamApps/v1?key='+opskinskey
    response = urllib2.urlopen(gamesurl)
    html = response.read();
    parsed_json=json.loads(html)
    gameslistjson=parsed_json['response']['apps']
    buttons=list()
    line=list()
    foo=0
    bar=0
    linie=list()
    for f in gameslistjson:
        name=f['name']
        app=f['appid']
        app=str(app)
        global supportedgames
        supportedgames.append(app)
        supportedgames=list(set(supportedgames))
        button=InlineKeyboardButton(name, callback_data=app)

        if foo<=1:
            linie.append(button)
            foo=foo+1
        else:
            linie=[]
            foo=0
            linie.append(button)
            line.append(linie)







    reply_markup = InlineKeyboardMarkup(line,resize_keyboard=False)
    update.message.reply_text('Choose game:', reply_markup=reply_markup)



def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(bottoken, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("games", games))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(CallbackQueryHandler(button_callback))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':

    main()
