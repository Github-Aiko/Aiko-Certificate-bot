import asyncio

desc = 'Nhận thông tin trò chuyện hiện tại'


async def exec(update, context) -> None:
    msg = update.message
    tid = msg.from_user.id
    gid = msg.chat.id
    chat_type = msg.chat.type

    text = '💥*Hello*\n'
    utid = f'{text}\nID：`{tid}`'

    if chat_type == 'private':
        await msg.reply_markdown(utid)
    else:
        group = f'\nID：`{gid}`'
        if update.message.from_user.is_bot is False:
            callback = await msg.reply_markdown(f'{utid}{group}')
        else:
            callback = await msg.reply_markdown(f'{text}{group}')
        await asyncio.sleep(15)
        await context.bot.deleteMessage(message_id=callback.message_id, chat_id=msg.chat_id)
