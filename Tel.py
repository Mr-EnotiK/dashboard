import asyncio
import sys  # Импортируем модуль sys для управления выходом из консоли
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import CommandStart, Command

# Вставь сюда токен, который тебе выдал BotFather при создании бота
BOT_TOKEN = "9289438212:AAE0s8MeGLYGHaCd2rNpjZD7ZDNCzSB8sjA"
# Ссылка на твое созданное Mini App в Telegram (Замени на свой точный поддомен!)
MINI_APP_URL = "https://miniapp.my1.ru/index.html"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    # Создаем элегантную инлайн-кнопку для запуска приложения
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💻 Открыть Терминал Заказов",
                web_app=WebAppInfo(url=MINI_APP_URL)
            )
        ]
    ])
    
    await message.answer(
        "Привет! Добро пожаловать в систему управления.\n\n"
        "Нажми на кнопку ниже, чтобы открыть панель управления складом и графиками продаж 👇",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# Хэндлер на команду /exit или текстовое слово "Exit" для выключения бота
@dp.message(F.text.lower() == "exit")
@dp.message(Command("exit"))
async def cmd_exit(message: Message):
    await message.answer("⚠️ Работа бота завершена. Консоль закрывается...")
    
    # Сначала закрываем сессию бота, чтобы освободить соединение
    await bot.session.close()
    
    # Останавливаем бесконечный цикл опроса aiogram
    dp.stop_polling()
    
    print("\n[INFO] Получена команда выключения. Бот остановлен администратором.")
    
    # Полностью завершаем процесс в Windows-консоли
    sys.exit(0)

# Хэндлер для приема данных обратно из Mini App, когда пользователь жмет кнопки
@dp.message(F.web_app_data)
async def handle_mini_app_data(message: Message):
    action = message.web_app_data.data
    if action == "action_open_склад":
        await message.answer("📦 Раздел *Склад* успешно запрошен. Загружаю остатки...")
    elif action == "action_open_статистика":
        await message.answer("📊 Модуль аналитики: Показ детальной статистики запущен.")

async def main():
    print("Бот успешно запущен и готов к работе!")
    # Запускаем поллинг, игнорируя старые, накопившиеся сообщения
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("[INFO] Программа успешно завершила работу.")
