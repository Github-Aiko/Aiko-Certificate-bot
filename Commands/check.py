import bot
from datetime import datetime
from typing import Optional, Tuple
from handler import MysqlUtils
from telegram import Update
from telegram.ext import ContextTypes

desc = 'Lấy thông tin người dùng qua UDID Apple'
config = bot.config['bot']

def onQuery(sql):
    result = None  # assign a default value to result
    try:
        db = MysqlUtils()
        result = db.sql_query(sql)
    finally:
        db.close()
        return result

async def autoDelete(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.delete_message(job.chat_id, job.data)

async def exec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    user_id = msg.from_user.id
    chat_type = msg.chat.type
    chat_id = msg.chat_id
    
    if chat_type == 'private' or chat_id == bot.config['bot']['group_id']:
        if len(context.args) > 0:
            if user_id in bot.config['bot']['admin_ids']:
                target_udid_apple = context.args[0]
                user_info = get_user_info_by_udid_apple(target_udid_apple)
                if user_info:
                    purchase_date = user_info[3].strftime('%d/%m/%Y')
                    wait_date_str = user_info[4].strftime('%Y-%m-%d')
                    wait_date_obj = datetime.strptime(wait_date_str, '%Y-%m-%d')
                    wait_days = (wait_date_obj.date() - datetime.now().date()).days
                    info_str = f"Thông tin UDID:\n\n" 
                    if chat_type == 'private':
                        info_str += f"UDID Apple: {user_info[1]}\n"
                    info_str += f"Loại thiết bị: {user_info[2]}\n"           
                    info_str += f"Ngày mua: {purchase_date}\n"
                    if wait_days < 0:
                        info_str += f"Trạng thái: Đang Hoạt Động\n" 
                    else:
                        info_str += f"Thời gian đợi: {wait_days} ngày\n"       
                        info_str += f"Ngày đợi còn lại: {wait_date_obj.strftime('%d/%m/%Y')}"
                    await msg.reply_markdown(info_str)
            else:
                await msg.reply_markdown("❌*Lỗi*\nBạn không có quyền sử dụng lệnh này!")
        else:
            await msg.reply_markdown("❌*Lỗi*\nVui lòng nhập UDID Apple của bạn!")
    else:
        await msg.reply_markdown('❌*Lỗi*\nVui lòng trò chuyện riêng với tôi để thực hiện lệnh này！')

def get_user_info_by_udid_apple(target_udid_apple: str) -> Optional[Tuple]:
    sql = f"SELECT id, udid_apple, type_of_device, purchase_date, wait FROM user WHERE udid_apple = '{target_udid_apple}'"
    result = onQuery(sql)
    if result and len(result) > 0:
        return result[0]
    return None