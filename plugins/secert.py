from pyrogram import filters, Client

@Client.on_message(filters.command("send_secret") & filters.chat(int(-1002002636126)))
async def handle_group_message(client, message):
        try:
            recipient_id = int(message.text.split(None, 2)[1])  # Extract recipient ID
            text = message.text.split(None, 2)[2]  # Extract message text

            await client.send_message(
                recipient_id,
                text,
                reply_to_message_id=message.message_id  # Link back to original message
            )

            await message.delete()  # Delete original message to hide command
            await client.send_message(message.chat.id, "Message sent secretly!")  # Confirm in group
        except (IndexError, ValueError):
            await message.reply_text("Invalid usage. Usage: /send_secret <user_id> <message>")

