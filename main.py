import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, 
    InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, InputFile
)
from aiogram.filters import CommandStart

# ⚠️ Вставь сюда свой токен, но не публикуй его в открытых местах!
TOKEN = "7494203016:AAEopdG_EB-t35SbkfGqYjp9fgXXay7jPHM"

# URL изображения для приветственного сообщения (замени на свою ссылку)
IMAGE_URL = "https://i.postimg.cc/CLhRSDJp/photo-2025-02-11-20-49-13.jpg"  # <-- Укажи ссылку на изображение

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список услуг с WebApp-кнопками, их описанием и индивидуальными названиями
services = {
    "🚗 ОСАГО": {
        "url": "https://golnk.ru/xl0dw",
        "description": "Оцените, сравните и оформите полис ОСАГО от 16+ надежных страховых компаний — быстро, удобно и на лучших условиях!",
        "button_text": "▶️ Запустить виджет"
    },
    "🚙 КАСКО": {
        "url": "https://golnk.ru/lpZ34",
        "description": "Защитите свой автомобиль и свои нервы — оформите КАСКО на лучших условиях! Быстро, удобно и с максимальной выгодой!",
        "button_text": "▶️ Запустить виджет"
    },
    "🏠 Страхование ипотеки": {
        "url": "https://golnk.ru/Wgb82",
        "description": "Сравните стоимость полиса ипотечного страхования в ведущих компаниях и выберите лучший вариант, соответствующий требованиям вашего банка. Экономьте время и деньги, получая оптимальные условия в один клик!",
        "button_text": "▶️ Запустить виджет"
    },
    "🏦 Прочие услуги": {
        "url": "https://golnk.ru/qJdQb",
        "description": "Мы подберем лучшие услуги с учетом большинства указанных параметров, а также предоставим возможность выбрать самые популярные финансовые продукты.",
        "button_text": "▶️ Запустить виджет"
    },
    "🏝 Экскурсии🏝": {
        "url": "https://golnk.ru/QabvB",
        "description": "Здесь вы найдете тысячи гидов с уникальным опытом и глубокими знаниями. Среди них журналисты, историки, архитекторы и другие увлеченные люди, способные захватывающе рассказывать о своих городах и странах.",
        "button_text": "🗣Забронировать"
    },
}

# Создание меню с кнопками (2 в ряд)
buttons = [KeyboardButton(text=service) for service in services.keys()]
keyboard_layout = [buttons[i:i+2] for i in range(0, len(buttons), 2)]  
main_menu = ReplyKeyboardMarkup(keyboard=keyboard_layout, resize_keyboard=True)

@dp.message(CommandStart())
async def start(message: types.Message):
    user_name = message.from_user.first_name
    
    # Отправляем изображение, если есть ссылка
    if IMAGE_URL:
        await message.answer_photo(
            photo=IMAGE_URL,
            caption=f"👋 Привет, {user_name}! Мы предлагаем вам умные решения для всех сфер жизни, чтобы вы могли сэкономить время и деньги! Оформляйте всё в одном месте — быстро, выгодно и без переплат. Получите лучшие условия без лишних усилий!",
            reply_markup=main_menu
        )
    else:
        await message.answer(
            f"👋 Привет, {user_name}! Мы предлагаем вам умные решения для всех сфер жизни, чтобы вы могли сэкономить время и деньги! Оформляйте всё в одном месте — быстро, выгодно и без переплат. Получите лучшие условия без лишних усилий!",
            reply_markup=main_menu
        )

@dp.message()
async def service_handler(message: types.Message):
    service_name = message.text
    if service_name in services:
        service_info = services[service_name]
        
        # Получаем индивидуальное название кнопки или создаем его по умолчанию
        button_text = service_info.get("button_text", f"🔗 Перейти к {service_name}")

        # Создание WebApp-кнопки с индивидуальным названием
        webapp_markup = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(
                text=button_text,
                web_app=WebAppInfo(url=service_info["url"])
            )]]
        )

        await message.answer(f"📌 {service_name}\n\n{service_info['description']}", reply_markup=webapp_markup)
    else:
        await message.answer("❌ Такой услуги нет в списке. Выберите из меню.")

async def on_startup():
    logging.info("✅ Бот успешно запущен!")

async def main():
    logging.basicConfig(level=logging.INFO)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
