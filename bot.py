import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode

# ==========================================
# SOZLAMALAR (TOKEN VA ADMINLAR)
# ==========================================
BOT_TOKEN = "9117090922:AAHBdLtCq7bGsSbcnNoiFT_xCQZCh4xetcc"
ADMIN_IDS = [6258110646, 7645769320]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Adminlar uchun menyu tugmalari
admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📢 Barchaga Broadcast yuborish"),
            KeyboardButton(text="🧹 Chatni tozalash")
        ],
        [
            KeyboardButton(text="💡 Yordam & Qo'llanma")
        ]
    ],
    resize_keyboard=True
)

# ==========================================
# /start BUYRUG'I
# ==========================================
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    if user_id in ADMIN_IDS:
        await message.answer(
            "👩‍⚕️ <b>Assalomu alaykum, Doktor Surayyo Vahobjonovna!</b>\n\n"
            "Klinika rasmiy saytidan (<b>ginekologplastikxirurg.uz</b>) kelgan "
            "barcha bemor savollari shu yerga keladi.\n\n"
            "↩️ <b>Javob berish tartibi:</b> Bemor savoli yozilgan xabarga "
            "<i>Reply (Javob berish)</i> qilib yozing — xabar darhol bemor ekranida ko'rinadi.",
            parse_mode=ParseMode.HTML,
            reply_markup=admin_keyboard
        )
    else:
        await message.answer(
            "Assalomu alaykum! <b>Doktor Surayyo Vahobjonovna</b> — Estetik ginekologiya "
            "va plastik jarrohlik klinikasining rasmiy botiga xush kelibsiz.\n\n"
            "Savolingizni shu yerga yozib qoldirishingiz yoki saytimiz orqali murojaat qilishingiz mumkin:\n"
            "🌐 https://ginekologplastikxirurg.uz\n"
            "📞 Tel: +998 95 277 53 54",
            parse_mode=ParseMode.HTML
        )

# ==========================================
# ADMIN TUGMALARI HANDLERLARI
# ==========================================
@dp.message(F.text == "📢 Barchaga Broadcast yuborish")
async def btn_broadcast(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    await message.answer(
        "📢 <b>Ommaviy Broadcast:</b>\n"
        "Sayt orqali yozgan bemorlarning ma'lumotlari brauzer keshida (<code>localStorage</code>) saqlanadi. "
        "Har bir bemorga alohida javob berish uchun uning savoliga <b>Reply</b> qiling.",
        parse_mode=ParseMode.HTML
    )

@dp.message(F.text == "🧹 Chatni tozalash")
async def btn_clear_chat(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    await message.answer(
        "🧹 Telegram chatini tozalash uchun keraksiz xabarlarni belgilab, "
        "yuqoridagi <b>O'chirish (Delete)</b> tugmasini bosing.",
        parse_mode=ParseMode.HTML
    )

@dp.message(F.text == "💡 Yordam & Qo'llanma")
async def btn_help(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    await message.answer(
        "💡 <b>Shifokor uchun qo'llanma:</b>\n\n"
        "1️⃣ Saytdan yangi savol kelganda xabarda <code>ID-XXXXXX</code> bemor kodi ko'rinadi.\n"
        "2️⃣ Bemorga javob yuborish uchun o'sha xabarga <b>Reply (Javob berish)</b> qilib matn yozing.\n"
        "3️⃣ Javobingiz 5 soniya ichida bemorning saytdagi chat oynasida paydo bo'ladi.\n"
        "4️⃣ Rasm va fayllar xavfsizlik sababli qabul qilinmaydi — faqat matnli xabarlar ishlaydi.",
        parse_mode=ParseMode.HTML
    )

# ==========================================
# SHIFOKOR JAVOBINI (REPLY) TASDIQLASH
# ==========================================
@dp.message(F.reply_to_message)
async def handle_doctor_reply(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    replied_text = message.reply_to_message.text or ""
    if "ID-" in replied_text:
        # Bemor ID kodini ajratib olish
        patient_id = "Noma'lum"
        for word in replied_text.split():
            if word.startswith("ID-"):
                patient_id = word.strip(".,:;()[]")
                break

        await message.reply(
            f"✅ Javobingiz <b>{patient_id}</b> kodli bemorga yuborildi!",
            parse_mode=ParseMode.HTML
        )

# ==========================================
# ODDIY FOYDALANUVCHI XABARLARINI ADMINLARGA YUBORISH
# ==========================================
@dp.message()
async def forward_user_message(message: types.Message):
    user = message.from_user
    if user.id in ADMIN_IDS:
        return

    if not message.text:
        await message.answer("⚠️ Xavfsizlik qoidasi: Rasm yoki fayllar qabul qilinmaydi. Iltimos, savolingizni faqat matn ko'rinishida yozing.")
        return

    full_name = user.full_name or "Foydalanuvchi"
    username = f"@{user.username}" if user.username else "yo'q"

    alert_text = (
        f"📩 <b>TELEGRAM BOTDAN YANGI SAVOL</b>\n\n"
        f"👤 <b>Mijoz:</b> {full_name} ({username})\n"
        f"🆔 <b>Telegram ID:</b> <code>{user.id}</code>\n"
        f"💬 <b>Xabar:</b> {message.text}"
    )

    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(chat_id=admin_id, text=alert_text, parse_mode=ParseMode.HTML)
        except Exception as e:
            logging.error(f"Adminga yuborishda xatolik ({admin_id}): {e}")

    await message.answer("✅ Savolingiz Doktor Surayyo Vahobjonovnaga yuborildi. Tez orada javob beramiz!")

# ==========================================
# BOTNI ISHGA TUSHIRISH
# ==========================================
async def main():
    await bot.delete_webhook(drop_pending_updates=False)
    logging.info("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
