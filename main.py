#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from telegram import Emoji, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


def start_message(bot, chat_id):
    bot.sendMessage(chat_id, text="https://www.youtube.com/watch?v=N4mEzFDjqtA")
    callback_data = 'answer|'
    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('A. 1', callback_data=callback_data + '1'),
            InlineKeyboardButton('B. 2', callback_data=callback_data + '2'),
        ],
        [
            InlineKeyboardButton('C. 3', callback_data=callback_data + '3'),
            InlineKeyboardButton('D. 4', callback_data=callback_data + '4'),
        ]
    ])
    bot.sendMessage(chat_id, text="Choose an answer:", reply_markup=reply_markup)


def start(bot, update):
    start_message(bot, update.message.chat_id)


def answer_question(bot, update):
    query = update.callback_query
    chat_id = query.message.chat_id
    parts = dict(enumerate(query.data.split('|', 1)))
    answer_type = parts[0]
    data = parts.get(1)
    bot.answerCallbackQuery(query.id, text="Ok!")
    if answer_type == 'answer':
        if data == '3':
            answer = "Correct!"
        else:
            answer = "Wrong!"
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Next', callback_data='next')]])
        edit_message = {
            'chat_id': chat_id,
            'message_id': query.message.message_id,
            'text': answer,
            'reply_markup': reply_markup,
        }
        bot.editMessageText(**edit_message)
    elif answer_type == 'next':
        start_message(bot, chat_id)


def error(bot, update, error_msg):
    logging.warning('Update "%s" caused error "%s"' % (update, error_msg))


# Create the Updater and pass it your bot's token.
updater = Updater(config.TOKEN)

updater.dispatcher.add_handler(CommandHandler('start', start))
# The confirmation
updater.dispatcher.add_handler(CallbackQueryHandler(answer_question))
updater.dispatcher.add_error_handler(error)

# Start the Bot
updater.start_polling(timeout=60)

# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT
updater.idle()
