from aiogram import Bot, Dispatcher, executor, types
import API_bot
from API_bot import APIClass
from bot_token import Bot_token
import json
import magic

bot = Bot(token=Bot_token)
dp = Dispatcher(bot)

OAuth = json.load(open("config.json"))["OAuth"]

api = APIClass(OAuth=OAuth)

# @dp.message_handler(commands="start")
# async def start(message: types.Message):
#     bot.send_message("please ")

@dp.message_handler(commands="download")
async def start(message: types.Message):
    start_buttons = [
        types.InlineKeyboardButton("move to dir", callback_data="cd"),
        types.InlineKeyboardButton("get file", callback_data="get_file")
    ]
    await message.answer("Downloading MetaData")
    api.GetMetaData()
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer(api.resp, reply_markup=keyboard)
    # types.CallbackQuery()
    # await message.answer("Choose", reply_markup=keyboard)
    # bot.send_document()
@dp.callback_query_handler(text="cd")
async def cd(message: types.Message):
    # await bot.delete_message(message.from_user.id, message.message.message_id)
    # dir_string = f""
    # for dir in api.list_of_data[0]:
    #     dir_string += dir
    #     dir_string += "\n"
    await bot.send_message(message.from_user.id, "Write number of directory you want to go?")
    
@dp.message_handler(lambda message: message.text.startswith("/cd"))
async def move(message: types.Message):
    dir_index = int(message.text[3:])
    api.disc_path += api.list_of_data[0][dir_index]
    api.disc_path += "/"
    api.GetMetaData()
    await message.answer(api.resp)

@dp.message_handler(lambda message: message.text.startswith("/get"))
async def get(message: types.Message):
    file_index = int(message.text[4:])
    file_name = api.list_of_data[1][file_index][0]
    # mime = magic.Magic(mime=True)
    # Content_type = mime.from_file(str(file_name))
    download_path = api.disc_path + file_name
    download_url = api.GetDownloadUrl(download_path)
    await message.answer_photo(photo=download_url)

if __name__ == "__main__":
    executor.start_polling(dp)
    