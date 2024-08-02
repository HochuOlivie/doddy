import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '7293560232:AAEfbhXF-bNtG1J_AY24ghfRcKUQLiCEmxM'
'''https://google.com/#tgWebAppData=query_id%3DAAEjbQprAgAAACNtCmvL9Vos%26user%3D%257B%2522id%2522%253A6090812707%252C%2522first_name%2522%253A%2522Johan%2522%252C%2522last_name%2522%253A%2522%2522%252C%2522username%2522%253A%2522shrim_l%2522%252C%2522language_code%2522%253A%2522ru%2522%252C%2522allows_write_to_pm%2522%253Atrue%257D%26auth_date%3D1722465166%26hash%3D7cb6c65514106e484bc15e0e0adfc4579762954dc753d5fff1f4baf7c34e95c8&tgWebAppVersion=7.6&tgWebAppPlatform=web&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23ffffff%22%2C%22button_color%22%3A%22%233390ec%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22hint_color%22%3A%22%23707579%22%2C%22link_color%22%3A%22%2300488f%22%2C%22secondary_bg_color%22%3A%22%23f4f4f5%22%2C%22text_color%22%3A%22%23000000%22%2C%22header_bg_color%22%3A%22%23ffffff%22%2C%22accent_text_color%22%3A%22%233390ec%22%2C%22section_bg_color%22%3A%22%23ffffff%22%2C%22section_header_text_color%22%3A%22%233390ec%22%2C%22subtitle_text_color%22%3A%22%23707579%22%2C%22destructive_text_color%22%3A%22%23df3f40%22%7D'''
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm your bot!\nPowered by aiogram.")

@dp.message_handler(commands=['webapp'])
async def send_webapp(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    web_app = types.WebAppInfo(url="https://doddynft.ru/?param=param")  # URL to your webapp
    button = types.InlineKeyboardButton(text="Open WebApp", web_app=web_app)
    keyboard.add(button)
    await message.answer("Click the button below to open the WebApp.", reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
