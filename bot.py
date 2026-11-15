import re
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode

BOT_TOKEN = "9081300362:AAFR05lSfO2a2Khi3zB8qSSYIFwlngQCXAc"
ADMIN_IDS = [6258110646, 7645769320]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()

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
    persistent=True
)

links_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Rasmiy sayt (ginekologplastikxirurg.uz)", url="https://ginekologplastikxirurg.uz")],
        [InlineKeyboardButton(text="📢 Telegram kanalimiz", url="https://t.me/ginekologplastikx")],
        [InlineKeyboardButton(text="▶️ YouTube kanalimiz", url="https://youtube.com/@ginekologestetst")]
    ]
)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        await message.answer(
            "👩‍⚕️ <b>Assalomu alaykum, Doktor Surayyo Vahobjonovna!</b>\n\n"
            "Bot 24/7 faol ishlamoqda. Bemor savollariga <b>Reply</b> qilib javob bering.",
            parse_mode=ParseMode.HTML,
            reply_markup=admin_keyboard
        )
    else:
        await message.answer(
            "🌸 <b>Assalomu alaykum!</b>\n\n"
            "<b>Ginekolog Plastik Xirurg — Doktor Surayyo Vahobjonovna</b> klinikasining rasmiy botiga xush kelibsiz!\n\n"
            "Pastdagi tugmalardan tanlang yoki savolingizni matn ko'rinishida yozing 👇",
            parse_mode=ParseMode.HTML,
            reply_markup=patient_keyboard
        )

@dp.message(F.photo | F.video | F.animation | F.document | F.video_note | F.sticker | F.voice | F.audio)
async def block_all_media(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        return
    try:
        await message.delete()
    except Exception:
        pass
    await message.answer(
        "🚫 <b>XAVFSIZLIK QOIDASI:</b> Rasm, video va fayl yuborish taqiqlangan! Faqat matn yozing.",
        parse_mode=ParseMode.HTML,
        reply_markup=patient_keyboard
    )

@dp.message(F.text == "🩺 Xizmatlar va muolajalar")
async def patient_services(message: types.Message):
    await message.answer(
        "🩺 <b>ESTETIK GINEKOLOGIYA VA TIBBIY MUOLAJALAR:</b>\n\n"
        "1️⃣ Labioplastika\n2️⃣ Vaginoplastika\n3️⃣ Klitoroplastika\n4️⃣ Intim oqartirish\n"
        "5️⃣ Intim yoshartirish (PRP)\n6️⃣ Bachadon bo'yni eroziyasini davolash\n"
        "7️⃣ Poliplarni olish\n8️⃣ Spiral o'rnatish\n9️⃣ Sistitni CO2 lazer bilan davolash\n"
        "🔟 Bachadon miyomasi\n1️⃣1️⃣ Ajralmalar davolash\n1️⃣2️⃣ Tug'ruqdan keyingi yirtilishlarni tiklash",
        parse_mode=ParseMode.HTML,
        reply_markup=links_inline
    )

@dp.message(F.text == "📅 Qabulga yozilish")
async def patient_appointment(message: types.Message):
    await message.answer(
        "📅 <b>QABULGA YOZILISH:</b>\n\n"
        "👩‍⚕️ Doktor Surayyo Vahobjonovna\n📍 Toshkent shahri\n📞 Tel: <code>+998952775354</code>\n\n"
        "✍️ Ismingiz va telefon raqamingizni shu yerga yozib qoldiring — o'zimiz bog'lanamiz!",
        parse_mode=ParseMode.HTML,
        reply_markup=patient_keyboard
    )

@dp.message(F.text == "💬 Shifokorga savol berish")
async def patient_ask_info(message: types.Message):
    await message.answer(
        "💬 Savolingizni shu yerga oddiy matn qilib yozing — Doktor Surayyo Vahobjonovna tez orada javob beradilar.",
        reply_markup=patient_keyboard
    )

@dp.message(F.text == "🌐 Rasmiy sayt va kanallar")
async def patient_links(message: types.Message):
    await message.answer("🌐 Rasmiy sahifalarimiz:", reply_markup=links_inline)

@dp.message(F.text == "👤 Bemor menyusini ko'rish")
async def admin_preview(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        await message.answer("👀 Bemor tugmalari (qaytish uchun /start bosing):", reply_markup=patient_keyboard)

@dp.message(F.text == "💡 Yordam & Qo'llanma")
async def btn_help(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        await message.answer("💡 Bemor savoliga <b>Reply</b> qilib javob yozing — darhol bemorga boradi.", parse_mode=ParseMode.HTML)

@dp.message(F.reply_to_message)
async def handle_doctor_reply(message: types.Message):
    if message.from_user.id not in ADMIN_IDS or not message.text:
        return
    replied_text = message.reply_to_message.text or ""
    tg_match = re.search(r"TG-ID:\s*(\d+)", replied_text)
    if tg_match:
        target_id = int(tg_match.group(1))
        await bot.send_message(
            chat_id=target_id,
            text=f"👩‍⚕️ <b>Doktor Surayyo Vahobjonovna javobi:</b>\n\n{message.text}",
            parse_mode=ParseMode.HTML,
            reply_markup=patient_keyboard
        )
        await message.reply("✅ Javob bemorga yuborildi!")

@dp.message(F.text)
async def forward_user_message(message: types.Message):
    user = message.from_user
    if user.id in ADMIN_IDS:
        return
    alert_text = (
        f"📩 <b>YANGI BEMOR SAVOLI</b>\n\n"
        f"👤 <b>Mijoz:</b> {user.full_name}\n"
        f"🆔 <b>TG-ID:</b> <code>{user.id}</code>\n"
        f"💬 <b>Savol:</b> {message.text}"
    )
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(chat_id=admin_id, text=alert_text, parse_mode=ParseMode.HTML)
        except Exception:
            pass
    await message.answer(
        "✅ Savolingiz Doktor Surayyo Vahobjonovnaga yuborildi! Tez orada javob olasiz.",
        reply_markup=patient_keyboard
    )

@app.post("/api/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return {"ok": True}

@app.get("/")
async def home():
    return {"status": "Bot 24/7 ishlamoqda"}
