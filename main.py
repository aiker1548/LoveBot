import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os

from data_project import COMPLIMENTS, MSG_HELLO, TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
bot = Bot(token=TOKEN)
router = Router()
global cx  # Объявляем переменную cx как глобальную
cx = 1  # Инициализируем переменную cx

# Главное меню
main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Антон просит прощения", callback_data="apology")],
    [InlineKeyboardButton(text="получить комплимент", callback_data="get_compliment")],
    [InlineKeyboardButton(text="получить наше случайное фото", callback_data="random_photo")]
])

# Подменю для комплиментов
compliment_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Получить комплимент", callback_data="compliment")],
    [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
])

# Подписи к фотографиям
photo_captions = {
    "1.jpg": "Тут мы сильно удивились, что оказывается телефон работает",
    "2.jpg": "О, это что та самая красивая пара, что стоят в бальном зале Екатерины второй?",
    "4.jpg": "Сюда попала даже ты одна, потому что самая красивая лапочка",
    "5.jpg": "Это мы в сексте(меня чуть не украли туда)",
    "6.jpg": "Это мы сильно едем в такси в бар, чтобы культурно выпить",
    "7.jpg": "Это я ночью ем без тебя",
    "8.jpg": "Это мы собираемся куда-то и почему-то у меня голова растет сбоку, можно сказать 'уложила' меня",
    "10.jpg": "Чувствуют стиль Эрмитажа!",
    "9.jpg": "Поминаем бедолагу",
    "3.jpg": "Интересное путешествие, с интересными разговорами позади нас"
}

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(MSG_HELLO, reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Выберите опцию:', reply_markup=main_keyboard)

@router.callback_query(F.data == 'apology')
async def handle_apology(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("Антон просит прощения")
    photo = FSInputFile('media/apologize/1.jpg')
    await callback_query.message.answer_photo(photo=photo, caption="Понимаю, что такое отношение терпеть тяжело, когда парень вот так не пишет и в себя уходит, но дурак извиняется, еще не привык к отношениям. Люблю тебя, малышка!")
    await callback_query.message.answer('Выберите опцию:', reply_markup=main_keyboard)

@router.callback_query(F.data == 'get_compliment')
async def get_compliment_menu(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("Выберите опцию:", reply_markup=create_compliment_keyboard())

@router.callback_query(F.data == 'compliment')
async def send_compliment(callback_query: types.CallbackQuery):
    compliment = random.choice(COMPLIMENTS)
    await callback_query.message.edit_text(compliment, reply_markup=create_compliment_keyboard())

@router.callback_query(F.data == 'back_to_main')
async def back_to_main(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text('Выберите опцию:', reply_markup=main_keyboard)

@router.callback_query(F.data == 'back_to_main_new')
async def back_to_main(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Выберите опцию:', reply_markup=main_keyboard)

@router.callback_query(F.data == 'random_photo')
async def handle_random_photo(callback_query: types.CallbackQuery):
    global cx  # Объявляем переменную cx как глобальную
    photo_folder = 'media/our'
    random_photo = str(cx) + '.jpg'
    
    if cx+1 == 11:
        cx = 0
    cx += 1
    caption = photo_captions.get(random_photo, "Нет подписи для этого фото.")
    photo = FSInputFile(photo_folder+'/'+random_photo)
    
    # Создаем клавиатуру с кнопками "Назад" и "Еще фото"
    photo_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main_new")],
        [InlineKeyboardButton(text="Еще фото", callback_data="random_photo")]
    ])
    await callback_query.message.answer_photo(photo=photo, caption=caption, reply_markup=photo_keyboard)

def create_compliment_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Получить комплимент", callback_data="compliment")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
    ])

@router.callback_query(F.data == 'back_to_main_new')
async def back_to_main_new(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text('Выберите опцию:', reply_markup=main_keyboard)

if __name__ == '__main__':
    dp = Dispatcher()
    dp.include_router(router)
    asyncio.run(dp.start_polling(bot))
