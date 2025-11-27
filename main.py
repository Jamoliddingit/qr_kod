import qrcode
import os
import asyncio
import threading
import time
import requests

from fastapi import FastAPI
import uvicorn
from fastapi.responses import JSONResponse

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile


# -------------------------
# 🔑 Bot token (ENVIRONMENT VARIABLEDAN OLINADI)
# -------------------------
# BOT_TOKEN ni kod ichida yozmang! Render / .env orqali o‘rnating.
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "BOT_TOKEN topilmadi! Iltimos, BOT_TOKEN environment variable sifatida o‘rnating."
    )

bot = Bot(token=TOKEN)
dp = Dispatcher()

# QR kodlar saqlanadigan papka
os.makedirs("qrcodes", exist_ok=True)


# -------------------------
# 🌐 FASTAPI SERVER
# -------------------------
app = FastAPI()


@app.get("/")
def index():
    return {"status": True, "alive": True}


@app.head("/")
def head_alive():
    return JSONResponse(content={"ok": True}, status_code=200)


@app.get("/ping")
def ping():
    return {"pong": True}


def start_web():
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))


# -------------------------
# 🤖 SELF-PING ROBOT (RENDER STOP BO‘LMASLIK UCHUN)
# -------------------------

def self_ping():
    url = os.getenv("RENDER_EXTERNAL_URL")  # Render env dan olinadi
    if not url:
        print("❗ RENDER_EXTERNAL_URL topilmadi! Self-ping ishlamaydi.")
        return

    while True:
        try:
            print(f"🔄 Self-ping → {url}")
            requests.get(url)
        except Exception as e:
            print(f"⚠️ Ping muammo, lekin bot davom etmoqda... ({e})")
        time.sleep(300)  # 5 minut = 300 sekund


def start_self_pinger():
    thread = threading.Thread(target=self_ping)
    thread.daemon = True
    thread.start()


# -------------------------
# 📥 DIRECT TELEGRAM URL FUNKSIYA
# -------------------------
async def get_direct_url(file_id):
    file = await bot.get_file(file_id)
    return f"https://api.telegram.org/file/bot{TOKEN}/{file.file_path}"


# -------------------------
# 🤖 BOT HANDLERLAR
# -------------------------

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "👋 Salom! QR yasashga tayyorman.\n"
        "Matn, rasm, fayl, video yuboring — men QR kod qilib beraman!"
    )


@dp.message(F.text)
async def text_qr(message: types.Message):
    path = f"qrcodes/{message.from_user.id}_text.png"
    qrcode.make(message.text).save(path)
    await message.reply_photo(FSInputFile(path), caption="📌 Matn QR tayyor!")
    os.remove(path)


@dp.message(F.photo)
async def photo_qr(message: types.Message):
    url = await get_direct_url(message.photo[-1].file_id)
    path = f"qrcodes/{message.from_user.id}_photo.png"
    qrcode.make(url).save(path)
    await message.reply_photo(
        FSInputFile(path),
        caption="📸 Rasm QR tayyor!\n👉 Skanerlasang rasm ochiladi."
    )
    os.remove(path)


@dp.message(F.document)
async def doc_qr(message: types.Message):
    url = await get_direct_url(message.document.file_id)
    path = f"qrcodes/{message.from_user.id}_file.png"
    qrcode.make(url).save(path)
    await message.reply_photo(
        FSInputFile(path),
        caption="📁 Fayl QR tayyor!\n👉 Skanerlasang faylni yuklaydi."
    )
    os.remove(path)


@dp.message(F.video)
async def video_qr(message: types.Message):
    url = await get_direct_url(message.video.file_id)
    path = f"qrcodes/{message.from_user.id}_video.png"
    qrcode.make(url).save(path)
    await message.reply_photo(
        FSInputFile(path),
        caption="🎥 Video QR tayyor!\n👉 Skanerlasang video ochiladi."
    )
    os.remove(path)


# -------------------------
# 🚀 MAIN START
# -------------------------
async def start_bot():
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Web server
    threading.Thread(target=start_web).start()

    # Render self-ping roboti
    start_self_pinger()

    # Aiogram bot
    asyncio.run(start_bot())
