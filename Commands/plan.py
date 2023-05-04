import bot
from handler import MysqlUtils
from telegram import Update
from telegram.ext import ContextTypes

config = bot.config['bot']
desc = 'Xem thông tin gói dịch vụ hiện đang bán'

def onQuery(sql):
    result = None  # assign a default value to result
    try:
        db = MysqlUtils()
        result = db.sql_query(sql)
    finally:
        db.close()
        return result

def get_plan_info():
    sql = 'SELECT id,name,IF(status = 1, "Còn hàng", "Hết hàng"),price AS status_text FROM plan'
    result = onQuery(sql)
    if result:
        plan_info = []
        for row in result:
            plan_id = row[0]
            plan_name = row[1]
            plan_status = row[2]
            plan_price = row[3]
            plan_price_str = '{:,.0f} VND'.format(plan_price)
            plan_info.append(f'Gói {plan_id} - Tên gói: {plan_name} - Giá: {plan_price_str} - Tình trạng: {plan_status}')
        msg = '\n'.join(plan_info)
        msg += '\n\nĐể mua gói dịch vụ, vui lòng liên hệ @Tele_Aiko'
        return msg
    else:
        return 'Không tìm thấy thông tin gói dịch vụ'

async def autoDelete(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.delete_message(job.chat_id, job.data)

async def exec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    chat_type = msg.chat.type
    
    callback = await msg.reply_text(get_plan_info())
    
    if chat_type != 'private':
        context.job_queue.run_once(
            autoDelete, 300, data=msg.id, chat_id=msg.chat_id, name=str(msg.id))
        context.job_queue.run_once(
            autoDelete, 300, data=callback.message_id, chat_id=msg.chat_id, name=str(callback.message_id))
    
