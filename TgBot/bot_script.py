from re import U
from aiogram import Bot, Dispatcher, executor, types
import API_bot
from API_bot import APIClass, Mod
from bot_token import Bot_token
import json
import magic
import requests
from pathlib import Path

bot = Bot(token=Bot_token)
dp = Dispatcher(bot)

Users = {}

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
    await bot.delete_message(message.chat.id, message.message_id)
    await message.answer("Your OAuth saved")

@dp.message_handler(commands="download")
async def download(message: types.Message):
    user_id = message.from_id
    Users[user_id].mod = Mod.DOWNLOAD
    Users[user_id].disk_path = '/'
    await message.answer("Downloading MetaData")
    Users[user_id].GetMetaData()
    Users[user_id].MetaDataDownload()
    await message.answer(Users[user_id].resp)

@dp.message_handler(commands="upload")
async def download(message: types.Message):
    user_id = message.from_id
    Users[user_id].mod = Mod.UPLOAD
    Users[user_id].disk_path = '/'
    await message.answer("Choose upload path, than just upload file")
    Users[user_id].GetMetaData()
    Users[user_id].MetaDataUpload()
    await message.answer(Users[user_id].resp)
    
@dp.message_handler(lambda message: message.text.startswith("/cd"))
async def move(message: types.Message):
    user_id = message.from_id
    dir_index = int(message.text[3:])
    Users[user_id].disk_path += Users[user_id].list_of_data[0][dir_index]
    Users[user_id].disk_path += "/"
    Users[user_id].GetMetaData()
    Users[user_id].MetaDataDownload()
    await message.answer(Users[user_id].resp)

# @dp.message_handler(content_types=['photo'])
# async def photo(message: types.Message):
#     user_id = message.from_id
#     file_id = json.loads(message.as_json())['photo'][-1]["file_id"]
#     file_name = message.text
#     file = await bot.get_file(file_id)
#     # print(file.file_size)
#     download_url = f"https://api.telegram.org/file/bot{Bot_token}/{file.file_path}"
#     Users[user_id].UploadViaLink(download_url, str(file_name))
#     await message.answer("kek")

@dp.message_handler(content_types=['document'])
async def photo(message: types.Message):
    user_id = message.from_id
    file_id = message.document.file_id
    file_name = message.document.file_name
    file = await bot.get_file(file_id)
    download_url = f"https://api.telegram.org/file/bot{Bot_token}/{file.file_path}"
    Users[user_id].UploadViaLink(download_url, str(file_name))
    await message.answer("your file downloaded successfully")

@dp.message_handler(lambda message: message.text.startswith("/back"))
async def move(message: types.Message):
    user_id = message.from_id
    Users[user_id].disk_path = str(Path(Users[user_id].disk_path).parent)
    Users[user_id].GetMetaData()
    Users[user_id].MetaDataDownload()
    await message.answer(Users[user_id].resp)

@dp.message_handler(lambda message: message.text.startswith("/root"))
async def move(message: types.Message):
    user_id = message.from_id
    Users[user_id].disk_path = str(Path(Users[user_id].disk_path).root)
    Users[user_id].GetMetaData()
    Users[user_id].MetaDataDownload()
    await message.answer(Users[user_id].resp)

@dp.message_handler(lambda message: message.text.startswith("/get"))
async def get(message: types.Message):
    user_id = message.from_id
    file_index = int(message.text[4:])
    file_name = Users[user_id].list_of_data[1][file_index][0]
    # mime = magic.Magic(mime=True)
    # Content_type = mime.from_file(str(file_name))
    download_path = Users[user_id].disk_path + file_name
    download_url = Users[user_id].GetDownloadUrl(download_path)
    await message.answer_photo(photo=download_url)

if __name__ == "__main__":
    executor.start_polling(dp)