import logging
import yaml
from sshtunnel import SSHTunnelForwarder

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]
if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This bot is not compatible with your current PTB version {TG_VER}. To upgrade use this command:"
        f"pip3 install python-telegram-bot --upgrade --pre"
    )
from telegram.ext import Application, CommandHandler

import Commands


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger(__name__)


with open('config.yaml') as f:
    config = yaml.safe_load(f)


def main():
    #proxy = 'http://127.0.0.1:7890'
    token = config['bot']['token']
    app = Application.builder().token(token).build()
    #app = Application.builder().token(token).proxy_url(proxy).get_updates_proxy_url(proxy).build()
    for i in Commands.cmd:
        model = getattr(Commands, i)
        app.add_handler(CommandHandler(i, model.exec))

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
