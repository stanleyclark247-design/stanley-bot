import os
import random
import yt_dlp
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8423324489:AAGpBdyxPz3Qm-4VAhaqwnhO7wD3lw1r9sM"
OWNER = "stanley"
START_TIME = datetime.now()

# ─── START ───
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now()
    user = update.effective_user.first_name
    text = f"""
╭━━━━━━━━━━━━━━━━━━⬡
┃ 𝗦𝗧𝗔𝗡𝗟𝗘𝗬 𝗠𝗗  
┃__________________________
┃ 💎 ᴏᴡɴᴇʀ : {OWNER}
┃ 🗓️ ᴅᴀᴛᴇ : {now.strftime("%d/%m/%Y")}
┃ ⏰ ᴛɪᴍᴇ : {now.strftime("%H:%M:%S")}
┃ 🔅 ᴅᴀʏ : {now.strftime("%A")}
╰━━━━━━━━━━━━━━━━━━⬡
╔━━━━━━━━━━━━━━━━━━❒
║ ⦿ 𝗦𝗧𝗔𝗧𝗨𝗦 : ONLINE 🟢
║ ⦿ 𝗨𝗦𝗘𝗥 : {user}
╚━━━━━━━━━━━━━━━━━━❒

Hi {user}! Type /help to see all commands 🎉
"""
    await update.message.reply_text(text)

# ─── HELP ───
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
┌─〔 Owner Commands 〕
┃─❐ /start - Start bot
┃─❐ /alive - Bot status
┃─❐ /ping - Test speed
┃─❐ /uptime - Bot uptime
┃─❐ /owner - Owner info
└──────────────────────

┌─〔 Music 🎵 〕
┃─❐ /music <song name> - Download music
┃─❐ /play <YouTube link> - Play by link
└──────────────────────

┌─〔 Fun & Games 🎮 〕
┃─❐ /dice - Roll a dice
┃─❐ /coin - Flip a coin
┃─❐ /joke - Random joke
┃─❐ /quote - Random quote
┃─❐ /dadjoke - Dad joke
┃─❐ /funfact - Fun fact
┃─❐ /advice - Random advice
┃─❐ /truth - Truth question
┃─❐ /dare - Dare challenge
┃─❐ /8ball - Magic 8 ball
┃─❐ /roast - Get roasted
┃─❐ /compliment - Compliment
└──────────────────────

