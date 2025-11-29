from pyrogram import Client
import os

TOKEN = os.environ.get("TOKEN", "8316171898:AAF5jqCPvv1yU8tZdk_y_CmyVcStaycILnU")

APP_ID = int(os.environ.get("APP_ID", "21218274"))

API_HASH = os.environ.get("API_HASH", "3474a18b61897c672d315fb330edb213")

if __name__ == "__main__" :
    plugins = dict(
        root="plugins"
    )
    app = Client(
        "renamer",
        bot_token=TOKEN,
        api_id=APP_ID,
        api_hash=API_HASH,
        plugins=plugins
    )
    app.run()
