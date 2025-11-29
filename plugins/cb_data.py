from helper.progress import progress_for_pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.database import find
import os
from PIL import Image
import time

@Client.on_callback_query(filters.regex('cancel'))
async def cancel(bot, update):
    try:
        await update.message.delete()
    except:
        pass

@Client.on_callback_query(filters.regex('rename'))
async def rename(bot, update):
    await update.message.delete()
    await update.message.reply_text(
        "__Please enter the new filename...__",
        reply_to_message_id=update.message.reply_to_message.id,
        reply_markup=ForceReply(True)
    )


### ========== DOCUMENT ==============
@Client.on_callback_query(filters.regex("doc"))
async def doc(bot, update):

    new_name = update.message.reply_to_message.text  # FIX
    if new_name is None:
        return await update.message.reply("❌ File name not found. Please rename again.")

    name = new_name.split(":-") if ":-" in new_name else [None, new_name]
    new_filename = name[1]
    file_path = f"downloads/{new_filename}"
    file = update.message.reply_to_message

    ms = await update.message.edit("``` Trying To Download...```")

    try:
        path = await bot.download_media(message=file,progress=progress_for_pyrogram,
            progress_args=("``` Trying To Download...```", ms, time.time()))
    except Exception as e:
        return await ms.edit(str(e))

    old = path.split("/downloads/")[1]
    os.rename(f"downloads/{old}",file_path)

    user_id = update.message.chat.id
    thumb = find(user_id)

    if thumb:
        ph = await bot.download_media(thumb)
        Image.open(ph).convert("RGB").save(ph)
        Image.open(ph).resize((320,320)).save(ph,"JPEG")

        await ms.edit("```Trying To Uploading```")
        try:
            await bot.send_document(user_id,document=file_path,thumb=ph,
                caption=f"**{new_filename}**",progress=progress_for_pyrogram,
                progress_args=("```Trying To Uploading```",ms,time.time()))
            await ms.delete()
            os.remove(file_path); os.remove(ph)
        except Exception as e:
            await ms.edit(str(e)); os.remove(file_path); os.remove(ph)

    else:
        await ms.edit("```Trying To Uploading```")
        try:
            await bot.send_document(user_id,document=file_path,caption=f"**{new_filename}**",
                progress=progress_for_pyrogram,progress_args=("```Trying To Uploading```",ms,time.time()))
            await ms.delete(); os.remove(file_path)
        except Exception as e:
            await ms.edit(str(e)); os.remove(file_path)



### ========== VIDEO ==============
@Client.on_callback_query(filters.regex("vid"))
async def vid(bot,update):

    new_name = update.message.reply_to_message.text  # FIX
    if new_name is None:
        return await update.message.reply("❌ File name missing. Retry rename!")

    name = new_name.split(":-") if ":-" in new_name else [None,new_name]
    new_filename = name[1]
    file_path = f"downloads/{new_filename}"
    file = update.message.reply_to_message

    ms = await update.message.edit("``` Trying To Download...```")

    try:
        path = await bot.download_media(message=file,progress=progress_for_pyrogram,
            progress_args=("``` Trying To Download...```",ms,time.time()))
    except Exception as e:
        return await ms.edit(str(e))

    old = path.split("/downloads/")[1]
    os.rename(f"downloads/{old}",file_path)

    duration=0
    meta = extractMetadata(createParser(file_path))
    if meta and meta.has("duration"): duration = meta.get("duration").seconds

    user_id = update.message.chat.id
    thumb = find(user_id)

    if thumb:
        ph = await bot.download_media(thumb)
        Image.open(ph).convert("RGB").save(ph)
        Image.open(ph).resize((320,320)).save(ph,"JPEG")

        await ms.edit("```Trying To Uploading```")
        try:
            await bot.send_video(user_id,video=file_path,thumb=ph,caption=f"**{new_filename}**",
                duration=duration,progress=progress_for_pyrogram,
                progress_args=("```Trying To Uploading```",ms,time.time()))
            await ms.delete(); os.remove(file_path); os.remove(ph)
        except Exception as e:
            await ms.edit(str(e)); os.remove(file_path); os.remove(ph)

    else:
        await ms.edit("```Trying To Uploading```")
        try:
            await bot.send_video(user_id,video=file_path,caption=f"**{new_filename}**",
                duration=duration,progress=progress_for_pyrogram,
                progress_args=("```Trying To Uploading```",ms,time.time()))
            await ms.delete(); os.remove(file_path)
        except Exception as e:
            await ms.edit(str(e)); os.remove(file_path)



### ======== AUDIO ==============
@Client.on_callback_query(filters.regex("aud"))
async def aud(bot,update):

    new_name = update.message.reply_to_message.text  # FIX
    if new_name is None:
        return await update.message.reply("❌ Rename text missing. Retry!")

    name = new_name.split(":-") if ":-" in new_name else [None,new_name]
    new_filename = name[1]
    file_path=f"downloads/{new_filename}"
    file=update.message.reply_to_message

    ms=await update.message.edit("``` Trying To Download...```")

    try:
        path=await bot.download_media(message=file,progress=progress_for_pyrogram,
            progress_args=("``` Trying To Download...```",ms,time.time()))
    except Exception as e:
        return await ms.edit(str(e))

    old=path.split("/downloads/")[1]
    os.rename(f"downloads/{old}",file_path)

    duration=0
    meta=extractMetadata(createParser(file_path))
    if meta and meta.has("duration"): duration=meta.get("duration").seconds

    user_id=update.message.chat.id
    thumb=find(user_id)

    if thumb:
        ph=await bot.download_media(thumb)
        Image.open(ph).convert("RGB").save(ph)
        Image.open(ph).resize((320,320)).save(ph,"JPEG")

        await ms.edit("```Trying To Uploading```")
        try:
            await bot.send_audio(user_id,audio=file_path,thumb=ph,caption=f"**{new_filename}**",
                duration=duration,progress=progress_for_pyrogram,
                progress_args=("```Trying To Uploading```",ms,time.time()))
            await ms.delete(); os.remove(file_path); os.remove(ph)
        except Exception as e:
            await ms.edit(str(e)); os.remove(file_path); os.remove(ph)

    else:
        await ms.edit("```Trying To Uploading```")
        try:
            await bot.send_audio(user_id,audio=file_path,caption=f"**{new_filename}**",
                duration=duration,progress=progress_for_pyrogram,
                progress_args=("```Trying To Uploading```",ms,time.time()))
            await ms.delete(); os.remove(file_path)
        except Exception as e:
            await ms.edit(str(e)); os.remove(file_path)