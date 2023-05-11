import bot
from handler import MysqlUtils
from telegram import Update
from telegram.ext import ContextTypes
import re

desc = 'Liệt Kê Tất Cả UDID Khách Hàng'
config = bot.config['bot']

def onQuery(sql):
    try:
        db = MysqlUtils()
        result = db.sql_query(sql)
    finally:
        db.close()
        return result

def clean_text(text):
    # Remove special characters and formatting
    cleaned_text = re.sub(r'[`\*_]', '', text)
    return cleaned_text

def getContent():
    sql = 'SELECT id, udid_apple, purchase_date, date_update, wait FROM user'
    result = onQuery(sql)
    if not result:
        return 'Không tìm thấy thông tin khách hàng nào'
    udid_info = []
    for row in result:
        id = row[0]
        udid_apple = row[1]
        purchase_date = row[2]
        purchase_date = purchase_date.strftime('%d/%m/%Y')
        if row[3] is None:
            date_update = 'Chưa Update'
        else:
            date_update = row[3]
            date_update = date_update.strftime('%d/%m/%Y')
        wait = row[4]
        wait = wait.strftime('%d/%m/%Y')
        udid_info.append(f'ID: {clean_text(str(id))} - UDID: {clean_text(str(udid_apple))} - Ngày Mua: {clean_text(purchase_date)} - Ngày Update: {clean_text(str(date_update))} - Wait: {clean_text(wait)}')
    msg = '\n\n'.join(udid_info)
    msg += '\n\nĐể mua gói dịch vụ, vui lòng liên hệ @Tele_Aiko'
    return msg


async def autoDelete(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    async with context.bot:
        await context.bot.delete_message(job.chat_id, job.data)

async def exec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    user_id = msg.from_user.id
    chat_type = msg.chat.type
    if chat_type == 'private':
        if user_id in bot.config['bot']['admin_ids']:
            content = getContent()
            await msg.reply_text(content)
        else:
            await msg.reply_text('Bạn không có quyền truy cập')
    else:
        await msg.reply_text('Bạn phải sử dụng lệnh này trong chat riêng với bot')
