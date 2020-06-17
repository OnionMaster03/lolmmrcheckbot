#!/bin/python3.7

import requests
from pprint import pprint
import json
import urllib.parse
from telegram.ext import MessageHandler, CommandHandler, Updater
import logging
def searchs(x):
    headers = {
    'User-Agent': '<YOUR_USERAGENT>'
    }
    x = urllib.parse.quote(x.lower(), safe="")
    p = requests.get("https://euw.whatismymmr.com/api/v1/summoner?name={}".format(x), headers=headers)
    f = json.loads(p.text)
    return f
def search(update, context):
    bot = context.bot
    chat_id = update.effective_chat.id
    lung = len(context.args)
    name = ""
    if lung > 1:
        for i in range(lung):
            if i == 0:
                name += context.args[i]
            else:
                name += " " + context.args[i]
    else:
        name = context.args[0]
    results = searchs(name)
    wot = "MMR Calc powered by whatismymmr.com\n\n"
    if "error" in results.keys():
        wot += "Summoner not available, are you sure you wrote it right?\nIn that case remember we only support EUW at the moment"
    else:
        if results["ranked"]["avg"] is not None:
            wot += "Ranked MMR: {rmin} - {rmax}\n".format(rmin = results["ranked"]["avg"]-results["ranked"]["err"], rmax = results["ranked"]["avg"]+results["ranked"]["err"])
        else:
            wot += "Ranked MMR: Unavailable\nPlay more solo queues to know\n"
        if results["normal"]["avg"] is not None:
            wot += "Normal MMR: {nmin} - {nmax}\n".format(nmin = results["normal"]["avg"]-results["normal"]["err"], nmax = results["normal"]["avg"]+results["normal"]["err"])
        else:
            wot += "Normal MMR: Unavailable\nPlay more solo games to know\n"
        if results["ARAM"]["avg"] is not None:
            wot += "ARAM MMR: {amin} - {amax}\n".format(amin = results["ARAM"]["avg"]-results["ARAM"]["err"], amax = results["ARAM"]["avg"]+results["ARAM"]["err"])
        else:
            wot += "ARAM MMR: Unavailable\nPlay more solo games to know\n"
    bot.sendMessage(text=wot, chat_id=chat_id)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
updater = Updater(token="<YOUR_TOKEN>", use_context="True")
dispatcher = updater.dispatcher
searchCommandHandler = CommandHandler("search", search)
dispatcher.add_handler(searchCommandHandler)
updater.start_polling()
updater.idle()
