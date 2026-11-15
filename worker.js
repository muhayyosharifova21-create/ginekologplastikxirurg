const BOT_TOKEN = "9081300362:AAFR05lSfO2a2Khi3zB8qSSYIFwlngQCXAc";
const ADMIN_IDS = [9081300362];
const TG_API = `https://api.telegram.org/bot${BOT_TOKEN}`;

const adminKeyboard = {
  keyboard: [
    [{ text: "📢 Barchaga Broadcast yuborish" }, { text: "🧹 Chatni tozalash" }],
    [{ text: "💡 Yordam & Qo'llanma" }, { text: "👤 Bemor menyusini ko'rish" }]
  ],
  resize_keyboard: true,
  is_persistent: true
};

const patientKeyboard = {
  keyboard: [
    [{ text: "🩺 Xizmatlar va muolajalar" }, { text: "📅 Qabulga yozilish" }],
    [{ text: "💬 Shifokorga savol berish" }, { text: "🌐 Rasmiy sayt va kanallar" }]
  ],
  resize_keyboard: true,
  is_persistent: true
};

// Xabar tagida doim ko'rinib turadigan katta tugmalar
const patientInlineMenu = {
  inline_keyboard: [
    [
      { text: "🩺 Xizmatlar va muolajalar", callback_data: "services" },
      { text: "📅 Qabulga yozilish", callback_data: "appointment" }
    ],
    [
      { text: "💬 Shifokorga savol berish", callback_data: "ask_doctor" }
    ],
    [
      { text: "🌐 Rasmiy sayt (ginekologplastikxirurg.uz)", url: "https://ginekologplastikxirurg.uz" }
    ],
    [
      { text: "📢 Telegram kanal", url: "https://t.me/ginekologplastikx" },
      { text: "▶️ YouTube kanal", url: "https://youtube.com/@ginekologestetst" }
    ]
  ]
};

