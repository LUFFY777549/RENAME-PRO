from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from helper.progress import progress_for_pyrogram
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.database import find
from PIL import Image
import os, time

# Temporary dict to store filenames per user
user_filename = {}

# ForceReply handler
@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    if message.reply_to_message.reply_markup and isinstance(message.reply_to_message.reply_markup, ForceReply):
        user_id = message.chat.id
        new_name = message.text
        user_filename[user_id] = new_name  # store filename
        await message.delete()

        media = await client.get_messages(message.chat.id, message.reply_to_message.id)
        file = media.reply_to_message.document or media.reply_to_message.video or media.reply_to_message.audio
        filename = file.file_name
        types = file.mime_type.split("/")
        mime = types[0]

        mg_id = media.reply_to_message.id

        # buttons
        if mime == "video":
            markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("📁 Documents", callback_data="doc"),
                 InlineKeyboardButton("🎥 Video", callback_data="vid")]
            ])
        elif mime == "audio":
            markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("📁 Documents", callback_data="doc"),
                 InlineKeyboardButton("🎵 audio", callback_data="aud")]
            ])
        else:
            markup = InlineKeyboardMarkup([[InlineKeyboardButton("📁 Documents", callback_data="doc")]])

        await message.reply_text(
            f"**Select the output file type**\n**Output FileName** :- ```{new_name}```",
            reply_to_message_id=mg_id,
            reply_markup=markup
        )

# Callback query handlers
async def process_file(bot, update, file_type):
    user_id = update.from_user.id
    if user_id not in user_filename:
        return await update.message.answer("❌ File name missing. Retry rename!")

    new_filename = user_filename[user_id]
    del user_filename[user_id]  # remove after use

    file_path = f"downloads/{new_filename}"
    file = update.message.reply_to_message
    ms = await update.message.edit("``` Trying To Download...```")

    try:
        path = await bot.download_media(file, progress=progress_for_pyrogram,
                                        progress_args=("``` Trying To Download...```", ms, time.time()))
    except Exception as e:
        return await ms.edit(str(e))

    old = path.split("/downloads/")[1]
    os.rename(f"downloads/{old}", file_path)

    duration = 0
    if file_type in ["vid", "aud"]:
        meta = extractMetadata(createParser(file_path))
        if meta and meta.has("duration"): duration = meta.get("duration").seconds

    thumb = find(user_id)

    if thumb:
        ph = await bot.download_media(thumb)
        Image.open(ph).convert("RGB").save(ph)
        Image.open(ph).resize((320, 320)).save(ph, "JPEG")

    await ms.edit("```Trying To Uploading```")

    try:
        if file_type == "doc":
            await bot.send_document(user_id, document=file_path, thumb=ph if thumb else None,
                                    caption=f"**{new_filename}**",
                                    progress=progress_for_pyrogram,
                                    progress_args=("```Trying To Uploading```", ms, time.time()))
        elif file_type == "vid":
            await bot.send_video(user_id, video=file_path, thumb=ph if thumb else None,
                                 caption=f"**{new_filename}**", duration=duration,
                                 progress=progress_for_pyrogram,
                                 progress_args=("```Trying To Uploading```", ms, time.time()))
        elif file_type == "aud":
            await bot.send_audio(user_id, audio=file_path, thumb=ph if thumb else None,
                                 caption=f"**{new_filename}**", duration=duration,
                                 progress=progress_for_pyrogram,
                                 progress_args=("```Trying To Uploading```", ms, time.time()))
        await ms.delete()
        os.remove(file_path)
        if thumb:
            os.remove(ph)
    except Exception as e:
        await ms.edit(str(e))
        os.remove(file_path)
        if thumb:
            os.remove(ph)

# Map callback queries
@Client.on_callback_query(filters.regex("doc"))
async def doc(bot, update):
    await process_file(bot, update, "doc")

@Client.on_callback_query(filters.regex("vid"))
async def vid(bot, update):
    await process_file(bot, update, "vid")

@Client.on_callback_query(filters.regex("aud"))
async def aud(bot, update):
    await process_file(bot, update, "aud")