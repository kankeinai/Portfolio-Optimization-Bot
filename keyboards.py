from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def yes_no_keyboard():
    # Initialize the reply keyboard with "Yes", "No", and "/abort" buttons
    reply_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Yes"), KeyboardButton(text="No")],  # "Yes" and "No" in the same row
            [KeyboardButton(text="/abort")]  # "/abort" button on a new row
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_kb

def next_keyboard():
    # Initialize the reply keyboard with "Next" and "/abort" buttons
    reply_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Next")],  # "Next" button in a single row
            [KeyboardButton(text="/abort")]  # "/abort" button on a new row
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_kb