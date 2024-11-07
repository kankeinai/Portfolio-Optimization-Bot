import asyncio
import logging
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters import StateFilter
import logging
import os
from config import *
from utils import *
from keyboards import *
import random
import numpy as np

class Form(StatesGroup):
    projects_data = State()
    submit_param = State()
    advanced_param = State()
    advanced = State()
    ready = State()
    simple = State()
 
form_router = Router()
folder_name = ""
user_name = ""


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,)



# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    global folder_name
    global user_name

    if message.from_user.username:
        user_name = message.from_user.username
    else:
        user_name = "friend"


    if folder_name=="":
        folder_name = "user_"+str(message.from_user.id)
        await repository_exist(folder_name)

    file_path = "example_files/instructions.pdf"

    if os.path.exists(file_path):
        # Use FSInputFile to load the file
        document = FSInputFile(file_path)

    await message.answer(f"Hello {user_name}! I am so happy to help you with portfolio optimization today.")
    await bot.send_sticker(chat_id=message.chat.id, sticker=STICKERS['hi'])
    await asyncio.sleep(1)
    await message.answer("For now, you can read this instructions file. It dives deeper into the problem and explains what I am doing.")
    await asyncio.sleep(1)
    await bot.send_document(chat_id=message.chat.id, document=document)
    await asyncio.sleep(1)
    await message.answer("Once you are ready, you can you use command /help and I will explain what to do next.")
    await message.answer("By the way, if you text something out of topic, I can share a joke with you :D.")
    
    

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    global folder_name
    if folder_name=="":
        folder_name = "user_"+str(message.from_user.id)
        await repository_exist(folder_name)

    await message.answer("Oh, wow! You are already here.")
    await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['celebrate']))
    
    text = [
        "Hm lets start from the basics. To start optimization process, you need to use command /optimize and at any point you can abort optimization by writing /abort.",
        "At each step, you will be explained what to do.",
        "I believe in you! :D"
    ]
    for t in text:
        await message.answer(t)
        await asyncio.sleep(1)


    await asyncio.sleep(3)

    await message.answer("Just run /optimize and see what happens xD")

@dp.message(Command("optimize"))
async def cmd_optimize(message: types.Message, state: FSMContext):
    
    await message.answer("Lets optimize! You can abort it by writing /abort.")
    await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['celebrate']))
    text = [
        "First, provide me with data about projects in .csv, .xlsx (multiple tabs are allowed) formats.",
        "Dataset should include at least next columns: \"profit\", \"project\"(name), \"risk\"(probability between 0 and 1), \"cost\", \"dependence\".\n\nMake sure that names of columns are the same. Possible inputs for \"dependence\" can be found in example file."
    ]
    for t in text:
        await message.answer(t)
        await asyncio.sleep(2)
    
    global folder_name
    folder_name = "user_" + str(message.from_user.id)
    await repository_exist(folder_name)

    await message.answer(f"Here is example file.") 
    file_path = "example_files/sample.xlsx"

    if os.path.exists(file_path):
        # Use FSInputFile to load the file
        document = FSInputFile(file_path)
        await bot.send_document(chat_id=message.chat.id, document=document)
    
    text = [f"Please upload as many files as you wish. Once you finish uploading just text 'next'.",
            "If there are any problems with files, I will let you know."]
    for t in text:
        await message.answer(t)
        await asyncio.sleep(1)

    await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['yes']))

    await state.set_state(Form.projects_data)


