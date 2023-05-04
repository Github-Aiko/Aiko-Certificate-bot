import bot
from handler import MysqlUtils
from telegram import Update
from telegram.ext import ContextTypes
import re
from datetime import datetime, timedelta

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

def is_udid_exist(db: MysqlUtils, udid: str) -> bool:
    cursor = db.conn.cursor()
    sql = 'SELECT COUNT(*) FROM `user` WHERE `udid_apple` = %s'
    cursor.execute(sql, (udid,))
    row = cursor.fetchone()
    return row[0] > 0


async def exec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    user_id = msg.from_user.id
    chat_type = msg.chat.type
    if chat_type == 'private':
        if user_id in config['admin_ids']:
            if len(context.args) == 3:
                udid_apple = context.args[0]
                type_of_device = context.args[1]
                wait_str = context.args[2]
                wait_days = None
                
                # kiểm tra xem wait có định dạng số + ký tự "d" hay không
                if re.match(r'^\d+d$', wait_str):
                    # trích xuất số ngày từ chuỗi wait
                    wait_days = int(wait_str[:-1])
                
                if wait_days is not None:
                    # tính toán ngày kết thúc
                    end_date = datetime.today() + timedelta(days=wait_days)
                    wait = end_date.strftime('%Y-%m-%d')
                else:
                    # nếu không có định dạng hợp lệ, báo lỗi
                    await msg.reply_markdown('❌*Lỗi*\nĐịnh dạng đúng là: `/add udid_apple type_of_device wait(d)`')
                    return

                purchase_date = datetime.today().strftime('%Y-%m-%d')

                db = MysqlUtils()
                # kiểm tra xem UDID đã tồn tại trong cơ sở dữ liệu hay chưa
                if is_udid_exist(db, udid_apple):
                    cursor = db.conn.cursor()
                    # sử dụng câu lệnh UPDATE để cập nhật thông tin của bản ghi
                    sql = '''
                        UPDATE `user`
                        SET `type_of_device` = %s, `purchase_date` = %s, `wait` = %s
                        WHERE `udid_apple` = %s
                    '''
                    params = (type_of_device, purchase_date, wait, udid_apple)
                    cursor.execute(sql, params)
                    db.conn.commit()
                    db.close()
                    await msg.reply_markdown('✔️*Thành Công*\nĐã cập nhật thông tin vào cơ sở dữ liệu!')
                else:
                    cursor = db.conn.cursor()
                    # sử dụng câu lệnh INSERT INTO để thêm một bản ghi mới
                    sql = '''
                        INSERT INTO `user` (`udid_apple`, `type_of_device`, `purchase_date`, `wait`)
                        VALUES (%s, %s, %s, %s)
                    '''
                    params = (udid_apple, type_of_device, purchase_date, wait)
                    cursor.execute(sql, params)
                    db.conn.commit()
                    db.close()
                    await msg.reply_markdown('✔️*Thành Công*\nĐã thêm thông tin vào cơ sở dữ liệu!')
            else:
                await msg.reply_markdown('❌*Lỗi*\nĐịnh dạng đúng là: `/add udid_apple type_of_device wait(d)`')
        else:
            await msg.reply_markdown('❌*Lỗi*\nBạn không có quyền thực hiện lệnh này!')
    else:
        await msg.reply_markdown('❌*Lỗi*\nVui lòng trò chuyện riêng với tôi để thực hiện lệnh này！')
