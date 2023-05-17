import random
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from config import TOKEN_API



bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot)

keyboard = types.InlineKeyboardMarkup()
join_button = types.InlineKeyboardButton(text='Присоединиться', callback_data='join_game')
keyboard.add(join_button)
roles = ['Ты мафия - Веревочкин', 'Ты мирный житель - Восканян', 'Ты комиссар - Райгородский',
         'Ты доктор - Молчанов', 'Ты мирный житель - Монченко', 'Ты мафия - Ткачёв',
         'Ты мирный житель - Андреев', 'Ты мирный житель - Павлова', 'Ты дон-мафия - Иванова',
         'Ты мирный житель - Подлесных']
flag = 0
killer_flag_first = 0
killer_flag_second = 0
killer_flag_third = 0
healer_flag = 0
chop_flag = 0
players = list()
killed_players = list()
healed_player = list()
killed_player = list()
votes = list()
first_mafia = None
second_mafia = None
third_mafia = None
healer = None
chop = None
checked = list()

counter_of_alive = 0
counter_of_mafia = 0

game_text = '''Добро пожаловать на физтех-Мафию!🥰🥰🥰
К сожалению, в нашем мирном вузе завелись негодяи, которые делают
вид, что они честные и справедливые преподаватели, но по ночам они фачат
за даже самые мелкие недочёты в контрольных и домашках бедных студентов.
Вам нужно найти этих преподавателей и лишить их премии!😈😈😈
Желаю удачи честным преподавателям!
Через 2 минуты после начала напишите функцию next day, чтобы добраться до следующего утра'''

start_text = '''Минимальное количество участников для начала игры набралось
Чтобы начать напишите Go'''

night_text = '''Новая ночь началась, кто же мафия?'''

@dp.message_handler(Text(equals='Play'))
async def start_the_connection(message: types.Message):
    global flag
    if flag == 0:
        await bot.send_message(chat_id=message.chat.id,
                               text='Хотите сыграть в физтех-Мафию?🎃🎃🎃',
                               reply_markup=keyboard)
        flag = 1
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text='Игра уже идёт')

@dp.message_handler(Text(equals='Go'))
async def start_the_game(message: types.Message):
    global counter_of_mafia, counter_of_alive
    global first_mafia, second_mafia, third_mafia
    global chop, healer
    global flag
    if len(players) >= 5 and flag == 1:
        flag += 1
        await bot.send_message(chat_id=message.chat.id,
                               text=game_text)
        game_role = list()
        buttons = list()
        counter_of_alive = len(players)
        for i in range(len(players)):
            game_role.append(roles[i])
        random_role = random.sample(game_role, len(players))
        for j in range(len(players)):
            player = players[j]
            if random_role[j] == roles[0]:
                counter_of_mafia += 1
                first_mafia = player
                await bot.send_message(chat_id=player.id,
                                       text=f'{random_role[j]}')
                await bot.send_message(chat_id=player.id,
                                       text='''Выбери жертву
Для этого напиши команду Kill''')
            elif random_role[j] == roles[5]:
                counter_of_mafia += 1
                second_mafia = player
                await bot.send_message(chat_id=player.id,
                                       text=f'{random_role[j]}')
                await bot.send_message(chat_id=player.id,
                                       text='''Выбери жертву
Для этого напиши команду Kill''')
            elif random_role[j] == roles[8]:
                counter_of_mafia += 1
                third_mafia = player
                await bot.send_message(chat_id=player.id,
                                       text=f'{random_role[j]}')
                await bot.send_message(chat_id=player.id,
                                       text='''Выбери жертву
Для этого напиши команду Kill''')
            elif random_role[j] == roles[2]:
                await bot.send_message(chat_id=player.id,
                                       text=f'{random_role[j]}\nВыбери кого проверить\nДля этого напиши команду check')
                chop = player
            elif random_role[j] == roles[3]:
                await bot.send_message(chat_id=player.id,
                                       text=f'{random_role[j]}\nВыбери кого вылечить\nДля этого напиши команду heal')
                healer = player
            else:
                await bot.send_message(chat_id=player.id,
                                       text=f'{random_role[j]}\nЖди утра')
    elif len(players) < 5:
        await bot.send_message(chat_id=message.chat.id,
                               text='Недостаточно участников для начала игры')
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text='Игра уже идёт')


