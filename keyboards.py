from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text='/help')
b2 = KeyboardButton(text='/description')
b3 = KeyboardButton(text='Role')
kb.add(b1, b2).add(b3)


kb_photo = ReplyKeyboardMarkup(resize_keyboard=True)
bp1 = KeyboardButton(text='Random')
bp2 = KeyboardButton(text='Главное меню')
kb_photo.add(bp1, bp2)


ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text='❤️',
                           callback_data='like')
ib2 = InlineKeyboardButton(text='🖤',
                           callback_data='dislike')
ib3 = InlineKeyboardButton(text='Следующая роль',
                           callback_data='next_role')
ib4 = InlineKeyboardButton(text='Главное меню',
                           callback_data='main_menu')
ikb.add(ib1, ib2).add(ib3).add(ib4)


ikb_1 = InlineKeyboardMarkup(row_width=2)
ib1_1 = InlineKeyboardButton(text='Присоединиться',
                             callback_data='join')


ikb_1.add(ib1_1)