┌─〔 Tools 🛠️ 〕
┃─❐ /time - Current time
┃─❐ /calc <math> - Calculator
┃─❐ /wiki <topic> - Wikipedia
┃─❐ /weather <city> - Weather
└──────────────────────
"""
    await update.message.reply_text(text)

# ─── OWNER COMMANDS ───
async def alive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟢 Stanley Bot is ONLINE and running!")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong! Bot is active!")

async def owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👑 Owner: {OWNER}\n💬 Stanley Bot made with ❤️")

async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    delta = datetime.now() - START_TIME
    hours, rem = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(rem, 60)
    await update.message.reply_text(f"⏱️ Uptime: {hours}h {minutes}m {seconds}s")

# ─── MUSIC COMMANDS ───
async def download_and_send(update, query, is_url=False):
    msg = await update.message.reply_text(f"🎵 {'Fetching' if is_url else 'Searching'}... please wait!")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'music.%(ext)s',
            'quiet': True,
            'noplaylist': True,
            'default_search': 'ytsearch1' if not is_url else None,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            if 'entries' in info:
                info = info['entries'][0]
            title = info['title']
            duration = info.get('duration', 0)

        await msg.edit_text(f"🎶 Sending: *{title}*", parse_mode="Markdown")

        with open("music.mp3", "rb") as audio:
            await update.message.reply_audio(
                audio=audio,
                title=title,
                performer="Stanley Bot 🎵",
                caption=f"🎵 *{title}*\n⏱️ {duration//60}:{duration%60:02d}\n\n🤖 Stanley Bot",
                parse_mode="Markdown"
            )

        os.remove("music.mp3")
        await msg.delete()

    except Exception as e:
        await msg.edit_text("❌ Failed! Try a different song name or link.")

async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /music <song name>\nExample: /music Shape of You")
        return
    query = ' '.join(context.args)
    await download_and_send(update, query, is_url=False)

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /play <YouTube link>\nExample: /play https://youtube.com/watch?v=xxx")
        return
    url = context.args[0]
    await download_and_send(update, url, is_url=True)

# ─── FUN & GAMES ───
async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🎲 You rolled: *{random.randint(1, 6)}*", parse_mode="Markdown")

async def coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🪙 *{random.choice(['Heads', 'Tails'])}*", parse_mode="Markdown")

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything! 😄",
        "I told my wife she was drawing her eyebrows too high. She looked surprised. 😂",
        "Why can't you give Elsa a balloon? Because she'll let it go! ❄️",
        "I'm reading a book about anti-gravity. It's impossible to put down! 📚",
        "What do you call a fake noodle? An impasta! 🍝",
    ]
    await update.message.reply_text(random.choice(jokes))

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quotes = [
        "💬 'The best way to predict the future is to create it.' – Lincoln",
        "💬 'In the middle of difficulty lies opportunity.' – Einstein",
        "💬 'It does not matter how slowly you go, as long as you do not stop.' – Confucius",
        "💬 'Believe you can and you're halfway there.' – Roosevelt",
    ]
    await update.message.reply_text(random.choice(quotes))

async def dadjoke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jokes = [
        "I used to hate facial hair... but then it grew on me. 😅",
        "What do you call cheese that isn't yours? Nacho cheese! 🧀",
        "Why did the scarecrow win an award? He was outstanding in his field! 🌾",
        "I only know 25 letters of the alphabet. I don't know y. 😂",
    ]
    await update.message.reply_text(random.choice(jokes))

async def funfact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    facts = [
        "🤓 Honey never spoils. 3000-year-old honey was found in Egyptian tombs!",
        "🤓 A group of flamingos is called a 'flamboyance'.",
        "🤓 Octopuses have three hearts and blue blood!",
        "🤓 The Eiffel Tower grows 6 inches taller in summer due to heat!",
        "🤓 Bananas are berries but strawberries are not! 🍌",
    ]
    await update.message.reply_text(random.choice(facts))

async def advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    advices = [
        "💡 Don't compare your chapter 1 to someone else's chapter 20.",
        "💡 Work hard in silence, let success make the noise.",
        "💡 Be yourself; everyone else is already taken.",
        "💡 Small steps every day lead to big results.",
    ]
    await update.message.reply_text(random.choice(advices))

async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    truths = [
        "🙋 What is your biggest fear?",
        "🙋 Have you ever lied to your best friend?",
        "🙋 What's the most embarrassing thing you've done?",
        "🙋 Who was your first crush?",
    ]
    await update.message.reply_text(random.choice(truths))

async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dares = [
        "🎯 Send a voice note singing your favorite song!",
        "🎯 Change your profile picture to a funny face for 1 hour!",
        "🎯 Text someone 'I love you' without explanation!",
        "🎯 Do 10 pushups right now!",
    ]
    await update.message.reply_text(random.choice(dares))

async def eightball(update: Update, context: ContextTypes.DEFAULT_TYPE):
    responses = [
        "🎱 It is certain!", "🎱 Without a doubt!", "🎱 Yes, definitely!",
        "🎱 Don't count on it.", "🎱 My sources say no.", "🎱 Very doubtful.",
        "🎱 Reply hazy, try again.", "🎱 Ask again later.",
    ]
    await update.message.reply_text(random.choice(responses))

async def roast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    roasts = [
        "🔥 You're the reason they put instructions on shampoo bottles.",
        "🔥 I'd agree with you but then we'd both be wrong.",
        "🔥 You have something on your chin... no, the third one.",
    ]
    await update.message.reply_text(random.choice(roasts))

async def compliment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    compliments = [
        "💐 You light up every room you walk into!",
        "💐 You have an amazing sense of humor!",
        "💐 You're more fun than bubble wrap!",
        "💐 You're a great human being. Keep it up! 🌟",
    ]
    await update.message.reply_text(random.choice(compliments))

# ─── TOOLS ───
async def time_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now()
    await update.message.reply_text(f"🕐 Time: {now.strftime('%H:%M:%S')}\n📅 Date: {now.strftime('%d/%m/%Y')}\n🔅 Day: {now.strftime('%A')}")

async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        expression = ' '.join(context.args)
        result = eval(expression)
        await update.message.reply_text(f"🧮 {expression} = *{result}*", parse_mode="Markdown")
    except:
        await update.message.reply_text("❌ Usage: /calc 5 + 3")

async def wiki(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join(context.args)
    if query:
        await update.message.reply_text(f"🔍 Wikipedia: https://en.wikipedia.org/wiki/{query.replace(' ', '_')}")
    else:
        await update.message.reply_text("❌ Usage: /wiki python")

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = ' '.join(context.args)
    if city:
        await update.message.reply_text(f"🌤️ Weather for *{city}* coming soon!\nGet a free API key at openweathermap.org to enable this.", parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Usage: /weather Lagos")

# ─── RUN BOT ───
app = ApplicationBuilder().token(BOT_TOKEN).build()

handlers = [
    ("start", start), ("help", help_command),
    ("alive", alive), ("ping", ping), ("owner", owner), ("uptime", uptime),
    ("music", music), ("play", play),
    ("dice", dice), ("coin", coin), ("joke", joke), ("quote", quote),
    ("dadjoke", dadjoke), ("funfact", funfact), ("advice", advice),
    ("truth", truth), ("dare", dare), ("8ball", eightball),
    ("roast", roast), ("compliment", compliment),
    ("time", time_cmd), ("calc", calc), ("wiki", wiki), ("weather", weather),
]

for name, func in handlers:
    app.add_handler(CommandHandler(name, func))

print("✅ Stanley Bot is running...")
app.run_polling()
