import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

API_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
    "?ids=bitcoin,ethereum&vs_currencies=usd"
)


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! 👋\n"
        "Я покажу курс криптовалют.\n\n"
        "Команда:\n"
        "/price — курс BTC и ETH"
    )


@dp.message(Command("price"))
async def price(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            data = await response.json()

    btc_price = data["bitcoin"]["usd"]
    eth_price = data["ethereum"]["usd"]

    text = (
        "💴 **Курсы криптовалют:**\n\n"
        f"🪙 **Bitcoin (BTC):** ${btc_price}\n"
        f"💎 **Ethereum (ETH):** ${eth_price}"
    )

    await message.answer(text, parse_mode="Markdown")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
