import asyncio

from aiogram import Bot, Dispatcher, F, exceptions
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

bot_token = "7451801913:AAGB3WRh_7wtg4p9_vDT1HldTfUf78-fAIc"

bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

menu = [
    [InlineKeyboardButton(text="1", callback_data="add:1"), InlineKeyboardButton(text="2", callback_data="add:2"), InlineKeyboardButton(text="3", callback_data="add:3")],
    [InlineKeyboardButton(text="4", callback_data="add:4"), InlineKeyboardButton(text="5", callback_data="add:5"), InlineKeyboardButton(text="6", callback_data="add:6")],
    [InlineKeyboardButton(text="7", callback_data="add:7"), InlineKeyboardButton(text="8", callback_data="add:8"), InlineKeyboardButton(text="9", callback_data="add:9")],
    [InlineKeyboardButton(text="+", callback_data="add: + "), InlineKeyboardButton(text="×", callback_data="add: × "), InlineKeyboardButton(text="0", callback_data="add:0"), InlineKeyboardButton(text="÷", callback_data="add: ÷ "), InlineKeyboardButton(text="-", callback_data="add: - ")],
    [InlineKeyboardButton(text="=", callback_data="calculate"), InlineKeyboardButton(text="⌫", callback_data="delete")]
]

menu = InlineKeyboardMarkup(inline_keyboard=menu)


@dp.message(CommandStart)
async def start(message: Message) -> None:

    await message.answer("Приветствую, я бот–калькулятор, введи любое число, выбери операцию и получи ответ!", reply_markup=menu)


@dp.callback_query(F.data.startswith("add:"))
async def add(call: CallbackQuery) -> None:

    symbol = call.data.replace("add:", "")
    text = call.message.text

    if len(symbol) == 3:

        if symbol[-2] in "+×÷-" and text == "Приветствую, я бот–калькулятор, введи любое число, выбери операцию и получи ответ!":

            await call.answer()
            return

        if symbol[-2] in "+-×÷" and text[-2] in "+-×÷":

            text = text[:-3]

    if text == "Приветствую, я бот–калькулятор, введи любое число, выбери операцию и получи ответ!":

        symbol = f"\n\n{symbol}"

    try:

        await call.message.edit_text(text + symbol, reply_markup=menu)

    except exceptions.TelegramBadRequest:

        await call.answer()


@dp.callback_query(F.data.startswith("delete"))
async def delete(call: CallbackQuery) -> None:

    if call.message.text == "Приветствую, я бот–калькулятор, введи любое число, выбери операцию и получи ответ!":

        await call.answer()
        return

    if call.message.text[-1] == " ":

        await call.message.edit_text(call.message.text[:-3], reply_markup=menu)

    else:

        await call.message.edit_text(call.message.text[:-1], reply_markup=menu)


@dp.callback_query(F.data.startswith("calculate"))
async def calculate(call: CallbackQuery) -> None:

    if call.message.text == "Приветствую, я бот–калькулятор, введи любое число, выбери операцию и получи ответ!":

        await call.answer()
        return

    example = call.message.text.replace("Приветствую, я бот–калькулятор, введи любое число, выбери операцию и получи ответ!\n\n", "").replace("×", "*").replace("÷", "/").replace(" ", " ")

    if call.message.text[-1] == " ":

        await call.answer("Пожалуйста, завершите математическое уравнение или удалите последний символ.", show_alert=True)
        return

    try:

        answer = eval(example)
        example = example.replace("*", "×").replace("/", "÷")

        keyboard = [
            [InlineKeyboardButton(text="⟵ Калькулятор", callback_data="calculator")]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

        await call.message.edit_text(f"{example} = {int(answer) if answer == int(answer) else round(answer, 7)}", reply_markup=keyboard)

    except ZeroDivisionError:

        keyboard = [
            [InlineKeyboardButton(text="⟵ Калькулятор", callback_data="calculator")]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

        await call.message.edit_text("Произошла ошибка при вычислении примера: деление на ноль невозможно.", reply_markup=keyboard)

    except Exception as e:

        keyboard = [
            [InlineKeyboardButton(text="⟵ Калькулятор", callback_data="calculator")]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

        await call.message.edit_text(f"Произошла ошибка при вычислении примера: {str(e)}.", reply_markup=keyboard)


@dp.callback_query(F.data == "calculator")
async def calculator(call: CallbackQuery) -> None:

    await call.message.edit_text("Приветствую, я бот–калькулятор, введи любое число, выбери операцию и получи ответ!", reply_markup=menu)


async def main() -> None:

    await dp.start_polling(bot)


if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        print("Бот остановлен пользователем.")