async function callTg(method, payload) {
  return fetch(`${TG_API}/${method}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}

export default {
  async fetch(request) {
    if (request.method !== "POST") {
      return new Response("Ginekolog Plastik Xirurg Bot 24/7 faol!", { status: 200 });
    }

    const update = await request.json();

    // Xabar tagidagi Inline tugmalar bosilganda
    if (update.callback_query) {
      const cb = update.callback_query;
      const chatId = cb.message.chat.id;
      const data = cb.data;

      await callTg("answerCallbackQuery", { callback_query_id: cb.id });

      if (data === "services") {
        await callTg("sendMessage", {
          chat_id: chatId,
          text: "🩺 <b>ESTETIK GINEKOLOGIYA VA TIBBIY MUOLAJALAR:</b>\n\n1️⃣ Labioplastika\n2️⃣ Vaginoplastika\n3️⃣ Klitoroplastika\n4️⃣ Intim oqartirish\n5️⃣ Intim yoshartirish (PRP)\n6️⃣ Bachadon bo'yni eroziyasini davolash\n7️⃣ Poliplarni olish\n8️⃣ Spiral o'rnatish\n9️⃣ Sistitni CO2 lazer bilan davolash\n🔟 Bachadon miyomasi\n1️⃣1️⃣ Ajralmalar davolash\n1️⃣2️⃣ Tug'ruqdan keyingi yirtilishlarni tiklash",
          parse_mode: "HTML",
          reply_markup: patientInlineMenu
        });
      } else if (data === "appointment") {
        await callTg("sendMessage", {
          chat_id: chatId,
          text: "📅 <b>QABULGA YOZILISH:</b>\n\n👩‍⚕️ Doktor Surayyo Vahobjonovna\n📍 Toshkent shahri\n📞 Tel: <code>+998952775354</code>\n\n✍️ Ismingiz va telefon raqamingizni shu yerga yozib qoldiring — o'zimiz bog'lanamiz!",
          parse_mode: "HTML",
          reply_markup: patientKeyboard
        });
      } else if (data === "ask_doctor") {
        await callTg("sendMessage", {
          chat_id: chatId,
          text: "💬 Savolingizni shu yerga oddiy matn qilib yozing — Doktor Surayyo Vahobjonovna tez orada javob beradilar.\n\n🚫 <i>Eslatma: Rasm va video yuborish taqiqlangan.</i>",
          parse_mode: "HTML",
          reply_markup: patientKeyboard
        });
      }
      return new Response("OK");
    }

    const msg = update.message;
    if (!msg) return new Response("OK");

    const chatId = msg.chat.id;
    const isAdmin = ADMIN_IDS.includes(chatId);

    // 1. Bemor rasm/video/fayl yuborsa — darhol o'chirish
    if (!isAdmin && (msg.photo || msg.video || msg.animation || msg.document || msg.video_note || msg.sticker || msg.voice || msg.audio)) {
      await callTg("deleteMessage", { chat_id: chatId, message_id: msg.message_id });
      await callTg("sendMessage", {
        chat_id: chatId,
        text: "🚫 <b>XAVFSIZLIK QOIDASI:</b>\n\nBotga rasm, video, GIF yoki fayl yuborish <b>qat'iyan taqiqlangan</b>! Iltimos, savolingizni faqat matn ko'rinishida yozing.",
        parse_mode: "HTML",
        reply_markup: patientInlineMenu
      });
      return new Response("OK");
    }

    const text = msg.text || "";

    // 2. /start buyrug'i
    if (text === "/start") {
      if (isAdmin) {
        await callTg("sendMessage", {
          chat_id: chatId,
          text: "👩‍⚕️ <b>Assalomu alaykum, Doktor Surayyo Vahobjonovna!</b>\n\nBot Cloudflare'da 24/7 ishga tushdi. Bemor savollariga <b>Reply</b> qilib javob bering.",
          parse_mode: "HTML",
          reply_markup: adminKeyboard
        });
      } else {
        // Pastki klaviaturani ham, xabar ostidagi katta tugmalarni ham chiqarish
        await callTg("sendMessage", {
          chat_id: chatId,
          text: "🌸 <b>Assalomu alaykum!</b>\n\n<b>Ginekolog Plastik Xirurg — Doktor Surayyo Vahobjonovna</b> klinikasining rasmiy botiga xush kelibsiz!",
          parse_mode: "HTML",
          reply_markup: patientKeyboard
        });
        await callTg("sendMessage", {
          chat_id: chatId,
          text: "👇 Kerakli bo'limni tanlang yoki savolingizni shu yerga matn ko'rinishida yozing:",
          reply_markup: patientInlineMenu
        });
      }
      return new Response("OK");
    }

    // 3. Pastki menyu tugmalari bosilganda
    if (text === "🩺 Xizmatlar va muolajalar") {
      await callTg("sendMessage", {
        chat_id: chatId,
        text: "🩺 <b>ESTETIK GINEKOLOGIYA VA TIBBIY MUOLAJALAR:</b>\n\n1️⃣ Labioplastika\n2️⃣ Vaginoplastika\n3️⃣ Klitoroplastika\n4️⃣ Intim oqartirish\n5️⃣ Intim yoshartirish (PRP)\n6️⃣ Bachadon bo'yni eroziyasini davolash\n7️⃣ Poliplarni olish\n8️⃣ Spiral o'rnatish\n9️⃣ Sistitni CO2 lazer bilan davolash\n🔟 Bachadon miyomasi\n1️⃣1️⃣ Ajralmalar davolash\n1️⃣2️⃣ Tug'ruqdan keyingi yirtilishlarni tiklash",
        parse_mode: "HTML",
        reply_markup: patientInlineMenu
      });
      return new Response("OK");
    }

    if (text === "📅 Qabulga yozilish") {
      await callTg("sendMessage", {
        chat_id: chatId,
        text: "📅 <b>QABULGA YOZILISH:</b>\n\n👩‍⚕️ Doktor Surayyo Vahobjonovna\n📍 Toshkent shahri\n📞 Tel: <code>+998952775354</code>\n\n✍️ Ismingiz va telefon raqamingizni shu yerga yozib qoldiring — o'zimiz bog'lanamiz!",
        parse_mode: "HTML",
        reply_markup: patientKeyboard
      });
      return new Response("OK");
    }

    if (text === "💬 Shifokorga savol berish") {
      await callTg("sendMessage", {
        chat_id: chatId,
        text: "💬 Savolingizni shu yerga oddiy matn qilib yozing — Doktor Surayyo Vahobjonovna tez orada javob beradilar.",
        reply_markup: patientKeyboard
      });
      return new Response("OK");
    }

    if (text === "🌐 Rasmiy sayt va kanallar") {
      await callTg("sendMessage", {
        chat_id: chatId,
        text: "🌐 Bizning rasmiy sahifalarimiz:",
        reply_markup: patientInlineMenu
      });
      return new Response("OK");
    }

    // 4. Admin tugmalari
    if (isAdmin && text === "👤 Bemor menyusini ko'rish") {
      await callTg("sendMessage", {
        chat_id: chatId,
        text: "👀 Bemorlarga ko'rinadigan tugmalar (Admin menyusiga qaytish uchun /start bosing):",
        reply_markup: patientInlineMenu
      });
      return new Response("OK");
    }

    if (isAdmin && text === "💡 Yordam & Qo'llanma") {
      await callTg("sendMessage", {
        chat_id: chatId,
        text: "💡 Bemorga javob berish uchun uning savoliga <b>Reply</b> qiling — javob darhol bemorga boradi.",
        parse_mode: "HTML",
        reply_markup: adminKeyboard
      });
      return new Response("OK");
    }

    // 5. Shifokor Reply qilganda bemorga javob yuborish
    if (isAdmin && msg.reply_to_message && text) {
      const orig = msg.reply_to_message.text || "";
      const match = orig.match(/TG-ID:\s*(\d+)/);
      if (match) {
        await callTg("sendMessage", {
          chat_id: Number(match[1]),
          text: `👩‍⚕️ <b>Doktor Surayyo Vahobjonovna javobi:</b>\n\n${text}\n\n📞 <i>Aloqa: +998 95 277 53 54</i>`,
          parse_mode: "HTML",
          reply_markup: patientInlineMenu
        });
        await callTg("sendMessage", {
          chat_id: chatId,
          text: "✅ Javobingiz bemorga yetkazildi!",
          reply_to_message_id: msg.message_id
        });
      }
      return new Response("OK");
    }

    // 6. Bemor yozgan savolni adminga yuborish
    if (!isAdmin && text) {
      const fullName = `${msg.from.first_name || ""} ${msg.from.last_name || ""}`.trim();
      const username = msg.from.username ? `@${msg.from.username}` : "yo'q";
      const alertText = `📩 <b>YANGI BEMOR SAVOLI</b>\n\n👤 <b>Mijoz:</b> ${fullName} (${username})\n🆔 <b>TG-ID:</b> <code>${chatId}</code>\n💬 <b>Savol:</b> ${text}\n\n👇 <i>Javob berish uchun Reply qiling.</i>`;

      for (const adminId of ADMIN_IDS) {
        await callTg("sendMessage", {
          chat_id: adminId,
          text: alertText,
          parse_mode: "HTML"
        });
      }

      await callTg("sendMessage", {
        chat_id: chatId,
        text: "✅ <b>Savolingiz Doktor Surayyo Vahobjonovnaga yuborildi!</b>\nTez orada shu chatga javob yozamiz.",
        parse_mode: "HTML",
        reply_markup: patientInlineMenu
      });
    }

    return new Response("OK");
  }
};
