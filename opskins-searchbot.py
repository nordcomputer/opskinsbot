#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.
Simple Bot to get prices for items from opskins
"""
from __future__ import division
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler, InlineQueryHandler)
import urllib.request as urllib2
import urllib.parse as urllib3
import json
import requests
import logging
import base64
global appid
global supportedgames
global contextid
global gamename
global waxurl
global opskinskey
global bottoken
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from requests import Request, Session
from credentials import (bottoken,opskinskey,cmcapikey,cmcsandboxkey,activatecmcsandbox)
waxurl='https://api.coinmarketcap.com/v2/ticker/2300/?convert=USD'
contextid=''
supportedgames=list()
appid=''
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def remove_duplicates(values):
    output = []
    seen = set()
    response = urllib2.urlopen(waxurl)
    html = response.read();
    response.close()
    parsed_json=json.loads(html)
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


def start(update,context):
    """Send a message when the command /start is issued."""
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hi! Just type /games to get a List of supported games and choose one. After that, you can search for your favorite item!')

def help(update, context):
    """Send a message when the command /help is issued."""
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hi! Just type /games to get a List of supported games and choose one. After that, you can search for your favorite item!')

def echo(update,context):
    empfangen=update.message.text
    if appid=='':
        context.bot.send_message(chat_id=update.effective_chat.id, text='Hi! Just type /games to get a List of supported games and choose one. After that, you can search for your favorite item!')
    else:
        getItem(update,context)


def getItem(update, context):
    empfangen=update.message.text
    empfangen=urllib3.quote(empfangen)
    global contextid
    searchurl = 'https://api.opskins.com/ISales/Search/v2/?app='+appid+'_'+contextid+'&search_item='+empfangen
    html = getfromurl(searchurl)
    parsed_json = json.loads(html)
    sales=parsed_json['response']['sales']
    my_list=None
    my_list=list()
    pic={}
    if len(sales) > 0:
        for f in sales:
            name=f['market_name']
            pic.update({name:f['img']})
            my_list.append(name)
        my_list=list(set(my_list))
        for g in my_list:
            keyboard = [[InlineKeyboardButton(g, callback_data=g)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('Found this:', reply_markup=reply_markup)
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=pic[g])
    else:
        update.message.reply_text('no results found')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def button_callback(update,context):
    try:
        # data is the callback_data where you declared in the buttons
        query = update.callback_query
        name=query.data
        item=name
        if item in supportedgames:
            global appid
            appid=str(item)
            gamesurl='https://api.opskins.com/ISales/GetSupportedSteamApps/v1'
            html=getfromurl(gamesurl)
            parsed_json=json.loads(html)
            gameslistjson=parsed_json['response']['apps']
            for f in gameslistjson:
                if str(f['appid'])==item:
                    gamename=str(f['name'])
                    global contextid
                    contextid=str(f['contextid'])
                    context.bot.send_message(chat_id=update.effective_chat.id,
                    text='ok - game is set to <b>'+gamename+'</b>\r\nYou can now search for items by typing your search phrase',
                    parse_mode=ParseMode.HTML)
            return
        else:
            query = update.callback_query.data
            name=query
            query=urllib3.quote(query)
            priceurl='https://api.opskins.com/IPricing/GetSuggestedPrices/v1/?appid='+appid+'&items[]='+query
            html=getfromurl(priceurl)
            parsed_json=json.loads(html)
            marketprice=parsed_json['response']['prices'][name]['opskins_lowest_price']
            if marketprice==None:
                marketprice='0'
            waxprice=getcmcprice()
            marketprice=int(marketprice)
            marketprice=marketprice/100;
            wax=marketprice/waxprice
            wax=round(wax,2)
            wax=str(wax)
            context.bot.send_message(chat_id=update.effective_chat.id, text=name+': \r\nLowest Price on Opskins (USD): '+str(marketprice)+' USD\r\n ~'+wax+' WAX')
            return
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Please type /games first, to get a list of supported games.')
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
    gamesurl='https://api.opskins.com/ISales/GetSupportedSteamApps/v1'
    html=getfromurl(gamesurl)
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


def getfromurl(url):
    data = opskinskey+":"
    encodedBytes = base64.b64encode(data.encode("utf-8"))
    myToken = str(encodedBytes, "utf-8")
    request = urllib2.Request(url)
    request.add_header("Authorization", "Basic %s" % myToken)
    html = urllib2.urlopen(request).read()
    urllib2.urlopen(request).close()
    return html


def getcmcprice():
    if activatecmcsandbox==True:
        url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        ckey = cmcsandboxkey
    else:
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        ckey = cmcapikey

    parameters = {
      'id':'2300'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': ckey,
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      parsed_json=json.loads(response.text)
      marketprice=parsed_json['data']['2300']['quote']['USD']['price']
      return marketprice
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

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
