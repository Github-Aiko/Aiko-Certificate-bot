desc = 'Bắt đầu với Bot'


async def exec(update, context) -> None:
    await update.message.reply_text('Xin chào, tôi là bot của nhóm @aiko_certificate')
