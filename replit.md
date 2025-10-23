# Telegram File Sharing Bot

## Overview
This is a Telegram file sharing bot that stores files in a user's Saved Messages and provides shareable links to access them.

## Recent Changes (October 23, 2025)
**Major Performance Optimization**: Removed file download/upload process

### What Changed
Previously, the bot would:
1. Download files from Telegram to disk
2. Upload them to saved messages
3. Delete the downloaded files

Now, the bot:
1. Uses Telegram file IDs (strings) directly
2. Sends files to saved messages using those IDs
3. No downloading or uploading needed - everything happens via Telegram's internal file references

### Benefits
- ✅ Much faster file processing (no download/upload time)
- ✅ No disk space used for temporary files
- ✅ More efficient bandwidth usage
- ✅ Cleaner code with less complexity

### How It Works
When an admin sends a file to the bot:
1. The bot extracts the `file_id` from the message (a string reference)
2. Uses `send_video()`, `send_document()`, etc. with that `file_id`
3. Saves the message ID to the database with a secure token
4. Users can retrieve files using the generated link

Files are stored as message references (message IDs + file IDs) in:
- MongoDB database (for tokens and message mappings)
- User's Saved Messages (for actual file storage)

## Project Structure
- `main.py` - Entry point
- `bot.py` - Bot initialization and setup
- `config.py` - Configuration and environment variables
- `database/database.py` - Database operations
- `plugins/` - Bot command handlers
  - `channel_post.py` - File storage handler (optimized)
  - `start.py` - Start command and file retrieval
  - `link_generator.py` - Batch link generation
  - Other plugin files for various features

## Environment Variables
- `TG_BOT_TOKEN` - Telegram bot token
- `USER_SESSION_STRING` - User session for saved messages storage
- `DATABASE_URL` - MongoDB connection string
- `CHANNEL_ID` - Fallback channel ID (legacy)
- See `config.py` for complete list

## Key Features
- File storage in user's Saved Messages
- Secure token-based file access
- Batch file link generation
- User verification system
- Force subscription to channels
- Auto-delete messages
- Premium user management
- User ban/unban functionality

## Storage Method
The bot now uses **string-based file storage** via Telegram's file ID system, which is:
- Instant (no file transfer needed)
- Space-efficient (no local storage)
- Secure (files stay within Telegram's infrastructure)