@dp.message_handler(Text(equals='Kill'))
async def kill_command(message: types.Message):
    global flag, killer_flag_first, killer_flag_second, killer_flag_third
    global first_mafia, second_mafia, third_mafia
    if flag == 2 and message.from_user == first_mafia and killer_flag_first == 0:
        Kill_kb = InlineKeyboardMarkup()
        kill_buttons = list()
        for i in range(len(players)):
            kill_buttons.append(InlineKeyboardButton(text=f'{players[i].full_name}',
                                                     callback_data=f'Kill {players[i].full_name}'))
        Kill_kb.add(*kill_buttons)
        await message.answer(text='Выбери жертву',
                             reply_markup=Kill_kb)
        killer_flag_first += 1
    elif flag == 2 and message.from_user == second_mafia and killer_flag_second == 0:
        Kill_kb = InlineKeyboardMarkup()
        kill_buttons = list()
        for i in range(len(players)):
            kill_buttons.append(InlineKeyboardButton(text=f'{players[i].full_name}',
                                                     callback_data=f'Kill {players[i].full_name}'))
        Kill_kb.add(*kill_buttons)
        await message.answer(text='Выбери жертву',
                             reply_markup=Kill_kb)
        killer_flag_second += 1
    elif flag == 2 and message.from_user == third_mafia and killer_flag_third == 0:
        Kill_kb = InlineKeyboardMarkup()
        kill_buttons = list()
        for i in range(len(players)):
            kill_buttons.append(InlineKeyboardButton(text=f'{players[i].full_name}',
                                                     callback_data=f'Kill {players[i].full_name}'))
        Kill_kb.add(*kill_buttons)
        await message.answer(text='Выбери жертву',
                             reply_markup=Kill_kb)
        killer_flag_third += 1
    else:
        await message.answer(text='Уже нельзя убивать')


@dp.message_handler(Text(equals='heal'))
async def heal_command(message: types.Message):
    global flag, healer_flag
    global healer
    if flag == 2 and healer_flag == 0 and message.from_user == healer:
        Heal_kb = InlineKeyboardMarkup()
        Heal_buttons = list()
        for i in range(len(players)):
            Heal_buttons.append(InlineKeyboardButton(text=f'{players[i].full_name}',
                                                     callback_data=f'Heal {players[i].full_name}'))
        Heal_kb.add(*Heal_buttons)
        await message.answer(text='Выбери кого хочешь вылечить',
                             reply_markup=Heal_kb)
        healer_flag += 1
    else:
        await message.answer(text='Сейчас нельзя лечить')


@dp.message_handler(Text(equals='check'))
async def check_command(message: types.Message):
    global checked
    global flag, chop_flag
    global chop
    if flag == 2 and message.from_user == chop and chop_flag == 0:
        check_kb = InlineKeyboardMarkup()
        chop_flag += 1
        check_buttons = list()
        for i in range(len(players)):
            check_buttons.append(InlineKeyboardButton(text=f'{players[i].full_name}',
                                                      callback_data=f'Check {players[i].full_name}'))
        check_kb.add(*check_buttons)
        await message.answer(text='Выбери кого хочешь проверить',
                             reply_markup=check_kb)
    else:
        await message.answer(text='Сейчас нельзя проверять')


