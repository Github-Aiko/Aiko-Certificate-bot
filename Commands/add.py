import bot
import requests
from handler import MysqlUtils
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime

desc = 'Add UDID vào Telegram bot'
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
    if chat_type == 'private':
        if user_id in config['admin_ids']:
            if len(context.args) == 3:
                udid_apple = context.args[0]
                type_of_device = context.args[1]
                purchase_date_str = context.args[2]
                purchase_date = datetime.strptime(purchase_date_str, '%d/%m/%Y').strftime('%Y-%m-%d')

                db = MysqlUtils()
                db.insert_one('user', params={
                    'udid_apple': udid_apple,
                    'type_of_device': type_of_device,
                    'purchase_date': purchase_date
                })
                db.conn.commit()
                db.close()

                await msg.reply_markdown('✔️*Thành Công*\nĐã thêm thông tin vào cơ sở dữ liệu!')
            else:
                await msg.reply_markdown('❌*Lỗi*\nĐịnh dạng đúng là: `/add udid_apple type_of_device purchase_date(dd/mm/yyyy)`')
        else:
            await msg.reply_markdown('❌*Lỗi*\nBạn không có quyền thực hiện lệnh này!')
    else:
        await msg.reply_markdown('❌*Lỗi*\nVui lòng trò chuyện riêng với tôi để thực hiện lệnh này！')
        
        


        

        
