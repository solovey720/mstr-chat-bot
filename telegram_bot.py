import telebot
import pandas as pd
import dataframe_image as dfi
import mstr_connect
import os

token = '<your_token>'
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
def sel_report(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    report_id = call.data.split("_")[1]
    markup = telebot.types.InlineKeyboardMarkup()
    yes_button = telebot.types.InlineKeyboardButton('Да', callback_data='yes_' + report_id)
    no_button = telebot.types.InlineKeyboardButton('Нет', callback_data='no_' + report_id)
    markup.add(yes_button, no_button)
    bot.send_message(call.message.chat.id, "Добавить фильтр на отчет?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('no_'))
def show_report(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    report_id = call.data.split("_")[1]
    markup = telebot.types.InlineKeyboardMarkup()
    part_data = telebot.types.InlineKeyboardButton('Показать первые 20 записей', callback_data='showTop20_' + report_id)
    all_data = telebot.types.InlineKeyboardButton('Показать все данные', callback_data='showAllData_' + report_id)
    markup.add(part_data, all_data)
    bot.send_message(call.message.chat.id, "В каком виде показать отчет?", reply_markup=markup)
    bot.send_message(call.message.chat.id, "\'Показать все данные\' может занять некоторое время")


@bot.callback_query_handler(func=lambda call: call.data.startswith('showAllData_'))
def show_report_all(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    report_id = call.data.split("_")[1]
    df = pd.DataFrame(data=mstr_connect.get_report(conn, report_id).to_dataframe()[:100])
    for i in range(len(df.index) // 20):
        dfi.export(df[i * 20:i * 20 + 20], report_id + '_' + str(i) + '.png', table_conversion='matplotlib')
        bot.send_photo(call.message.chat.id, open(report_id + '_' + str(i) + '.png', 'rb'))
    dfi.export(df[(len(df.index) // 20) * 20:], report_id + '_' + str((len(df.index) // 20)) + '.png',
               table_conversion='matplotlib')
    bot.send_photo(call.message.chat.id, open(report_id + '_' + str((len(df.index) // 20)) + '.png', 'rb'))
    remove_all_png_files()

@bot.callback_query_handler(func=lambda call: call.data.startswith('showTop20_'))
def show_report_top20(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    report_id = call.data.split("_")[1]
    df = pd.DataFrame(data=mstr_connect.get_report(conn, report_id).to_dataframe()[:20])
    dfi.export(df, report_id + '_top20.png', table_conversion='matplotlib')
    bot.send_photo(call.message.chat.id, open(report_id + '_top20.png', 'rb'))
    remove_all_png_files()


@bot.callback_query_handler(func=lambda call: call.data.startswith('yes_'))
def add_filter(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    report_id = call.data.split("_")[1]
    print(mstr_connect.get_report_attributes(conn, report_id))


# remove ALL .png files
def remove_all_png_files():
    for file in os.listdir(os.getcwd()):
        if file.endswith('.png'):
            os.remove(file)


bot.infinity_polling()
