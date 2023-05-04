from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from config import TOKEN_API
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import string
roles = ['Ты мафия - Веревочкин', 'Ты мирный житель - Восканян', 'Ты комиссар - Райгородский',
         'Ты доктор - Молчанов', 'Ты мирный житель - Монченко', 'Ты мафия - Ткачёв',
         'Ты мирный житель - Андреев', 'Ты мирный житель - Павлова', 'Ты мафия - Иванова',
         'Ты мирный житель - Подлесных']

bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot)
players = []
choose_player = InlineKeyboardMarkup(row_width=2)
check_but = InlineKeyboardButton(text='Что-то',
                                 callback_data='То же самое')
choose_player.add(check_but)
chat_id = ''
keyboard = types.InlineKeyboardMarkup()
join_button = types.InlineKeyboardButton(text='Присоединиться', callback_data='join_game')
keyboard.add(join_button)

game_text = '''Добро пожаловать на физтех-Мафию!🥰🥰🥰
К сожалению, в нашем мирном вузе завелись негодяи, которые делают
вид, что они честные и справедливые преподаватели, но по ночам они фачат
за даже самые мелкие недочёты в контрольных и домашках бедных студентов.
Вам нужно найти этих преподавателей и лишить их премии!😈😈😈
Желаю удачи честным преподавателям!
Через 2 минуты после начала напишите функцию next day, чтобы добраться до следующего утра'''

start_text = '''Минимальное количество участников для начала игры набралось
Чтобы начать напишите Go'''


@dp.message_handler(Text(equals='Play'))
async def start_the_connection(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id=message.chat.id,
                           text='Хотите сыграть в физтех-Мафию?🎃🎃🎃',
                           reply_markup=keyboard)


@dp.message_handler(Text(equals='Go'))
async def start_the_game(message: types.Message):
    if len(players) >= 1:
        await bot.send_message(chat_id=message.chat.id,
                               text=game_text)
        game_role = []
        buttons = []
        for i in range(len(players)):
            game_role.append(roles[i])
        random_role = random.sample(game_role, len(players))
        for j in range(len(players)):
            player = players[j]
            if random_role[j] == roles[0] or random_role[j] == roles[5] or random_role[j] == roles[8]:
                await bot.send_message(chat_id=player.id,
                                       text=f'{random_role[j]}')
                await bot.send_message(chat_id=player.id,
                                       text='''Выбери жертву
Для этого напиши команду Kill''')
            elif random_role[j] == roles[3]:
                await bot.send_message(chat_id=player.id,
                                       text=f'{random_role[j]}\nВыбери кого проверить\nДля этого напиши команду check')
            elif random_role[j] == roles[4]:
                await bot.send_message(chat_id=player.id,
                                       text=f'{random_role[j]}\nВыбери кого вылечить\nДля этого напиши команду heal')
            else:
                await bot.send_message(chat_id=player.id,
                                       text=f'{random_role[j]}\nЖди утра')
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text='Недостаточно участников для начала игры')


@dp.message_handler(Text(equals='Kill'))
async def kill_command(message: types.Message):
    Kill_kb=InlineKeyboardMarkup()
    kill_buttons=[]
    for i in range(len(players)):
        kill_buttons.append(InlineKeyboardButton(text=f'{players[i].full_name}',
                                                 callback_data=f'Kill {players[i].full_name}'))
    Kill_kb.add(*kill_buttons)
    await message.answer(text='Выбери жертву',
                         reply_markup=Kill_kb)


@dp.message_handler(Text(equals='Heal'))
async def heal_command(message: types.Message):
    Heal_kb=InlineKeyboardMarkup()
    Heal_buttons=[]
    for i in range(len(players)):
        Heal_buttons.append(InlineKeyboardButton(text=f'{players[i].full_name}',
                                                 callback_data=f'Heal {players[i].full_name}'))
    Heal_kb.add(*Heal_buttons)
    await message.answer(text='Выбери кого хочешь вылечить',
                         reply_markup=Heal_kb)


