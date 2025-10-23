import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode
from database.database import is_banned_user

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start', 'users', 'broadcast', 'batch', 'count', 'genlink', 'stats', 'total', 'puser', 'removepremium', 'premiumlist', 'ban', 'unban', 'listban', 'dverify']))
async def channel_post(client: Client, message: Message):
    user_id = message.from_user.id

    if await is_banned_user(user_id):
        return await message.reply(
            "🚫 **You are banned from using this bot.**\n\n"
            "Contact support if you think this is a mistake."
        )

    reply_text = await message.reply_text("Please Wait...!", quote=True)
    try:
        thumbnail_path = None

        if message.video and message.video.thumbs:
            thumbnail = message.video.thumbs[0].file_id
            thumbnail_path = await client.download_media(thumbnail)
        elif message.document and message.document.thumbs:
            thumbnail = message.document.thumbs[0].file_id
            thumbnail_path = await client.download_media(thumbnail)
        elif message.animation and message.animation.thumbs:
            thumbnail = message.animation.thumbs[0].file_id
            thumbnail_path = await client.download_media(thumbnail)

        from helper_func import create_file_link

        if hasattr(client, 'user_client') and client.user_client:
            try:
                bot_me = await client.get_me()
                bot_id = bot_me.id
                
                forwarded = await client.forward_messages(
                    chat_id=client.storage_user_id,
                    from_chat_id=message.chat.id,
                    message_ids=message.id
                )
                
                import asyncio
                await asyncio.sleep(0.5)
                
                post_message = await client.user_client.forward_messages(
                    chat_id="me",
                    from_chat_id=bot_id,
                    message_ids=forwarded.id
                )
                
                await client.user_client.delete_messages(
                    chat_id=bot_id,
                    message_ids=forwarded.id
                )
                
                print(f"✅ Message saved to user's saved messages (no download/upload)")
                
            except Exception as e:
                print(f"Error saving to saved messages: {e}")
                if hasattr(client, 'db_channel'):
                    post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
                else:
                    raise Exception("Both saved messages and channel storage failed")
        else:
            if hasattr(client, 'db_channel'):
                post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
            else:
                raise Exception("No storage method available (neither user_client nor db_channel)")

        link, token = await create_file_link(client, post_message.id)

        caption = f"<strong>🥵 DIRECT VIDEO 📂 👇\n\n{link}\n\n⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪\nBuy vip for 🔞 direct Video  @Myhero2k\n\n©️BACKUP CHANNEL @JNK_BACKUP\n⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪</strong>"

        if thumbnail_path:
            await client.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail_path,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]]
                )
            )
        else:
            await message.reply_text(caption, reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]]
            ))

        if message.video or message.document or message.animation:
            await message.delete()

        if 'reply_text' in locals():
            await reply_text.delete()

        if not DISABLE_CHANNEL_BUTTON:
            try:
                await post_message.edit_reply_markup(InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]]
                ))
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception:
                pass

    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return

@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):
    if DISABLE_CHANNEL_BUTTON:
        return

    from helper_func import create_file_link
    link, token = await create_file_link(client, message.id)
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])

    try:
        await message.edit_reply_markup(reply_markup)
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception:
        pass