@form_router.message(Form.projects_data)
async def handle_data_documents(message: types.Message, state: FSMContext):
    global folder_name

    if folder_name=="":
        folder_name = "user_"+str(message.from_user.id)
        if not os.path.isdir(folder_name):
            os.makedirs(folder_name, exist_ok=True)
            
    document = message.document

    if document:
        file_name = message.document.file_name

        # Check if the file extension is allowed
        if file_name.endswith(('.xlsx', '.csv')):
            file_id = message.document.file_id
            file = await bot.get_file(file_id)

            # Define the download path
            download_path = f"{folder_name}/{file_name}"

            # Download the file
            await bot.download_file(file.file_path, download_path)
            output = process_file(folder_name, download_path)

            if output:
                if os.path.exists(download_path):
                    os.remove(download_path)
                await message.answer(f"File is not accepted, here is a log message.\n\n{output}") 
                if np.random.rand()>=0.5:
                    await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['error']))
            else:
                await message.answer(f"File is accepted! If you finished uploading, text 'next'", reply_markup=next_keyboard()) 
        else:
            await message.answer(f"Only .csv, .xlsx files are accepted.") 
            if np.random.rand()>=0.5:
                    await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['error']))
    if message.text:
        text = message.text.lower()


        if text == "next":

            csv_file_count = len([file for file in os.listdir(folder_name) if file.endswith(".csv") and os.path.isfile(os.path.join(folder_name, file))])

            if csv_file_count>0:
                await message.answer(f"Thanks for submitting the files!") 
                if np.random.rand()>=0.5:
                    await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['yes']))

                text = """Do you want to change default parameters of the model:\n(M = 100, U = none, budget = 100000)"""
                await message.answer(text, reply_markup = yes_no_keyboard()) 
            
                await state.set_state(Form.submit_param)
            else:
                await message.answer(f"You haven't uploaded any files yet.")
                if np.random.rand()>=0.5:
                    await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['error']))
        elif text == "/abort":
            await repository_exist(folder_name)
            await message.answer("Optimization is aborted by user, all files are deleted")
            await state.clear() 
        else:
            await message.answer(f"I don't understand your message. Please upload file or respond 'next'", reply_markup = next_keyboard())
            await bot.send_sticker(chat_id=message.chat.id, sticker=STICKERS['dont'])
    
@form_router.message(Form.submit_param)
async def param_document(message: types.Message, state: FSMContext):
    if message.text:        
        text = message.text.lower()
        if text == "no":
            await message.answer("I will use default parameters for these projects.")
            await state.update_data(params=(100, None, 100000))
            await message.answer("Do you want to use advanced formulation?", reply_markup = yes_no_keyboard())
            await state.set_state(Form.advanced)

        elif text == "yes":
            await message.answer("You need to provide me 3 parameters:\nM (integer number, M>0), U (integer number, U>0), budget\n\nExample input:\n100, 20, 100000")
            await state.set_state(Form.simple)
        elif text == "/abort":
            await repository_exist(folder_name)
            await message.answer("Optimization is aborted by user, all files are deleted")
            await state.clear()
        else:
            await message.answer("Sorry, I don't understand. Plese write 'yes'/'no'", reply_markup = yes_no_keyboard())
            await bot.send_sticker(chat_id=message.chat.id, sticker=STICKERS['dont'])
    else:
        await message.answer("I don't understand. Please write 'yes'/'no'", reply_markup = yes_no_keyboard())
        await bot.send_sticker(chat_id=message.chat.id, sticker=STICKERS['dont'])

@form_router.message(Form.simple)
async def param_document(message: types.Message, state: FSMContext):    
    if message.text:
        if message.text == "/abort":
            await repository_exist(folder_name)
            await message.answer("Optimization is aborted by user, all files are deleted")
            await state.clear()
        try:
            text_no_spaces = re.sub(r'\s+', '', message.text)
            M, U, budget = map(to_number, text_no_spaces.split(','))

            if U>0 and M>0:
                if isinstance(U, int) and isinstance(M, int):
                    await state.update_data(params=(M, U, budget))
                    await message.answer("Great! Do you want to use advanced formulation?", reply_markup = yes_no_keyboard())
                    if np.random.rand()>=0.5:
                            await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['yes']))
                    await state.set_state(Form.advanced)
                else:
                    await message.answer("Invalid input. M and U should be integers.")
                    if np.random.rand()>=0.5:
                        await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['error']))
            else:
                await message.answer("Invalid input. M and U should be positive integers.")
                if np.random.rand()>=0.5:
                    await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['error']))
        except:
            await message.answer("Invalid input. Please provide M, U, budget in the format: 100, 20, 100000")   
            if np.random.rand()>=0.5:
                    await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['error']))   
    else:
        await message.answer("Invalid input. Please provide M, U, budget in the format: 100, 20, 100000")
        if np.random.rand()>=0.5:
                    await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['error']))

@form_router.message(Form.advanced)
async def advanced(message: types.Message, state: FSMContext):
    if message.text:

        text = message.text.lower()

        if text == "yes":
            await message.answer("I will use advanced formulation for these projects.")
            await state.update_data(advanced=True)
            await message.answer("You need to provide me 3 parameters: threshold, max_violation, tolerance (between 0 and 1)\n\nExample input:\n1000, 2000, 0.9")
            if np.random.rand()>=0.5:
                await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['yes']))
            await state.set_state(Form.advanced_param)
        elif text == "no":
            await message.answer("I will use simple formulation for these projects.")
            await state.update_data(advanced=False)
            await message.answer("Final question: do you want a full analysis report?", reply_markup= yes_no_keyboard())
            if np.random.rand()>=0.5:
                await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['yes']))
            await state.set_state(Form.ready)
        elif text == "/abort":
            await repository_exist(folder_name)
            await message.answer("Optimization is aborted by user, all files are deleted")
            await state.clear()
        else:
            await message.answer("Sorry, I don't understand. Plese write 'yes'/'no'", reply_markup = yes_no_keyboard())
            await bot.send_sticker(chat_id=message.chat.id, sticker=STICKERS['dont'])
    else:
        await message.answer("Sorry, I don't understand. Plese write 'yes'/'no'", reply_markup = yes_no_keyboard())
        await bot.send_sticker(chat_id=message.chat.id, sticker=STICKERS['dont'])


