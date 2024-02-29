import asyncio
import logging

# import g4f

from decouple import config


from aiogram import Bot, Dispatcher, Router, types,F
from aiogram.filters import CommandStart, Command   


TOKEN = config("TOKEN")

dp = Dispatcher() # объект диспетчера (оброботчик событий)
bot = Bot(TOKEN)

# async - асинхронная функция (позволяет не блокировать выполнение кода)
# await - ожидание выполнения асинхронной функции
FILE_STORAGE = "photos.txt"

cats = [
    'https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_square.jpg',
]

def read_photos():
    with open(FILE_STORAGE, "r") as file:
        return file.read().split("\n")

def write_photos(photos):
    with open(FILE_STORAGE, "w") as file:
        file.write("\n".join(photos))


all_photos = read_photos()




@dp.message(F.sticker)
async def sticker_handler(message: types.Message):
    print(message.sticker.file_id)
    await message.answer_sticker(message.sticker.file_id)
    await message.reply_sticker(message.sticker.file_id)

@dp.message(F.photo)
async def photo_handler(message: types.Message):
    all_photos.append(message.photo[-1].file_id)
    write_photos(all_photos)
    
    await message.answer(f'Фото додано до списку!\nВсього фото: {len(all_photos)}\n\n Для перегяду отстанніх 5 фото введіть /show_photos')



@dp.message(Command("show_photos"))
async def show_photos(message: types.Message):
    for photo in all_photos[-5:]:
        await message.answer_photo(photo)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer_video("BAACAgIAAxkBAAKiw2XU6F4hG-VwkckeqIOBgC4ShhfzAALwRQACBpqpSnDNr9yNiaGVNAQ") # 1
    await message.answer_video_note("BAACAgIAAxkBAAKiw2XU6F4hG-VwkckeqIOBgC4ShhfzAALwRQACBpqpSnDNr9yNiaGVNAQ") # 2
    await message.answer_photo(cats[0]) # 3
    await message.answer_photo('https://cdn.britannica.com/34/235834-050-C5843610/two-different-breeds-of-cats-side-by-side-outdoors-in-the-garden.jpg')
    await message.answer("Привіт!")

@dp.message()
async def echo_handler(message: types.Message):
    print(message.video)

    # print(message.text)
    # response = await g4f.ChatCompletion.create_async(
    #     model=g4f.models.default,
    #     messages=[{"role": "user", "content": f"{message.text}"}],
    #     timeout=120,  # in secs
    # )
    # print(f"Result:", response)
    # await message.answer(response, parse_mode="Markdown")


async def main() -> None:
    print("Start bot")
    me =await bot.get_me()
    # await bot.send_message(222201019, "START BOT")
    # await bot.send_sticker(222201019, "CAACAgIAAxkBAAKhX2XU1K_wfVtf-g-T4IfN16G-RtyzAAJNIgACoIGxSZc78ssXH64VNAQ")
    print("Bot username:", me.username)
    await dp.start_polling(bot)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    asyncio.run(main())