from telegram import Update
from telegram.ext import ContextTypes
import bot

desc = 'Nhận thông tin trò chuyện hiện tại'
config = bot.config['bot']


async def autoDelete(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.delete_message(job.chat_id, job.data)


async def exec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    user_id = msg.from_user.id
    chat_id = msg.chat_id
    chat_type = msg.chat.type
    
    # gửi cho người dùng thông tin trò chuyện hiện tại
    if chat_type == 'private':
        callback = await msg.reply_text(f'👨🏼‍🔧User ID: `{user_id}`', parse_mode='Markdown')
    # gửi cho nhóm thông tin trò chuyện hiện tại
    elif chat_id == config['group_id']:
        callback =  await msg.reply_text(f'👥Chat ID: `{chat_id}`', parse_mode='Markdown')
    # xóa tin nhắn
    if chat_type != 'private':
            context.job_queue.run_once(
                autoDelete, 300, data=msg.id, chat_id=chat_id, name=str(msg.id))
            context.job_queue.run_once(
                autoDelete, 300, data=callback.message_id, chat_id=chat_id, name=str(callback.message_id))

        
        