@dp.callback_query_handler(lambda c: c.data == 'join_game')
async def join_game(callback_query: types.CallbackQuery):
    global flag
    if flag == 1:
        user = callback_query.from_user
        if user not in players:
            players.append(user)
            await bot.send_message(chat_id=user.id,
                                   text='Вы присоединились к игре!')
            if user.full_name == 'Andrew':
                await bot.send_message(chat_id=callback_query.message.chat.id,
                                       text=f'{user.full_name} идёт на забив😎!')
            elif user.full_name == 'Айдар Аманкулов':
                await bot.send_message(chat_id=callback_query.message.chat.id,
                                       text=f'{user.full_name} Кыргыз в здании!')
            elif user.full_name == 'катя':
                await bot.send_message(chat_id=callback_query.message.chat.id,
                                       text=f'{user.full_name} - анигилятор кринжа идёт не забив')
            else:
                await bot.send_message(chat_id=callback_query.message.chat.id,
                                       text=f'{user.full_name} присоединился к игре!')
            await callback_query.message.edit_text(text=f'''Хотите сыграть в физтех-Мафию?🎃🎃🎃?
{len(players)} уже в игре🥳🥳🥳''',
                                                   reply_markup=keyboard)
            if len(players) >= 5:
                await bot.send_message(chat_id=callback_query.message.chat.id,
                                       text=start_text)
        else:
            await bot.send_message(chat_id=user.id,
                                   text='Вы уже присоединились к игре!')
    else:
        await bot.send_message(chat_id=callback_query.message.chat.id,
                               text='Игра уже идёт')



@dp.message_handler(Text(equals='next day'))
async def next_round(message: types.Message):
    global counter_of_alive, counter_of_mafia
    global first_mafia, second_mafia, third_mafia
    global flag
    global players, killed_player, killed_players, healed_player
    print(flag)
    print(first_mafia)
    print(counter_of_alive)
    print(counter_of_mafia)
    print(killed_player)
    print(killed_players)
    print(healed_player)
    if (len(healed_player) == 1 and len(killed_player) > 0 and killed_player[0] == healed_player[0]) and flag == 2:
        flag += 1
        await bot.send_message(chat_id=message.chat.id,
                               text='''Сегодня ночью никто не умер, можете обсудить
кого вы считаете факером
Для начала голосвания напишите Vote''')
    elif len(killed_player) > 0 and flag == 2:
        for player in players:
            if player == killed_player[0] and player == first_mafia:
                players.remove(player)
                counter_of_alive -= 1
                counter_of_mafia -= 1
            elif player == killed_player[0] and player == second_mafia:
                players.remove(player)
                counter_of_alive -= 1
                counter_of_mafia -= 1
            elif player == killed_player[0] and player == third_mafia:
                players.remove(player)
                counter_of_alive -= 1
                counter_of_mafia -= 1
            elif player == killed_player[0]:
                players.remove(player)
                counter_of_alive -= 1
        if counter_of_mafia != 0 and counter_of_alive > 2 * counter_of_mafia:
            await bot.send_message(chat_id=message.chat.id,
                               text=f'''Сегодня ночью умер(ла) {killed_player[0].full_name}, можете обсудить
кого вы считаете факером
Для начала голосвания напишите Vote''')
            flag += 1
        elif counter_of_mafia == 0:
            await bot.send_message(chat_id=message.chat.id,
                                   text=f'''Сегодня ночью умер(ла) {killed_player[0].full_name}
Мафий больше нет, Вы победили! 
Поздравляю мирных жителей с победой!
Напишите end game''')
            flag = 6
        elif counter_of_mafia != 0 and counter_of_alive <= 2 * counter_of_mafia:
            await bot.send_message(chat_id=message.chat.id,
                                   text=f'''К сожалению, факеры победили:(. 
Удачи мирным в следующей игре. 
Нажмите end game''')
            flag = 6
    #else:
     #   flag = 6
    #    await bot.send_message(chat_id=message.chat.id,
   #                            text=f'''Сегодня ночью умер(ла) {killed_player[0].full_name}
#Мафий больше нет, Вы победили!
#Поздравляю мирных жителей с победой!
#Напишите end game''')
    if len(killed_players) >= 1:
        for i in range(len(killed_players)):
            killed_players.remove(killed_players[0])
    if len(healed_player) >= 1:
        for j in range(len(healed_player)):
            healed_player.remove(healed_player[0])
    if len(killed_player) >= 1:
        for t in range(len(killed_player)):
            killed_player.remove(killed_player[0])