@form_router.message(Form.advanced_param)
async def final_step(message: types.Message, state: FSMContext):
    params = message.text
    global folder_name
    folder_name = message.from_user.id
    if params:
        if params == "/abort":
            await repository_exist(folder_name)
            await message.answer("Optimization is aborted by user, all files are deleted")
            await state.clear()
        else:
            try:
                text_no_spaces = re.sub(r'\s+', '', params)
                threshold, max_violation, tolerance = map(float, text_no_spaces.split(','))
                if tolerance<=1 and tolerance>=0:
                    await state.update_data(advanced_params=(threshold, max_violation, tolerance))
                    await message.answer("Final question: do you want a full analysis report?", reply_markup = yes_no_keyboard())
                    if np.random.rand()>=0.5:
                        await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['yes']))
                    await state.set_state(Form.ready)
                else:
                    await message.answer("Invalid input. Tolerance should be between 0 and 1.")
                    if np.random.rand()>=0.5:
                        await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['error']))
            except:
                await message.answer("Invalid input. Please provide threshold, max_violation, tolerance in the format: 1000, 2000, 0.9")
                if np.random.rand()>=0.5:
                    await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['error']))
    else:
        await message.answer("Sorry, I don't understand.\nPlese provide threshold, max_violation, tolerance in the format:\n1000, 2000, 0.9")
        await bot.send_sticker(chat_id=message.chat.id, sticker=STICKERS['dont'])
            

@form_router.message(Form.ready)
async def final_step(message: types.Message, state: FSMContext):

    global folder_name
    folder_name = "user_"+str(message.from_user.id)

    if message.text:
        if message.text=="/abort":
            await repository_exist(folder_name)
            await message.answer("Optimization is aborted by user, all files are deleted")
            await state.clear()
        else:
            text = message.text.lower()

            data = await state.get_data()
            M, U, budget = data.get('params')
            advanced = data.get('advanced')
            if advanced:
                threshold, max_violation, tolerance = data.get('advanced_params')
            else:
                threshold, max_violation, tolerance = None, None, None

            analysis =  text == "yes"
            if analysis:
                await message.answer("I will start optimization and make a report for you. Please wait a moment.")
                if np.random.rand()>=0.5:
                    await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['yes']))
            else:
                await message.answer("I will start optimization and report will be without analysis. Please wait a moment.")
                if np.random.rand()>=0.5:
                    await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['yes']))
            
            report = await generate_project_portfolio_report(message.from_user.id,folder_name, M,  budget, analysis=analysis, advanced=advanced, U=U, threshold=threshold, tolerance_level=tolerance, max_violation=max_violation)
            
            

            if report:
                await message.answer("Your report is ready! Hope you like it :з")
                await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['celebrate']))

                if os.path.exists(report):
                    document = FSInputFile(report)
                    await bot.send_document(chat_id=message.chat.id, document=document)
                    os.remove(report)
            else:
                await message.answer("An error occurred while generating the report :(")
                await message.answer("Please try again or contact @katteelsker")
                if np.random.rand()>=0.5:
                    await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['error']))

            await state.clear() 
    else:
        await message.answer("Sorry, I don't understand. Plese write 'yes'/'no'", reply_markup = yes_no_keyboard())
        await bot.send_sticker(chat_id=message.chat.id, sticker=STICKERS['dont'])


@form_router.message(StateFilter(None))
async def echo_message(message: types.Message, state: FSMContext):

    text = message.text

    if text == "/abort":
       await message.answer("Sorry this command works only during optimization")
       if np.random.rand()>=0.5:
        await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(STICKERS['error']))
    elif text =="/start" or text =="/help" or text =="/optimize":
        pass
    else:
        await message.answer(random.choice(UNRELATED_RESPONSES))

async def main():
    await dp.start_polling(bot)

dp.include_router(form_router)

if __name__ == "__main__":
    asyncio.run(main())

    