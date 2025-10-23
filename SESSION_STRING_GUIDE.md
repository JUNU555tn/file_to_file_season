
# How to Get User Session String

To use the saved messages storage feature, you need to generate a Pyrogram session string.

## Method 1: Using Replit (Recommended)

1. Create a new file `generate_session.py` in your repl
2. Add this code:

```python
from pyrogram import Client

API_ID = int(input("Enter your API_ID: "))
API_HASH = input("Enter your API_HASH: ")

with Client("my_account", api_id=API_ID, api_hash=API_HASH) as app:
    print("\n" + "="*50)
    print("SESSION STRING:")
    print("="*50)
    print(app.export_session_string())
    print("="*50)
```

3. Run the file: `python generate_session.py`
4. Enter your API_ID and API_HASH when prompted
5. Enter your phone number and OTP code
6. Copy the session string that appears
7. Add it to your Secrets as `USER_SESSION_STRING`

## Method 2: Using @StringSessionBot on Telegram

1. Open [@StringSessionBot](https://t.me/StringSessionBot) on Telegram
2. Click Start
3. Enter your API_ID
4. Enter your API_HASH
5. Enter your phone number
6. Enter the OTP code you receive
7. Copy the session string
8. Add it to your Secrets as `USER_SESSION_STRING`

## Important Notes

- **Never share your session string with anyone**
- The session string gives full access to your Telegram account
- Use a separate Telegram account for the bot (not your personal account)
- Files will be stored in the "Saved Messages" of the account used for the session

## Benefits of Using Saved Messages Storage

1. **No Channel Ban Risk**: Files are stored in your personal saved messages
2. **Privacy**: No need for a public/private channel
3. **Simplicity**: Just one Telegram account needed
4. **Reliability**: Saved messages are permanent and won't be deleted

## Environment Variable

Add this to your Replit Secrets:

```
USER_SESSION_STRING=your_session_string_here
```

If you don't add a session string, the bot will fall back to using the old channel storage method.
