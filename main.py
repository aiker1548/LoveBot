import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from data_project import COMPLIMENTS, MSG_HELLO, TOKEN
import random


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
bot = Bot(token=TOKEN)
router = Router()

keyboard = [
    [InlineKeyboardButton(text="получить комплимент", callback_data=f"compliment")]
]
main_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(MSG_HELLO, reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Для того, чтобы получить одну из случайных мыслей нажми', reply_markup=main_keyboard)

    
@router.callback_query(F.data == 'compliment')
async def get_compliment(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(random.choice(COMPLIMENTS), reply_markup=main_keyboard)
    print(callback_query.from_user.first_name, callback_query.from_user.last_name)



if __name__ == '__main__':
    dp = Dispatcher()
    dp.include_router(router)
    asyncio.run(dp.start_polling(bot))


