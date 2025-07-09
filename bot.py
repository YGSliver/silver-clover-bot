from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "7833691142:AAEe_Spa01bFMsjv7tH01qCNb0rIHsr7sCc"
ADMIN_CHAT_ID = 5765468417

print("✅ НОВАЯ ВЕРСИЯ БОТА ЗАПУЩЕНА!")

# Данные каталогов
rentals = [
    {
        "title": "Laguna Beach Resort 3 The Maldives",
        "photos": [
            "https://drive.google.com/uc?export=view&id=1u6KViZT0HVPvQM3Ywk0FXz9KtDzbhwIP",
            "https://drive.google.com/uc?export=view&id=1iK-GB4seFXF54UrTsvo4zxe378pxSGrT",
            "https://drive.google.com/uc?export=view&id=1iU2u3rspqAn2MAcRShaeYsgATPSFcZ60",
            "https://drive.google.com/uc?export=view&id=1OWJD8DP2hN0K7-fiHkUC8M1FgSG7LgEG",
            "https://drive.google.com/uc?export=view&id=1iiexHmk0hkyCQs-qYsDS8KmdJZz0kiIH"
        ],
        "description": """🏡 Аренда: квартира с 2 спальнями в Laguna Beach Resort 3 "The Maldives"
🌿 7 этаж | 68,5 кв.м | Балкон с видом на зелень и город

▪️ Удобная планировка и оборудованная кухня
▪️ Полностью меблирована и готова к проживанию
▪️ Курортная инфраструктура: лагунные бассейны, фитнес, охрана, парковка
📍 Рядом с пляжем Джомтьен

💰 25,000 бат/месяц
📩 За подробностями и просмотром — пишите нам!"""
    },
    # Добавь сюда остальные объекты аренды
]

sales = [
    {
        "title": "1 спальня, Copacabana Beach Jomtien",
        "photos": [
            "https://drive.google.com/uc?export=view&id=1XYTd635NLsZVy3tcIROypE8EZABSj1zN",
            "https://drive.google.com/uc?export=view&id=1Jr_DA7lVkkoA7xSNG59d7Q216MWhWVhC",
            "https://drive.google.com/uc?export=view&id=1NDcTpJ6zmxOUiUw6n_Wu4rh4d9c5tcmj",
            "https://drive.google.com/uc?export=view&id=1DGS0-jsiBaBuNRQLRtccRivbFtcNpBGk",
            "https://drive.google.com/uc?export=view&id=14OBUlf_mcQrmGQ3_pc8kiQSKqbOlQ7oO"
        ],
        "description": """🏝 Продаётся квартира в Copacabana Jomtien
🌇 41 этаж | Панорамный вид на море и город | Балкон с джакузи

📍 Престижный комплекс у пляжа Джомтьен — 50 м до моря
✅ 38 кв.м, иностранная собственность
💎 Современный дизайн, премиальные удобства
💰 8,500,000 бат | ~$260,000 | ~€230,000
📑 Оформление: 50/50

🔹 Бассейны с видами
🔹 SPA и фитнес
🔹 Рестораны, охрана, паркинг
🔹 Прямой выход к пляжу

📞 Готова к просмотрам — свяжитесь с нами!"""
    },
    # Добавь сюда остальные объекты продаж
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🏡 Аренда", callback_data="category_rent"),
            InlineKeyboardButton("🏷 Продажа", callback_data="category_sale")
        ]
    ]
    await update.message.reply_text("Добро пожаловать в каталог Silver Clover! Выберите категорию:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "category_rent":
        # Показываем листинг аренды
        keyboard = [[InlineKeyboardButton(item["title"], callback_data=f"rent_{i}")] for i, item in enumerate(rentals)]
        await query.edit_message_text("Выберите объект в категории Аренда:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "category_sale":
        # Показываем листинг продажи
        keyboard = [[InlineKeyboardButton(item["title"], callback_data=f"sale_{i}")] for i, item in enumerate(sales)]
        await query.edit_message_text("Выберите объект в категории Продажа:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("rent_") or data.startswith("sale_"):
        category, idx_str = data.split("_")
        idx = int(idx_str)
        item = rentals[idx] if category == "rent" else sales[idx]

        media = [InputMediaPhoto(media=url) for url in item["photos"]]
        # Отправляем фото группой
        await context.bot.send_media_group(chat_id=query.message.chat_id, media=media)
        # Отправляем описание
        await context.bot.send_message(chat_id=query.message.chat_id, text=item["description"])

    elif data == "apply_rent":
        context.user_data['category'] = 'аренду'
        await query.edit_message_text("Пожалуйста, отправьте ваше имя и номер телефона. Мы свяжемся с вами!")

    elif data == "apply_sale":
        context.user_data['category'] = 'продажу'
        await query.edit_message_text("Пожалуйста, отправьте ваше имя и номер телефона. Мы свяжемся с вами!")

async def collect_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = context.user_data.get('category', 'недвижимость')
    message = f"📬 Новая заявка на {category}:\n\n{update.message.text}"
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)
    await update.message.reply_text("Спасибо! Мы получили вашу заявку и скоро свяжемся с вами.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, collect_contact))

    print("🤖 Silver Clover Bot запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()