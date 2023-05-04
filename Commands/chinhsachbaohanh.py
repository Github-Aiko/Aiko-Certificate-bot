from telegram import Update
from telegram.ext import ContextTypes
import bot

desc = 'Chính sách bảo hành của Aiko'
config = bot.config['bot']

def getPolicyUpdateMessage():
    message = (
        f"📢 *THÔNG BÁO CHÍNH SÁCH BẢO HÀNH CERTIFICATE CỦA AIKO* 📢\n\n"
        f"Chính sách bảo hành CERTIFICATE của Aiko như sau:\n\n"
        f"👉 Đối với chứng chỉ hết hạn trước 9 tháng: Cấp lại chứng chỉ mới có thời hạn từ 6 tháng đến 1 năm.\n\n"
        f"👉 Đối với chứng chỉ khi bị thu hồi:\n"
        f"+ Lần đầu thu hồi: Gửi UDID + hình ảnh chứng chỉ bị thu hồi cho admin và chờ 17-20 ngày để nhận lại chứng chỉ mới.\n"
        f"+ Lần thứ 2 thu hồi: Gửi UDID + hình ảnh chứng chỉ bị thu hồi cho admin và chờ 33-35 ngày để nhận lại chứng chỉ mới.\n"
        f"+ Lần thứ 3 thu hồi: Gửi UDID + hình ảnh chứng chỉ bị thu hồi cho admin và chờ 63-65 ngày để nhận lại chứng chỉ mới.\n"
        f"*Lưu ý: Máy bị thu hồi càng nhiều lần thì Apple khóa càng lâu.*\n\n"
        f"👉 Đối với các trường hợp đổi thiết bị, máy bị mất emei, lèo nhèo -> Từ chối bảo hành.\n\n"
        f"Xin vui lòng liên hệ với chúng tôi nếu bạn có bất kỳ câu hỏi nào về chính sách bảo hành của Aiko.\n\n"
        f"Trân trọng,\n"
        f"Aiko"
    )
    return message

async def autoDelete(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.delete_message(job.chat_id, job.data)

async def exec(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    chat_id = msg.chat_id
    chat_type = msg.chat.type
    
    if chat_type == 'private' or chat_id == bot.config['bot']['group_id']:
        message = getPolicyUpdateMessage()
        callback = await msg.reply_markdown(message)
        if chat_type != 'private':
            context.job_queue.run_once(
                autoDelete, 300, data=msg.message_id, chat_id=chat_id, name=str(msg.message_id))
            context.job_queue.run_once(
                autoDelete, 300, data=callback.message_id, chat_id=chat_id, name=str(callback.message_id))

