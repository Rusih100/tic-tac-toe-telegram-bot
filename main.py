from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from random import choice
from time import sleep
import telebot

bot = telebot.TeleBot('1911810401:AAEJmxx-m7vllOmVsDhjK8bK-NcCT-pkZ_c')

command_dict = {
    '/start': 'Старт бота',
    '/help': 'Помощь с ботом',
    '/new_game': 'Запускает новую игру'
}


def game_grid(values_dict, all_moves_set):
    game_value = packaging_values(values_dict, all_moves_set)

    grid = InlineKeyboardMarkup()
    grid.row_width = 3
    for i in range(1, 10, 3):
        grid.add(InlineKeyboardButton(text=show_value(values_dict, i + 0),
                                      callback_data=f'1-{i + 0}-{game_value}'),
                 InlineKeyboardButton(text=show_value(values_dict, i + 1),
                                      callback_data=f'1-{i + 1}-{game_value}'),
                 InlineKeyboardButton(text=show_value(values_dict, i + 2),
                                      callback_data=f'1-{i + 2}-{game_value}'))
    return grid


def empty_game_grid(values_dict):
    grid = InlineKeyboardMarkup()
    grid.row_width = 3
    for i in range(1, 10, 3):
        grid.add(InlineKeyboardButton(text=show_value(values_dict, i + 0),
                                      callback_data=f'none'),
                 InlineKeyboardButton(text=show_value(values_dict, i + 1),
                                      callback_data=f'none'),
                 InlineKeyboardButton(text=show_value(values_dict, i + 2),
                                      callback_data=f'none'))
    return grid


def show_value(values_dict, index):
    index = str(index)
    value = str(values_dict[index])
    return value


def packaging_values(values_dict, all_moves_set):
    value_str = ''
    for i in values_dict:
        value_str += str(values_dict[i])
    value_str += '-'
    for i in all_moves_set:
        value_str += str(i)
    return value_str


def unpacking_values(value_str):
    data = value_str.split('-')
    move = data[1]
    dict_str = data[2]
    set_str = data[3]

    values_dict = {'1': ' ', '2': ' ', '3': ' ',
                   '4': ' ', '5': ' ', '6': ' ',
                   '7': ' ', '8': ' ', '9': ' '}
    for i in range(1, 10):
        values_dict[str(i)] = dict_str[i - 1]

    all_moves_set = set(set_str)
    return move, values_dict, all_moves_set


def check_win(values_dict):
    check_data = [
        [values_dict['1'], values_dict['2'], values_dict['3']],
        [values_dict['4'], values_dict['5'], values_dict['6']],
        [values_dict['7'], values_dict['8'], values_dict['9']],
        [values_dict['1'], values_dict['4'], values_dict['7']],
        [values_dict['2'], values_dict['5'], values_dict['8']],
        [values_dict['3'], values_dict['6'], values_dict['9']],
        [values_dict['1'], values_dict['5'], values_dict['9']],
        [values_dict['3'], values_dict['5'], values_dict['7']]
    ]
    for i in check_data:
        if i[0] == i[1] == i[2] == '❌':
            return True, 'Вы победили'

        if i[0] == i[1] == i[2] == '⭕':
            return True, 'Вы проиграли'

    return False, 'none'


def bot_ai(values_dict, all_moves_set):
    check_data = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9'],
        ['1', '4', '7'],
        ['2', '5', '8'],
        ['3', '6', '9'],
        ['1', '5', '9'],
        ['3', '5', '7']
    ]

    for i in check_data:
        if values_dict[i[0]] == values_dict[i[1]] == '⭕' and i[2] in all_moves_set:
            return i[2]

        elif values_dict[i[0]] == values_dict[i[2]] == '⭕' and i[1] in all_moves_set:
            return i[1]

        elif values_dict[i[1]] == values_dict[i[2]] == '⭕' and i[0] in all_moves_set:
            return i[0]

    for i in check_data:
        if values_dict[i[0]] == values_dict[i[1]] == '❌' and i[2] in all_moves_set:
            return i[2]

        elif values_dict[i[0]] == values_dict[i[2]] == '❌' and i[1] in all_moves_set:
            return i[1]

        elif values_dict[i[1]] == values_dict[i[2]] == '❌' and i[0] in all_moves_set:
            return i[0]

    bot_move = choice(list(all_moves_set))
    return bot_move


@bot.message_handler(commands=['start'])
def command_start(message):
    data_text = ["Привет!",
                 "Я бот с которым можно сыграть в крестики нолики.",
                 "Чтобы начать игру используйте команду /new_game"]
    for text in data_text:
        bot.send_message(message.from_user.id, text)
        sleep(0.4)


@bot.message_handler(commands=['help'])
def command_help(message):
    text = f"Список команд: \n"
    for key, value in command_dict.items():
        text += f"{key} - {value} \n"
    bot.send_message(message.from_user.id, text)


@bot.message_handler(commands=['new_game'])
def command_new_game(message):
    all_moves_set = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}

    values_dict = {'1': ' ', '2': ' ', '3': ' ',
                   '4': ' ', '5': ' ', '6': ' ',
                   '7': ' ', '8': ' ', '9': ' '}
    bot.send_message(message.from_user.id, text="Игра началась", reply_markup=game_grid(values_dict, all_moves_set))


@bot.message_handler(content_types=['text'])
def text_log(message):
    text = f'{datetime.now()} - {message.from_user.first_name} - {message.text}'
    print(text)


@bot.callback_query_handler(func=lambda call: True)
def callback_data(call):
    if call.data[0] == '1':

        move, values_dict, all_moves_set = unpacking_values(call.data)

        if move in all_moves_set:
            values_dict[move] = '❌'
            all_moves_set.remove(move)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.id,
                                          reply_markup=empty_game_grid(values_dict))

            if check_win(values_dict)[0]:
                text = f'Игра окончена. {check_win(values_dict)[1]}'
                bot.send_message(call.message.chat.id, text=text)
                bot.send_message(call.message.chat.id, text='Сыграем еще? /new_game')
                return

            sleep(0.7)

            if len(all_moves_set) != 0:
                bot_move = bot_ai(values_dict, all_moves_set)
                values_dict[bot_move] = '⭕'
                all_moves_set.remove(bot_move)
                bot.edit_message_reply_markup(call.message.chat.id, call.message.id,
                                              reply_markup=game_grid(values_dict, all_moves_set))

                if check_win(values_dict)[0]:
                    text = f'Игра окончена. {check_win(values_dict)[1]}'
                    bot.edit_message_reply_markup(call.message.chat.id, call.message.id,
                                                  reply_markup=empty_game_grid(values_dict))
                    bot.send_message(call.message.chat.id, text=text)
                    bot.send_message(call.message.chat.id, text='Сыграем еще? /new_game')
                    return

            else:
                bot.send_message(call.message.chat.id, text='Игра окончена. Ничья')
                bot.send_message(call.message.chat.id, text='Сыграем еще? /new_game')
                return


bot.polling(none_stop=True)
