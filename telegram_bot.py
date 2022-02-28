import telebot
import pandas as pd
import dataframe_image as dfi
import mstr_connect

token = '5181481316:AAFrV0UNkG7to7AWhwFjFyviQbqHPHH1MtU'
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
    df = pd.DataFrame(data=mstr_connect.show_report_info(conn, report_id))
    dfi.export(df, report_id + '.png', table_conversion='matplotlib')
    bot.send_photo(call.message.chat.id, open(report_id + '.png', 'rb'))


bot.infinity_polling()