@dp.message_handler(Text(equals='Vote'))
async def vote(message: types.Message):
    global flag
    if flag == 3:
        Vote_kb = InlineKeyboardMarkup()
        vote_buttons = list()
        for i in range(len(players)):
            vote_buttons.append(InlineKeyboardButton(text=f'{players[i].full_name}',
                                                     callback_data=f'Vote {players[i].full_name}'))
        Vote_kb.add(*vote_buttons)
        await message.answer(text='''Выбери факера
Через 2 минуты закройте голосование написав в чат end vote''',
                             reply_markup=Vote_kb)
        flag += 1
    else:
        await message.answer(text='Сейчас нельзя начинать голосование')





@dp.message_handler(Text(equals='end vote'))
async def vote_results(message: types.Message):
    global counter_of_mafia, counter_of_alive
    global first_mafia, second_mafia, third_mafia
    global flag
    global votes
    if flag == 4:
        max_votes = list()
        for player in players:
            max_votes.append(votes.count(player))
        counter = max_votes.count(max(max_votes))
        if counter != 1:
            await message.answer(text='''Вы никого не выгнали, чтобы начать следующую ночь,
напишите next night''')
            flag = 5
        else:
            for i in range(len(max_votes)):
                if max_votes[i] == max(max_votes):
                    if players[i] != first_mafia and players[i] != second_mafia and players[i] != third_mafia and counter_of_alive > 2 * counter_of_mafia + 1:
                        await message.answer(text=f'''Вы выгнали игрока {players[i].full_name},
чтобы начать следующую ночь, напишите next night''')
                        flag = 5
                        counter_of_alive -= 1
                        players.remove(players[i])
                    elif players[i] != first_mafia and players[i] != second_mafia and players[i] != third_mafia and counter_of_alive <= 2 * counter_of_mafia + 1:
                        await message.answer(text=f'''Вы выгнали игрока {players[i].full_name},
но он не был мафией:(
Мафии победили, удачи мирным в следующей игре
Напишите end game''')
                        flag = 6
                        counter_of_alive -= 1
                        players.remove(players[i])
                    elif (players[i] == first_mafia or players[i] == second_mafia or players[i] == third_mafia) and counter_of_mafia >= 2:
                        await message.answer(text=f'''Вы выгнали игрока {players[i].full_name},
чтобы начать следующую ночь, напишите next night''')
                        flag = 5
                        counter_of_alive -= 1
                        counter_of_mafia -= 1
                        players.remove(players[i])
                    else:
                        await bot.send_message(chat_id=message.chat.id,
                                               text=f'''Вы выгнали игрока {players[i].full_name}
Мафий больше нет, Вы победили! 
Поздравляю мирных жителей с победой!
Напишите end game''')
                        flag = 6
        for i in range(len(votes)):
            votes.remove(votes[0])
    else:
        await message.answer(text='Сейчас нельзя закончить голосование')


@dp.message_handler(Text(equals='next night'))
async def next_night(message: types.Message):
    global flag
    global killer_flag_first, killer_flag_second, killer_flag_third
    global chop_flag, healer_flag
    global first_mafia, second_mafia, third_mafia
    global chop, healer
    if flag == 5:
        if len(players) >= 1:
            await bot.send_message(chat_id=message.chat.id,
                                   text=night_text)
            buttons = list()
            flag = 2
            killer_flag_first, killer_flag_second, killer_flag_third = 0, 0, 0
            healer_flag, chop_flag = 0, 0
            for j in range(len(players)):
                player = players[j]
                if player == first_mafia or player == second_mafia or player == third_mafia:
                    await bot.send_message(chat_id=player.id,
                                           text='''Выбери жертву
Для этого напиши команду Kill''')
                elif player == chop:
                    await bot.send_message(chat_id=player.id,
                                           text=f'Выбери кого проверить\nДля этого напиши команду check')
                elif player == healer:
                    await bot.send_message(chat_id=player.id,
                                           text=f'Выбери кого вылечить\nДля этого напиши команду heal')
                else:
                    await bot.send_message(chat_id=player.id,
                                           text=f'Жди утра')
        else:
            await bot.send_message(chat_id=message.chat.id,
                                   text='Недостаточно участников для начала игры')
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text='Ещё рано')


