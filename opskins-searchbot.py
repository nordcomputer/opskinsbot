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
global waxprice
global opskinskey
global bottoken
bottoken="TOKEN-FROM-YOUR-TELEGRAM-BOT"
opskinskey='YOUR-OPSKINS-KEY'
waxurl='https://api.coinmarketcap.com/v1/ticker/WAX/'
response = urllib2.urlopen(waxurl)
html = response.read();
parsed_json=json.loads(html)
waxpricelist=parsed_json
for f in waxpricelist:
    waxprice=float(f['price_usd'])
    print (waxprice)


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
    for value in values:

        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Just type /games to get a List of supported games and choose one. After that, you can search for your favorite item!')


        # do something here



def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Hi! Just type /games to get a List of supported games and choose one. After that, you can search for your favorite item!')


def echo(bot, update):
    empfangen=update.message.text

    getItem(bot, update, empfangen)

def getItem( bot, update,name):
    empfangen=urllib2.quote(name)
    contents = 'https://api.opskins.com/ISales/Search/v2/?app='+appid+'_'+contextid+'&search_item='+empfangen+'&key='+opskinskey
    #update.message.reply_text(contents)
    response = urllib2.urlopen(contents)
    html = response.read()
    response.close() # best practice to close the file'
    parsed_json = json.loads(html)
    sales=parsed_json['response']['sales']
    x=0
    global chat
    chat=str(update.message.chat_id)
    print(chat)
    my_list=None
    my_list=list()
    pic={}
    for f in sales:
        name=f['market_name']
        pic.update({name:f['img']})
        print(pic[name])
        my_list.append(name)
        x=x+1
    my_list=list(set(my_list))
    for g in my_list:
        keyboard = [[InlineKeyboardButton(g, callback_data=g)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Found this:', reply_markup=reply_markup)
        bot.sendPhoto(chat_id=chat, photo=pic[g])
    y=0

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def button_callback(bot, update):
    # data is the callback_data where you declared in the buttons
    query = update.callback_query.data
    name=query
    item=name
    tname=update.callback_query.message
    print(item)
    if item in supportedgames:
        global appid
        appid=str(item)
        gamesurl='https://api.opskins.com/ISales/GetSupportedSteamApps/v1?key='+opskinskey
        response = urllib2.urlopen(gamesurl)
        html = response.read();    
        parsed_json=json.loads(html)
        gameslistjson=parsed_json['response']['apps']
        for f in gameslistjson:
            if f['appid']==item:
                print(f['contextid'])
                global contextid
                contextid=str(f['contextid'])
        bot.send_message(chat_id=chat, text="done")
    else:
        query = update.callback_query.data
        
        name=query
        priceurl='https://api.opskins.com/IPricing/GetSuggestedPrices/v1/?appid='+appid+'&items[]='+query+'&key='+opskinskey    
        response2 = urllib2.urlopen(priceurl)
        html = response2.read();
        
        parsed_json=json.loads(html)
        marketprice=parsed_json['response']['prices'][name]['market_price']
        # marketprice=('123')
        marketprice=int(marketprice)
        marketprice=marketprice/100;
        wax=marketprice/waxprice
        wax=round(wax,2)
        wax=str(wax)
        bot.send_message(chat_id=chat, text=name+': \r\n Marketprice (USD): '+str(marketprice)+' USD \r\n ~'+wax+' WAX')
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

def games(bot, update):
    global chat
    chat=str(update.message.chat_id)
    print(chat)
    gamesurl='https://api.opskins.com/ISales/GetSupportedSteamApps/v1?key='+opskinskey
    response = urllib2.urlopen(gamesurl)
    html = response.read();    
    parsed_json=json.loads(html)
    gameslistjson=parsed_json['response']['apps']
    buttons=list()
    b=1
    buttons1=list()
    buttons2=list()
    buttons3=list()
    buttons4=list()
    buttons5=list()
    buttons6=list()
    buttons7=list()
    buttons8=list()
    buttons9=list()
    for f in gameslistjson:
        name=f['name']
        app=f['appid']
       
        app=str(app)
        global supportedgames
        supportedgames.append(app)
        supportedgames=list(set(supportedgames))
        button=InlineKeyboardButton(name, callback_data=app)
        if b <= 3:
            buttons1.append(button)
        elif b <=6:
            buttons2.append(button)
        elif b <=9:
            buttons3.append(button)
        elif b <=12:
            buttons4.append(button)
        elif b <=15:
            buttons5.append(button)
        elif b <=18:
            buttons6.append(button)
        elif b <=21:
            buttons7.append(button)
        elif b <=24:
            buttons8.append(button)
        else:
            buttons9.append(button)
        b=b+1

    reply_markup = InlineKeyboardMarkup([buttons1,buttons2,buttons3,buttons4,buttons5,buttons6,buttons7,buttons8,buttons9],resize_keyboard=False)
    update.message.reply_text('Choose game:', reply_markup=reply_markup)
def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(bottoken)

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

