import os
from pyrogram import Client ,filters
from helper.database import getid

ADMIN = 7576729648   # ADMIN ID

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["broadcast"]))
async def broadcast(bot, message):
    if message.reply_to_message:
        ids = getid()     # sab users ki ID database se fetch
        if not ids:
            return await message.reply("⚠ Database empty — Koi users nahi mila.")

        ms = await message.reply_text("🔍 Fetching users from database...")

        tot = len(ids)
        sent = 0

        await ms.edit(f"📢 Broadcast Started...\n🟢 Sending message to {tot} users...")

        for user_id in ids:
            try:
                await message.reply_to_message.copy(user_id)
                sent += 1
            except:
                pass    # jo fail hojaye skip

        await ms.edit(f"✨ Broadcast Finished!\n\n📨 Successfully Delivered to **{sent}/{tot} users**")