from aiogram import Bot, Dispatcher, executor, types
import API_bot
from API_bot import APIClass
from bot_token import Bot_token
import json
import magic

bot = Bot(token=Bot_token)
dp = Dispatcher(bot)

# OAuth = json.load(open("config.json"))["OAuth"]
Users = {}
# api = APIClass(OAuth=OAuth)

@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer("please follow the link with the id of your Yandexapp with permission to change YandexDisk\n"\
                    "https://oauth.yandex.ru/authorize?response_type=token&client_id=<app Id>\nplease send OAuth "\
                    "in format </OAuth \"your OAuth\">")

@dp.message_handler(lambda message: message.text.startswith("/OAuth"))
async def OAuth(message: types.Message):
    user_id = message.from_id
    print(f"User {user_id} started")
    if message.text.count(" ") == 1:
        command, OAuth = message.text.split()
    else:
        OAuth = message.text[6:]
        print(OAuth)
    Users[user_id] = APIClass(OAuth=OAuth)
    await message.answer("Your OAuth saved")

@dp.message_handler(commands="download")
async def download(message: types.Message):
    user_id = message.from_id
    start_buttons = [
        types.InlineKeyboardButton("move to dir", callback_data="cd"),
        types.InlineKeyboardButton("get file", callback_data="get_file")
    ]
    await message.answer("Downloading MetaData")
    Users[user_id].GetMetaData()
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer(Users[user_id].resp, reply_markup=keyboard)
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
    user_id = message.from_id
    dir_index = int(message.text[3:])
    Users[user_id].disc_path += Users[user_id].list_of_data[0][dir_index]
    Users[user_id].disc_path += "/"
    Users[user_id].GetMetaData()
    await message.answer(Users[user_id].resp)

@dp.message_handler(lambda message: message.text.startswith("/get"))
async def get(message: types.Message):
    user_id = message.from_id
    file_index = int(message.text[4:])
    file_name = Users[user_id].list_of_data[1][file_index][0]
    # mime = magic.Magic(mime=True)
    # Content_type = mime.from_file(str(file_name))
    download_path = Users[user_id].disc_path + file_name
    download_url = Users[user_id].GetDownloadUrl(download_path)
    await message.answer_photo(photo=download_url)

if __name__ == "__main__":
    executor.start_polling(dp)