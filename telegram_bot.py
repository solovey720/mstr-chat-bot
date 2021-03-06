import telebot
import pandas as pd
import dataframe_image as dfi
import mstr_connect
import os

token = '5098007657:AAEwiPhBn7k-CR8q4FtPSYPJFNwrUEyGDxk'
bot = telebot.TeleBot(token)

conn = mstr_connect.get_connection()


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я помогу тебе найти отчет, для этого введи /search')
    

@bot.message_handler(commands=['help'])
def help_info(message):
    bot.send_message(message.chat.id, 'Текст помощи')


@bot.message_handler(commands=['search'])
def help_info(message):
    bot.send_message(message.chat.id, 'Введи имя своего отчета:')
    bot.register_next_step_handler(message, search_report)


@bot.message_handler(content_types=['text'])
def simple_text(message):
    bot.send_message(message.chat.id, 'Я пока тебя не понимаю')


def search_report(message):
    all_reports = mstr_connect.search_report(conn, message.text)
    markup = telebot.types.InlineKeyboardMarkup()
    if not all_reports:
        bot.send_message(message.chat.id, "Такого репорта не существует")
    else:
        for rep in all_reports:
            markup.add(telebot.types.InlineKeyboardButton(rep.name, callback_data='reportId_' + rep.id))
        bot.send_message(message.chat.id, "Выберите репорт:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('reportId_'))
def show_report(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    report_id = call.data.split("_")[1]
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Показать первые 20 записей', callback_data='showTop_20_' + report_id))
    markup.add(telebot.types.InlineKeyboardButton('Показать все данные', callback_data='showTop_100_' + report_id))
    bot.send_message(call.message.chat.id, "В каком виде показать отчет?", reply_markup=markup)
    bot.send_message(call.message.chat.id, "\'Показать все данные\' включает в себя не более 100 строк")


@bot.callback_query_handler(func=lambda call: call.data.startswith('showTop_'))
def show_report_data(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    top_data = int(call.data.split('_')[1])
    report_id = call.data.split('_')[2]
    df = pd.DataFrame(data=mstr_connect.get_report(conn, report_id).to_dataframe()[:top_data])
    for i in range(len(df.index) // 20 + (0 if (len(df.index) % 20 == 0) else 1) ):
        dfi.export(df[i * 20:i * 20 + 20], report_id + '_' + str(i) + '.png', table_conversion='matplotlib')
        bot.send_photo(call.message.chat.id, open(report_id + '_' + str(i) + '.png', 'rb'))
        os.remove(report_id + '_' + str(i) + '.png')
    markup = telebot.types.InlineKeyboardMarkup()
    yes_button = telebot.types.InlineKeyboardButton('Да', callback_data='use_filter_' + report_id)
    no_button = telebot.types.InlineKeyboardButton('Нет', callback_data='dont_use_filter')
    markup.add(yes_button, no_button)
    bot.send_message(call.message.chat.id, "Добавить фильтр на отчет?", reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data.startswith('use_filter_'))
def add_filter(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    report_id = call.data.split("_")[1]
    print(mstr_connect.get_report_attributes(conn, report_id))

@bot.callback_query_handler(func=lambda call: call.data.startswith('dont_use_filter'))
def add_filter(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "Для поиска другого отчета напиши /search")



bot.infinity_polling()
