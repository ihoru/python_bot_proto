#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Basic example for a bot that awaits an answer from the user. It's built upon
# the state_machine_bot.py example
# This program is dedicated to the public domain under the CC0 license.

import logging
from telegram import Emoji, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

# Define the different states a chat can be in
MENU, AWAIT_CONFIRMATION, AWAIT_INPUT = range(3)

# Python 2 and 3 unicode differences
try:
    YES, NO = (Emoji.THUMBS_UP_SIGN.decode('utf-8'), Emoji.THUMBS_DOWN_SIGN.decode('utf-8'))
except AttributeError:
    YES, NO = (Emoji.THUMBS_UP_SIGN, Emoji.THUMBS_DOWN_SIGN)

# States are saved in a dict that maps chat_id -> state
state = dict()
# Sometimes you need to save data temporarily
context = dict()
# This dict is used to store the settings value for the chat.
# Usually, you'd use persistence for this (e.g. sqlite).
values = dict()


def start_message(bot, chat_id):
    bot.sendMessage(chat_id, text="https://www.youtube.com/watch?v=N4mEzFDjqtA")
    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('A. 1', callback_data='1'),
            InlineKeyboardButton('B. 2', callback_data='2'),
        ],
        [
            InlineKeyboardButton('C. 3', callback_data='3'),
            InlineKeyboardButton('D. 4', callback_data='4'),
        ]
    ])
    bot.sendMessage(chat_id, text="Choose an answer:", reply_markup=reply_markup)


def start(bot, update):
    start_message(bot, update.message.chat_id)


def answer_question(bot, update):
    query = update.callback_query
    chat_id = query.message.chat_id
    text = query.data
    print(text)
    bot.answerCallbackQuery(query.id, text="Ok!")
    edit_message = {'chat_id': chat_id, 'message_id': query.message.message_id}
    if text == '3':
        answer = "Correct!"
    else:
        answer = "Wrong!"
    bot.editMessageText(text=answer, **edit_message)
    start_message(bot, chat_id)


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))


# Create the Updater and pass it your bot's token.
updater = Updater(config.TOKEN)

updater.dispatcher.add_handler(CommandHandler('start', start))
# The confirmation
updater.dispatcher.add_handler(CallbackQueryHandler(answer_question))
updater.dispatcher.add_error_handler(error)

# Start the Bot
updater.start_polling()

# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT
updater.idle()
