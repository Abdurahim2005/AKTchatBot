import asyncio
import re
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
import difflib
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
    """Noto‘g‘ri so‘zni eng yaqin variant bilan almashtiradi"""
    savol = savol.lower()
    mos_sozlar = difflib.get_close_matches(savol, javoblar.keys(), n=1, cutoff=0.6)
    
    if mos_sozlar:
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

    # **1. ADMIN REPLY QILGAN BO‘LSA**
    if user_id == admin_id and message.reply_to_message:
        try:
            match = re.search(r"👤 ID: (\d+)", message.reply_to_message.text)  # IDni olish
            if match:
                target_id = int(match.group(1))  # Reply xabaridan foydalanuvchi ID ni olish

                if message.text:
                    await bot.send_message(target_id, f"📩 *Admin javobi:\n* {message.text}", parse_mode="Markdown")
                elif message.photo:
                    await bot.send_photo(target_id, message.photo[-1].file_id, caption="📩 *Admin javobi:*", parse_mode="Markdown")
                elif message.video:
                    await bot.send_video(target_id, message.video.file_id, caption="📩 *Admin javobi:*", parse_mode="Markdown")
                elif message.document:
                    await bot.send_document(target_id, message.document.file_id, caption="📩 *Admin javobi:*", parse_mode="Markdown")

                await message.reply("✅ Javob foydalanuvchiga yuborildi.")  # Adminga tasdiq xabari

            else:
                await message.reply("❌ Foydalanuvchi ID topilmadi. ID formatini tekshiring.")

        except Exception as e:
            await message.reply(f"❌ Xatolik: {e}")  # Xatolikni terminalga chiqarish

        return  # Admin xabari qayta ishlanmasligi uchun


    # **2. ADMIN REPLY QILMAGAN BO‘LSA**
    if user_id == admin_id:
        return  # Adminning oddiy xabarlari bot tomonidan qayta ishlanmaydi

    # **3. FOYDALANUVCHI XABAR YUBORGAN BO‘LSA**
    if username:
        user_link = f"[@{username}](tg://user?id={user_id})"
        username_text = f"@{username}"
    else:
        user_link = f"[Foydalanuvchi](tg://user?id={user_id})"
        username_text = "@username mavjud emas"

    admin_text = f"📩 *Yangi xabar:*\n👤 ID: `{user_id}`\n🔗 Username: {username_text}\n✉️ *Xabar:* {text}\n\n👥 {user_link}"
    await bot.send_message(admin_id, admin_text, parse_mode="Markdown", disable_web_page_preview=True)

    # **4. CHATBOT JAVOBI**
    javob = chatbot(text)
    await message.answer(javob)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
