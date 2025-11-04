from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import re
import os
import asyncio

# Read your bot token from Render environment variable
TOKEN = os.getenv("TOKEN")

async def link_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the user replied to a message
    if update.message.reply_to_message and update.message.reply_to_message.text:
        text = update.message.reply_to_message.text

        # Look for a team code (starts with X, 7–9 characters, uppercase letters/numbers)
        match = re.search(r'\bX[A-Z0-9]{6,8}\b', text)
        if match:
            code = match.group(0)
            link = f"https://link.brawlstars.com/invite/gameroom/en?tag={code}"
            await update.message.reply_text(
                f"🔗 **Brawl Stars Team Link:**\n{link}",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text("❌ No team code found in that message.")
    else:
        await update.message.reply_text("ℹ️ Please reply with /link to a message containing the team code.")

async def main():
    if not TOKEN:
        print("❌ ERROR: Bot token not found. Set TOKEN environment variable on Render.")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("link", link_command))
    print("🤖 Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
