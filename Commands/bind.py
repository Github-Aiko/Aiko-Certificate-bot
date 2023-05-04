import bot
from handler import MysqlUtils
from telegram import Update
from telegram.ext import ContextTypes

desc = 'Liên kết UDID vào Telegram bot'
config = bot.config['bot']


def onQuery(sql):
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
    chat_id = msg.chat_id
    chat_type = msg.chat.type
    if chat_type == 'private':
        user = onQuery(
            'SELECT * FROM user WHERE `telegram_id` = %s' % user_id)
        if len(user) == 0:
            if len(context.args) == 1:
                udid_apple = context.args[0]
                user = onQuery(
                    'SELECT * FROM user WHERE `udid_apple` = "%s"' % udid_apple)
                if len(user) == 1:
                    db = MysqlUtils()
                    db.update_one('user', params={
                        'telegram_id': user_id}, conditions={'udid_apple': udid_apple})
                    db.conn.commit()
                    db.close()
                    await msg.reply_markdown('✔️*Thành Công*\nBạn đã liên kết thành công Telegram với UDID Apple!')
                else:
                    await msg.reply_markdown('❌*Lỗi*\nUDID Apple không hợp lệ hoặc đã được liên kết với một tài khoản khác!')
            else:
                await msg.reply_markdown('❌*Lỗi*\nĐịnh dạng đúng là: `/bind udid_apple`')
        else:
            await msg.reply_markdown('❌*Lỗi*\nBạn đã Liên kết tài khoản!')
    else:
        if chat_id == config['group_id']:
            callback = await msg.reply_markdown('❌*Lỗi*\nVui lòng trò chuyện riêng với tôi để thực hiện liên kết tài khoản！')
            context.job_queue.run_once(
                autoDelete, 300, data=msg.id, chat_id=chat_id, name=str(msg.id))
            context.job_queue.run_once(
                autoDelete, 300, data=callback.message_id, chat_id=chat_id, name=str(callback.message_id))
