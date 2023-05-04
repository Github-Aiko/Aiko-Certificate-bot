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
    user_id = msg.from_user.id
    chat_type = msg.chat.type
    
    if len(context.args) > 0:
        if user_id in config['admin_ids']:
            plan_id = context.args[0]
            plan_status = context.args[1]
            if plan_status == 'true' or plan_status == '1':
                plan_status = 1
            elif plan_status == 'false' or plan_status == '0':
                plan_status = 0
            else:
                await msg.reply_markdown('Bạn phải nhập trạng thái là true hoặc false')
                return
            db = MysqlUtils()
            db.update_one('plan', params={
                'status': plan_status
            }, conditions={
                'id': plan_id
            })
            db.conn.commit()
            db.close()
            await msg.reply_markdown('✔️*Thành Công*\nBạn đã cập nhật thành công')
            return
        else:
            await msg.reply_markdown('Bạn không có quyền thực hiện lệnh này')
            return
    callback = await msg.reply_text(get_plan_info())
    
    if chat_type != 'private':
        context.job_queue.run_once(
            autoDelete, 300, data=msg.id, chat_id=msg.chat_id, name=str(msg.id))
        context.job_queue.run_once(
            autoDelete, 300, data=callback.message_id, chat_id=msg.chat_id, name=str(callback.message_id))
    
