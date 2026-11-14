import asyncio
import logging
import re
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode

# ==========================================
# SOZLAMALAR (YANGI BOT TOKEN VA ADMINLAR)
# ==========================================
BOT_TOKEN = "9081300362:AAFR05lSfO2a2Khi3zB8qSSYIFwlngQCXAc"
ADMIN_IDS = [6258110646, 7645769320]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ==========================================
# KLAVIATURALAR (ADMIN VA BEMORLAR UCHUN)
# ==========================================
admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📢 Barchaga Broadcast yuborish"),
            KeyboardButton(text="🧹 Chatni tozalash")
        ],
        [
            KeyboardButton(text="💡 Yordam & Qo'llanma"),
            KeyboardButton(text="👤 Bemor menyusini ko'rish")
        ]
    ],
    resize_keyboard=True,
    persistent=True
)

patient_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🩺 Xizmatlar va muolajalar"),
            KeyboardButton(text="📅 Qabulga yozilish")
        ],
        [
            KeyboardButton(text="💬 Shifokorga savol berish"),
            KeyboardButton(text="🌐 Rasmiy sayt va kanallar")
        ]
    ],
    resize_keyboard=True,
    persistent=True,
    input_field_placeholder="Savolingizni yozing yoki menyudan tanlang..."
)

links_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Rasmiy sayt (ginekologplastikxirurg.uz)", url="https://ginekologplastikxirurg.uz")],
        [InlineKeyboardButton(text="📢 Telegram kanalimiz", url="https://t.me/ginekologplastikx")],
        [InlineKeyboardButton(text="▶️ YouTube kanalimiz", url="https://youtube.com/@ginekologestetst")]
    ]
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
            "<b>@ginekolog_plastik_xirurg_bot</b> rasmiy boti ishga tushdi. "
            "Bemorlarning barcha savollari shu yerga keladi.\n\n"
            "🔒 <b>Xavfsizlik himoyasi yoqilgan:</b> Bemorlar rasm, video yoki fayl yubora olmaydi — faqat matn qabul qilinadi.",
            parse_mode=ParseMode.HTML,
            reply_markup=admin_keyboard
        )
    else:
        await message.answer(
            "🌸 <b>Assalomu alaykum!</b>\n\n"
            "<b>Ginekolog Plastik Xirurg — Doktor Surayyo Vahobjonovna</b> klinikasining rasmiy botiga xush kelibsiz!\n\n"
            "Pastdagi tugmalardan kerakli bo'limni tanlang yoki savolingizni shu yerga <b>faqat matn ko'rinishida</b> yozib qoldiring 👇",
            parse_mode=ParseMode.HTML,
            reply_markup=patient_keyboard
        )

