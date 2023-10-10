from uuid import uuid4
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, WebAppInfo, \
    InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultPhoto, InputMessageContent
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from command_text import *
from utils import *

ZK_STATE, GG_STATE = "category: Золотое кольцо", "category: Города-герои"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.args)
    if len(context.args):
        print(context.args)
        city = (await City.get_cities_by_name(context.args[0]))[0]
        await update.message.reply_text(text=f'Что я нашел по городу "{city.name}"', reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="🔍Посмотреть", web_app=WebAppInfo(url=city.url))]]))
    else:
        keyboard = [
            [InlineKeyboardButton(text="🔎 Гид", callback_data=ZK_STATE)],
            # [InlineKeyboardButton(text="Города-герои", callback_data=GG_STATE)],
            [InlineKeyboardButton(text="🗺 Карта",
                                  web_app=WebAppInfo(url="https://rus-tour-bot-web-app.vercel.app/?full=1"))]
        ]
        await update.message.reply_text(START, parse_mode=ParseMode.MARKDOWN,
                                        reply_markup=InlineKeyboardMarkup(keyboard))


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=HELP, parse_mode="Markdown")


async def city_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    cities, answer_text = (cities_gg, GG_VIEW) if query.data == GG_STATE else (cities_zk, ZK_VIEW)

    keyboard = [list() for i in range(len(cities) // 2 + len(cities) % 2)]

    i = 0
    for city in cities:
        keyboard[i // 2].append(InlineKeyboardButton(text=city.name, web_app=WebAppInfo(url=city.url)))
        i += 1

    await update.get_bot().sendMessage(chat_id=update.effective_user.id, text=answer_text,
                                       parse_mode=ParseMode.MARKDOWN,
                                       reply_markup=InlineKeyboardMarkup(keyboard))


async def routes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=ROUTES, parse_mode="Markdown")


async def tours(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=TOURS, parse_mode="Markdown")


async def means_of_transport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=MEANS_OF_TRANSPORT, parse_mode="Markdown")


async def advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=ADVICE, parse_mode="Markdown")


async def sources(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=SOURCES, parse_mode="Markdown")


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query

    results = list()
    for city in await City.get_cities_by_name(name=query):
        results.append(InlineQueryResultArticle(
            id=str(uuid4()),
            thumbnail_url=city.image_url,
            title=city.name,
            url=city.image_url,
            hide_url=True,
            input_message_content=InputTextMessageContent(
                f"Туристические объекты города {city.name}. В нашем боте @russian_tourist_bot"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text=f"{city.name}",
                                                                     url=f't.me/russian_tourist_bot?start={city.name}')]])
        ))

    print(results)
    await update.inline_query.answer(results=results)
