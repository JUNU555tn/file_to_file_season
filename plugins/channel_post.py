import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
import os

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode
from database.database import is_banned_user

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start', 'users', 'broadcast', 'batch', 'count', 'genlink', 'stats', 'total', 'puser', 'removepremium', 'premiumlist', 'ban', 'unban', 'listban', 'dverify']))
async def channel_post(client: Client, message: Message):
    user_id = message.from_user.id

    # Check if user is banned (even admins can be banned)
    if await is_banned_user(user_id):
        return await message.reply(
            "🚫 **You are banned from using this bot.**\n\n"
            "Contact support if you think this is a mistake."
        )

    reply_text = await message.reply_text("Please Wait...!", quote=True)
    try:
        thumbnail_path = None  # Initialize thumbnail_path for cleanup
        post_message = None

        # Check if the message contains a video with a thumbnail
        if message.video and message.video.thumbs:
            thumbnail = message.video.thumbs[0].file_id
            thumbnail_path = await client.download_media(thumbnail)

        # Check if the message contains a document with a thumbnail
        elif message.document and message.document.thumbs:
            thumbnail = message.document.thumbs[0].file_id
            thumbnail_path = await client.download_media(thumbnail)

        # Check if the message contains a GIF with a thumbnail
        elif message.animation and message.animation.thumbs:
            thumbnail = message.animation.thumbs[0].file_id
            thumbnail_path = await client.download_media(thumbnail)

        # Use the new secure token system
        from helper_func import create_file_link

        # Copy message to saved messages (user client) or DB channel
        if hasattr(client, 'user_client') and client.user_client:
            try:
                # First, the bot forwards the message to the user client's account
                # This creates a bridge between bot and user client
                forwarded = await message.forward(chat_id=client.storage_user_id)
                
                # Check if forwarding was successful
                if forwarded and forwarded.id:
                    # Small delay to ensure message is available
                    await asyncio.sleep(0.5)
                    
                    # Now user client can copy it to saved messages
                    post_message = await client.user_client.copy_message(
                        chat_id="me",
                        from_chat_id=client.storage_user_id,
                        message_id=forwarded.id
                    )
                    
                    # Delete the forwarded message from user's chat to keep it clean
                    await forwarded.delete()
                else:
                    # If forward failed, fall back to channel storage
                    print("Forward returned None, using channel storage instead")
                    if hasattr(client, 'db_channel'):
                        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
                    else:
                        raise Exception("Forward failed and no channel storage available")
                
            except Exception as e:
                print(f"Error copying to saved messages: {e}")
                # Fallback to channel storage on error (if available)
                if hasattr(client, 'db_channel'):
                    post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
                else:
                    raise Exception("Both saved messages and channel storage failed")
        else:
            # Fallback to channel storage
            if hasattr(client, 'db_channel'):
                post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
            else:
                raise Exception("No storage method available (neither user_client nor db_channel)")

        # Generate secure link with token
        link, token = await create_file_link(client, post_message.id)

        # Prepare the caption with the link
        caption = f"<strong>🥵 DIRECT VIDEO 📂 👇\n\n{link}\n\n⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪\nBuy vip for 🔞 direct Video  @Myhero2k\n\n©️BACKUP CHANNEL @JNK_BACKUP\n⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪</strong>"

        # Send the link
        if thumbnail_path:
            # Send with thumbnail
            await client.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail_path,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]]
                )
            )
        else:
            # Send without thumbnail
            await message.reply_text(caption, reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]]
            ))

        # Delete the original media message if it was a media message
        if message.video or message.document or message.animation:
            await message.delete()

        # Remove the "Please Wait..." message after processing
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