# ==========================================
# QAT'IY MEDIA BLOKLASH (RASM, VIDEO, GIF, FAYL, STIKER)
# ==========================================
@dp.message(
    F.photo | F.video | F.animation | F.document |
    F.video_note | F.sticker | F.voice | F.audio
)
async def block_all_media(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        return

    try:
        await message.delete()
    except Exception:
        pass

    await message.answer(
        "🚫 <b>XAVFSIZLIK QOIDASI:</b>\n\n"
        "Botga har qanday rasm, video, GIF, stiker yoki fayl yuborish <b>qat'iyan taqiqlangan</b> va avtomatik o'chiriladi!\n\n"
        "✍️ Iltimos, muammo yoki savolingizni <b>faqat matn (so'z) ko'rinishida</b> yozib yuboring.",
        parse_mode=ParseMode.HTML,
        reply_markup=patient_keyboard
    )

# ==========================================
# BEMORLAR UCHUN TUGMA HANDLERLARI
# ==========================================
@dp.message(F.text == "🩺 Xizmatlar va muolajalar")
async def patient_services(message: types.Message):
    services_text = (
        "🩺 <b>ESTETIK GINEKOLOGIYA VA TIBBIY MUOLAJALAR:</b>\n\n"
        "1️⃣ <b>Labioplastika</b> — Kichik jinsiy lablar plastikasi (30–45 daqiqa)\n"
        "2️⃣ <b>Vaginoplastika</b> — Vagina devorlarini toraytirish\n"
        "3️⃣ <b>Klitoroplastika</b> — Estetik ko'rinish va sezgirlikni tiklash\n"
        "4️⃣ <b>Intim oqartirish</b> — Pigmentatsiyani lazer/piling bilan yo'qotish\n"
        "5️⃣ <b>Intim yoshartirish (PRP)</b> — Plazmoterapiya muolajasi\n"
        "6️⃣ <b>Bachadon bo'yni eroziyasini davolash</b> — Lazer va radioto'lqin usulida\n"
        "7️⃣ <b>Poliplarni olish</b> — Bachadon bo'yni va devori poliplari\n"
        "8️⃣ <b>Spiral o'rnatish (Implantsperal)</b> — Kontratseptiv vosita\n"
        "9️⃣ <b>Sistitni davolash</b> — Zamonaviy CO2 lazer yordamida og'riqsiz davolash\n"
        "🔟 <b>Bachadon miyomasi</b> — Tashxis va zamonaviy davolash\n"
        "1️⃣1️⃣ <b>Ajralmalar (Videlina)</b> — Mikroflorani tiklash va davolash\n"
        "1️⃣2️⃣ <b>Tug'ruqdan keyingi yirtilishlarni tiklash (Razriv)</b>\n\n"
        "ℹ️ Batafsil video ma'lumotlar uchun rasmiy saytimizga kiring yoki savolingizni shu yerga yozing!"
    )
    await message.answer(services_text, parse_mode=ParseMode.HTML, reply_markup=links_inline)

@dp.message(F.text == "📅 Qabulga yozilish")
async def patient_appointment(message: types.Message):
    await message.answer(
        "📅 <b>QABULGA YOZILISH VA ALOQA:</b>\n\n"
        "👩‍⚕️ <b>Shifokor:</b> Estetist ginekolog va plastik jarroh Surayyo Vahobjonovna\n"
        "📍 <b>Manzil:</b> Toshkent shahri\n"
        "📞 <b>Telefon / SMS:</b> <code>+998952775354</code>\n\n"
        "✍️ <i>Ism-familiyangiz, telefon raqamingiz va qaysi muolajaga kelmoqchi ekaningizni shu yerga matn qilib yozib qoldiring — o'zimiz bog'lanamiz!</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=patient_keyboard
    )

@dp.message(F.text == "💬 Shifokorga savol berish")
async def patient_ask_info(message: types.Message):
    await message.answer(
        "💬 <b>Shifokorga shaxsiy savol yuborish:</b>\n\n"
        "Savolingizni shu yerga oddiy xabar qilib yozing. Xabaringiz maxfiy tarzda to'g'ridan-to'g'ri "
        "<b>Doktor Surayyo Vahobjonovna</b>ga yuboriladi va tez orada shu chatning o'zida javob olasiz.\n\n"
        "🚫 <i>Eslatma: Rasm va video yuborish taqiqlangan — faqat matn yozing.</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=patient_keyboard
    )

@dp.message(F.text == "🌐 Rasmiy sayt va kanallar")
async def patient_links(message: types.Message):
    await message.answer(
        "🌐 <b>Bizning rasmiy sahifalarimiz:</b>\n\n"
        "Muolajalar haqida batafsil video sharhlar va foydali maslahatlar bilan tanishish uchun quyidagi tugmalarni bosing:",
        parse_mode=ParseMode.HTML,
        reply_markup=links_inline
    )

# ==========================================
# ADMIN TUGMALARI HANDLERLARI
# ==========================================
@dp.message(F.text == "👤 Bemor menyusini ko'rish")
async def admin_preview_patient_menu(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    await message.answer(
        "👀 Bemorlarga ko'rinadigan menyu tugmalari (Admin menyusiga qaytish uchun /start bosing):",
        reply_markup=patient_keyboard
    )

@dp.message(F.text == "📢 Barchaga Broadcast yuborish")
async def btn_broadcast(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    await message.answer(
        "📢 <b>Ommaviy Broadcast:</b>\n"
        "Har bir bemorga alohida javob berish uchun uning savoliga <b>Reply</b> qiling.",
        parse_mode=ParseMode.HTML,
        reply_markup=admin_keyboard
    )

@dp.message(F.text == "🧹 Chatni tozalash")
async def btn_clear_chat(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    await message.answer(
        "🧹 Telegram chatini tozalash uchun keraksiz xabarlarni belgilab, "
        "yuqoridagi <b>O'chirish (Delete)</b> tugmasini bosing.",
        parse_mode=ParseMode.HTML,
        reply_markup=admin_keyboard
    )

@dp.message(F.text == "💡 Yordam & Qo'llanma")
async def btn_help(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    await message.answer(
        "💡 <b>Shifokor uchun qo'llanma:</b>\n\n"
        "1️⃣ <b>Telegram botdan savol kelsa:</b> Xabarda <code>TG-ID: 123456789</code> bo'ladi. O'sha xabarga <b>Reply</b> qilsangiz, javob bemorning shaxsiy Telegramiga boradi.\n"
        "2️⃣ <b>Media himoyasi:</b> Bemorlar yuborgan barcha rasm, video va fayllar avtomatik o'chiriladi.",
        parse_mode=ParseMode.HTML,
        reply_markup=admin_keyboard
    )

# ==========================================
# SHIFOKOR JAVOBINI (REPLY) BEMORGA YUBORISH
# ==========================================
@dp.message(F.reply_to_message)
async def handle_doctor_reply(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    replied_text = message.reply_to_message.text or ""
    doctor_reply_text = message.text

    if not doctor_reply_text:
        await message.reply("⚠️ Iltimos, bemorga faqat matn ko'rinishida javob yozing.")
        return

    tg_match = re.search(r"TG-ID:\s*(\d+)", replied_text)
    if tg_match:
        target_user_id = int(tg_match.group(1))
        try:
            await bot.send_message(
                chat_id=target_user_id,
                text=(
                    f"👩‍⚕️ <b>Doktor Surayyo Vahobjonovna javobi:</b>\n\n"
                    f"{doctor_reply_text}\n\n"
                    f"📞 <i>Qo'shimcha savollar uchun: +998 95 277 53 54</i>"
                ),
                parse_mode=ParseMode.HTML,
                reply_markup=patient_keyboard
            )
            await message.reply("✅ Javobingiz bemorning Telegramiga yetkazildi!")
        except Exception as e:
            await message.reply(f"❌ Xatolik: Bemorga yuborib bo'lmadi ({e}).")
        return

# ==========================================
# FAQAT MATNLI SAVOLLARNI ADMINLARGA YUBORISH
# ==========================================
@dp.message(F.text)
async def forward_user_message(message: types.Message):
    user = message.from_user
    if user.id in ADMIN_IDS:
        return

    full_name = user.full_name or "Foydalanuvchi"
    username = f"@{user.username}" if user.username else "yo'q"

    alert_text = (
        f"📩 <b>TELEGRAM BOTDAN YANGI SAVOL</b>\n\n"
        f"👤 <b>Mijoz:</b> {full_name} ({username})\n"
        f"🆔 <b>TG-ID:</b> <code>{user.id}</code>\n"
        f"💬 <b>Savol:</b> {message.text}\n\n"
        f"👇 <i>Javob berish uchun ushbu xabarga Reply qiling.</i>"
    )

    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(chat_id=admin_id, text=alert_text, parse_mode=ParseMode.HTML)
        except Exception as e:
            logging.error(f"Adminga yuborishda xatolik ({admin_id}): {e}")

    await message.answer(
        "✅ <b>Savolingiz Doktor Surayyo Vahobjonovnaga yuborildi!</b>\n"
        "Shifokor ko'rib chiqib, tez orada shu chatga javob yozadi.",
        parse_mode=ParseMode.HTML,
        reply_markup=patient_keyboard
    )

# ==========================================
# BOTNI ISHGA TUSHIRISH
# ==========================================
async def main():
    await bot.delete_webhook(drop_pending_updates=False)
    logging.info("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
