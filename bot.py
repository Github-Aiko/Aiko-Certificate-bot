import logging
import yaml
import sys
from sshtunnel import SSHTunnelForwarder
from datetime import time

from telegram import __version__ as TG_VER
from telegram import BotCommand

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]
if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"Bot này không tương thích với phiên bản PTB hiện tại của bạn {TG_VER}. Để nâng cấp, hãy sử dụng lệnh sau:"
        f"pip3 install python-telegram-bot --upgrade --pre"
    )
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger(__name__)

VERSION = "1.0"

try:
    f = open('config.yaml', 'r')
    config = yaml.safe_load(f)
except FileNotFoundError as error:
    print('Không tìm thấy tệp cấu hình config.yaml, vui lòng sao chép tệp config.yaml.example và đổi tên thành config.yaml')
    sys.exit(0)

try:
    ssh_cfg = config['cert_bot']['ssh']
    db_cfg = config['cert_bot']['database']
    port = db_cfg['port']
    if ssh_cfg['enable'] is True:
        ssh = SSHTunnelForwarder(
            ssh_address_or_host=(ssh_cfg['ip'], ssh_cfg['port']),
            ssh_username=ssh_cfg['user'],
            ssh_password=ssh_cfg['pass'],
            remote_bind_address=(db_cfg['ip'], db_cfg['port']))
        ssh.start()
        port = ssh.local_bind_port
except Exception as error:
    print('Bạn đã bật SSH nhưng cấu hình SSH liên quan không chính xác')
    sys.exit(0)

try:
    token = config['bot']['token']
    app = Application.builder().token(token).build()
except Exception as error:
    print('Không thể khởi động Telegram Bot, hãy xác nhận xem Bot Token có chính xác hay không, hoặc kết nối với máy chủ Telegram')
    sys.exit(0)


async def onCommandSet(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.delete_my_commands()
    await context.bot.set_my_commands(context.job.data)


def main():
    try:
        # Import thư mục chứa các lệnh
        import Commands
        command_list = []
        for i in Commands.content:
            cmds = getattr(Commands, i)
            app.add_handler(CommandHandler(i, cmds.exec))
            command_list.append(BotCommand(i, cmds.desc))
        app.job_queue.run_once(onCommandSet, 1, command_list, 'onCommandSet')
        # Import thư mục chứa các nhiệm vụ
        import Modules
        for i in Modules.content:
            mods = getattr(Modules, i)
            Conf = mods.Conf
            if Conf.method == 'daily':
                app.job_queue.run_daily(
                    mods.exec, time.fromisoformat(Conf.runtime), name=i)
            elif Conf.method == 'repeating':
                app.job_queue.run_repeating(
                    mods.exec, interval=Conf.interval, name=i)
        # Khởi động Bot
        app.run_polling(drop_pending_updates=True)
    except Exception as error:
        print(error)
        sys.exit(0)


if __name__ == "__main__":
    main()