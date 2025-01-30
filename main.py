import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os
from ai import SaigaAPI
from data_project import COMPLIMENTS, MSG_HELLO, TOKEN, TOKEN_AI, URL_AI
import datetime
from openai import AsyncOpenAI

####################
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
bot = Bot(token=TOKEN)
router = Router()
global cx  # Объявляем переменную cx как глобальную
global ai_response_time
ai_response_time = 0
cx = 1  # Инициализируем переменную cx
SAIGA_API_URL = "http://localhost:11434"
MODEL_NAME = "bambucha/saiga-llama3"
USER_ID = 480710961

saiga_api = SaigaAPI(SAIGA_API_URL, MODEL_NAME)

##########
client = AsyncOpenAI(
    api_key=TOKEN_AI,
    base_url= URL_AI
)


async def gpt_response(content):
    try:
        response = await client.chat.completions.create(
            messages= [{"role": "user", "content": content}],
            model="gpt-4o-mini",
            max_tokens=1024,
            stream=False
        )
        print(1)
        return response.choices[0].message.content
    except Exception as e:
        print(e)



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
    "3.jpg": "Интересное путешествие, с интересными разговорами позади нас",
    "11.jpg": "О это же мы мелкие",
    "12.jpg": "Это мы в самолете и у тебя губы трубочкой",
    "13.jpg": "Упс, а тут уже у меня...",
    "14.jpg": "Это получается цифровое фото наших нецифровых фото... ой заумно",
    "15.jpg": "Привеееееет!"
    
}

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(MSG_HELLO, reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Выберите опцию:', reply_markup=main_keyboard)

@router.message(F.from_user.id == USER_ID)
async def handle_message_from_user(message: types.Message):
    global ai_response_time
    print(ai_response_time)
    if ai_response_time == 0:
        ai_response_time = datetime.datetime.now()

    elif (datetime.datetime.now() - ai_response_time).seconds < 10:
        print('no time')
        return 
    ai_response_time = datetime.datetime.now()
    user_message = message.text

    prompt = f"Маша пишет: \"{user_message}\"\nОтветь ей комплиментом в молодежном стиле, подчеркни ее красоту, назови красоткой и крошкой. Пожелай прекрасного настроения и напомни, что она самая милая и любимая девочка Антона.."
    
    # Генерируем комплимент
    
    #response = saiga_api.generate_response(prompt)
    response = await gpt_response(prompt)
    print(response)
    await message.answer(response)

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
    
    if cx+1 == 16:
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