@dp.message_handler(Text(equals='end game'))
async def end_game(message: types.Message):
    global first_mafia, second_mafia, third_mafia
    global chop, healer, checked
    global players, votes, killed_player, killed_players, healed_player
    global counter_of_mafia, counter_of_alive
    global flag, chop_flag, healer_flag
    global killer_flag_first, killer_flag_second, killer_flag_third
    counter_of_alive = 0
    counter_of_mafia = 0
    flag = 0
    chop_flag = 0
    healer_flag = 0
    killer_flag_first, killer_flag_second, killer_flag_third = 0, 0, 0
    first_mafia = None
    second_mafia = None
    third_mafia = None
    chop = None
    healer = None
    await bot.send_message(chat_id=message.chat.id,
                           text='Чтобы начать следующую игру напишите Play')
    if len(checked) > 0:
        for o in range(len(checked)):
            checked.remove(checked[0])
    if len(players) > 0:
        for i in range(len(players)):
            players.remove(players[0])
    if len(votes) > 0:
        for j in range(len(votes)):
            votes.remove(votes[0])
    if len(killed_player) > 0:
        for k in range(len(killed_player)):
            killed_player.remove(killed_player[0])
    if len(killed_players) > 0:
        for t in range(len(killed_players)):
            killed_players.remove(killed_players[0])
    if len(healed_player) > 0:
        for r in range(len(healed_player)):
            healed_player.remove(healed_player[0])



@dp.callback_query_handler()
async def Kill_Heal_Vote(callback: types.CallbackQuery):
    global checked, first_mafia, second_mafia, third_mafia
    global chop, healer
    global players, killed_player, killed_players, healed_player
    for player in players:
        if callback.data == f'Kill {player.full_name}' and (callback.from_user == first_mafia or callback.from_user == second_mafia or callback.from_user == third_mafia):
            killed_players.append(player)
            await callback.answer(text='Молодец, удачи в дальнейших отчислениях')
            await bot.edit_message_reply_markup(chat_id=callback.from_user.id,
                                                message_id=callback.message.message_id,
                                                reply_markup=None)
            print(killed_players)
        elif callback.data == f'Heal {player.full_name}' and callback.from_user == healer:
            healed_player.append(player)
            await callback.answer('Молодец, надеемся, что ты спас студента от отчисления')
            await bot.edit_message_reply_markup(chat_id=callback.from_user.id,
                                                message_id=callback.message.message_id,
                                                reply_markup=None)
        elif callback.data == f'Check {player.full_name}' and callback.from_user == chop:
            if player == first_mafia or player == second_mafia or player == third_mafia:
                await callback.answer(text=f'''{player.full_name} - Мафия, молодец, ты попал''')
            else:
                await callback.answer(text=f'''Увы
{player.full_name} - не мафия, удачи в дальнейших поисках''')
            await bot.edit_message_reply_markup(chat_id=callback.from_user.id,
                                                message_id=callback.message.message_id,
                                                reply_markup=None)
        elif callback.data == f'Vote {player.full_name}':
            if callback.from_user in players:
                votes.append(player)
                await bot.send_message(chat_id=callback.message.chat.id,
                                       text=f'''{callback.from_user.full_name} проголосовал в
{player.full_name}''')
            else:
                await callback.answer('Ты выбыл, голосовать нельзя')
    if len(killed_players) == 3:
        if killed_players[0] == killed_players[1]:
            killed_player.append(killed_players[0])
        elif killed_players[1] == killed_players[2]:
            killed_player.append(killed_players[1])
        elif killed_players[0] == killed_players[2]:
            killed_player.append(killed_players[1])
        else:
            killed_player.append(random.choice(killed_players))
    elif len(killed_players) == 2:
        killed_player.append(random.choice(killed_players))
    elif len(killed_players) == 1:
        killed_player.append(killed_players[0])
    print(killed_players)
    print(killed_player)


async def on_startup(dp):
    print('Бот был успешно запущен!')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
