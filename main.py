import asyncio
import re
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from fuzzywuzzy import fuzz, process
from javoblar import javoblar

TOKEN = "7648441927:AAGTGVsJMpsu1qS2hSq5AVHJ1ABEsn3XWK8"  # O'zingizning bot tokeningizni kiriting
admin_id = 1663567950  # Adminning Telegram ID'si

bot = Bot(token=TOKEN)
dp = Dispatcher()

def chatbot(savol):
    """AktChatBotga so‘rov jo‘natish"""
    savol = savol.lower()
    togri_savol = savolni_tuzatish(savol)

    if togri_savol:
        return javoblar[togri_savol][0]

    return "Kechirasiz, bu savolga javob bera olmayman."

def savolni_tuzatish(savol):
    """Fuzzywuzzy yordamida eng mos savolni topish"""
    mos_sozlar = process.extractOne(savol, javoblar.keys(), scorer=fuzz.ratio)
    
    if mos_sozlar and mos_sozlar[1] > 60:
        return mos_sozlar[0]
    
    return None

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Salom! Savollaringizni bering, men javob beraman.")

@dp.message()
async def echo_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    text = message.text

    if user_id == admin_id and message.reply_to_message:
        try:
            match = re.search(r"\\U0001F464 ID: (\d+)", message.reply_to_message.text)
            if match:
                target_id = int(match.group(1))
                await bot.send_message(target_id, f"\U0001F4E9 *Admin javobi:\n* {message.text}", parse_mode="Markdown")
                await message.reply("✅ Javob foydalanuvchiga yuborildi.")
            else:
                await message.reply("❌ Foydalanuvchi ID topilmadi. ID formatini tekshiring.")
        except Exception as e:
            await message.reply(f"❌ Xatolik: {e}")
        return

    if user_id == admin_id:
        return

    admin_text = f"\U0001F4E9 *Yangi xabar:*\n\U0001F464 ID: `{user_id}`\n🔗 Username: @{username}\n✉️ *Xabar:* {text}"
    await bot.send_message(admin_id, admin_text, parse_mode="Markdown", disable_web_page_preview=True)

    javob = chatbot(text)
    await message.answer(javob)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