@dp.callback_query_handler(lambda c: c.data == 'join_game')
async def join_game(callback_query: types.CallbackQuery):
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
        else:
            await bot.send_message(chat_id=callback_query.message.chat.id,
                                   text=f'{user.full_name} присоединился к игре!')
        await callback_query.message.edit_text(text=f'''Хотите сыграть в физтех-Мафию?🎃🎃🎃?
{len(players)} уже в игре🥳🥳🥳''',
                                               reply_markup=keyboard)
        if len(players) >= 1:
            await bot.send_message(chat_id=callback_query.message.chat.id,
                                   text=start_text)
    else:
        await bot.send_message(chat_id=user.id,
                               text='Вы уже присоединились к игре!')

killed_players = []
healed_player = []
killed_player = []


@dp.message_handler(Text(equals='next day'))
async def next_round(message: types.Message):
    if (len(healed_player) == 1 and len(killed_player) == 1 and killed_player[0] == healed_player[0]) or len(killed_player) == 0:
        await bot.send_message(chat_id=message.chat.id,
                               text='''Сегодня ночью никто не умер, можете обсудить
кого вы считаете факером
Для начала голосвания напишите Vote''')
    elif len(killed_player) == 1:
        for player in players:
            if player == killed_player[0]:
                players.remove(player)
        await bot.send_message(chat_id=message.chat.id,
                               text=f'''Сегодня ночью умер(ла) {killed_player[0].full_name}, можете обсудить
кого вы считаете факером
Для начала голосвания напишите Vote''')
    for i in range(len(killed_players)):
        killed_players.remove(killed_players[i])
    for j in range(len(healed_player)):
        healed_player.remove(healed_player[j])
    for t in range(len(killed_player)):
        killed_player.remove(killed_player)


@dp.message_handler(Text(equals='Vote'))
async def vote(message: types.Message):
    Vote_kb = InlineKeyboardMarkup()
    vote_buttons = []
    for i in range(len(players)):
        vote_buttons.append(InlineKeyboardButton(text=f'{players[i].full_name}',
                                                 callback_data=f'Vote {players[i].full_name}'))
    Vote_kb.add(*vote_buttons)
    await message.answer(text='''Выбери факера
Через 2 минуты закройте голосование написав в чат end vote''',
                         reply_markup=Vote_kb)


votes = []


@dp.message_handler(Text(equals='end vote'))
async def vote_results(message: types.Message):
    max_votes = []
    for i in range(len(players)):
        tmp = 0
        for j in range(len(votes)):
            if players[i] == votes[j]:
                tmp += 1
        max_votes.append(tmp)
    max_count = max(max_votes)
    flag = 0
    vote_res = -1
    for i in range(len(max_votes)):
        if max_votes == max_count and flag == 0 and i != (len(max_votes) - 1):
            vote_res = i
            flag += 1
        elif max_votes == max_count and flag != 0:
            await message.answer(text='''Вы никого не выгнали, чтобы начать следующую ночь,
напишите next night''')
        elif flag == 1 and i == (len(max_votes) - 1):
            await message.answer(text=f'''Вы выгнали игрока {players[vote_res]},
чтобы начать следующую ночь, напишите next night''')
            players.remove(players[vote_res])
        elif max_votes == max_count and flag == 0 and i == (len(max_votes) - 1):
            vote_res = i
            await message.answer(text=f'''Вы выгнали игрока {players[vote_res]},
            чтобы начать следующую ночь, напишите next night''')
            players.remove(players[vote_res])


@dp.callback_query_handler()
async def Kill_Heal_Vote(callback: types.CallbackQuery):
    for player in players:
        if callback.data == f'Kill {player.full_name}':
            killed_players.append(player)
            await callback.answer('Молодец, удачи в дальнейших отчислениях')
        elif callback.data == f'Heal {player.full_name}':
            healed_player.append(player)
            await callback.answer('Молодец, надеемся, что ты спас студента от отчисления')
        elif callback.data == f'Vote {player.full_name}':
            votes.append(player)
            await bot.send_message(chat_id=callback.message.chat.id,
                                   text=f'''{callback.from_user.full_name} проголосовал в
{player.full_name}''')
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
    elif len(killed_player) == 1:
        killed_player.append(random.choice(killed_players))


async def on_startup(dp):
    print('Бот был успешно запущен!')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
