import asyncio
import os
import re
import unicodedata
from pyrogram import Client, filters

# 🟢 قراءة التوكن وبيانات API من البيئة
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")

group_username = "@aaaaaac8"

# بيانات القناة والرسالة التي سنحولها
channel_username = "@kim5o11"
message_id_to_forward = 4  # اكتب هنا رقم الرسالة التي تريد تحويلها

raw_text = """
تجربة السيرفر تمام
"""  # حط النصوص اللي تبي تبحث فيها هنا

def normalize(text):
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.replace('ـ', '')
    return text

original_lines = [line.strip() for line in raw_text.strip().splitlines() if line.strip()]
normalized_lines = [normalize(line) for line in original_lines]

app = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

@app.on_message(filters.group & filters.text)
async def search_handler(client, message):
    text = message.text.strip()

    if not text.startswith("بحث"):
        return

    match = re.match(r"بحث\s*(\d+)\s+(.*)", text)
    if match:
        count_requested = int(match.group(1))
        search_line = match.group(2).strip()

        if not search_line:
            await message.reply("❌ يجب أن تكتب رقم ثم سطر كامل للبحث.")
            return

        if search_line.startswith("📖"):
            search_line = search_line[1:].strip()

        normalized_search_line = normalize(search_line)

        found_index = None
        for i, norm_line in enumerate(normalized_lines):
            if normalized_search_line == norm_line:
                found_index = i
                break

        if found_index is None:
            await message.reply("❌ لم أجد هذا السطر بالضبط في البيانات.")
            return

        num_lines_to_send = min(count_requested, 10)
        lines_to_send = original_lines[found_index:found_index + num_lines_to_send]

        reply_text = '\n'.join(f"📖 {line}" for line in lines_to_send)
        await message.reply(reply_text)
        return

    query = text[4:].strip()
    if len(query.split()) == 0:
        await message.reply("❌ اكتب كلمة أو أكثر بعد كلمة بحث.")
        return

    normalized_query = normalize(query)
    results = [original_lines[i] for i, norm_line in enumerate(normalized_lines) if normalized_query in norm_line]

    if len(results) == 0:
        await message.reply("❌ لا يوجد سطر يحتوي على هذا النص.")
    elif len(results) > 10:
        await message.reply("❗ النتائج كثيرة جدًا، حاول تضييق البحث أكثر.")
    else:
        reply_text = '\n'.join(f"📖 {line}" for line in results)
        await message.reply(reply_text)

async def main():
    await app.start()
    print("✅ البوت يعمل الآن ويستمع للرسائل...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
