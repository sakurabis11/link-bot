from pyrogram import Client, filters
from fpdf import FPDF

@Client.on_message(filters.command(["txt", "pdf"]))
async def convert_text(client, message):
    command = message.command[0]
    text = message.reply_to_message.text

    if command == "txt":
        await create_txt_file(text, message.chat.id)
    elif command == "pdf":
        await create_pdf_file(text, message.chat.id)
    else:
        await message.reply_text("Invalid command. Please use /txt or /pdf.")

async def create_txt_file(text, chat_id):
    with open("text.txt", "w") as f:
        f.write(text)
    await client.send_document(chat_id, document="text.txt")

async def create_pdf_file(text, chat_id):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(w=0, h=5, txt=text)
    pdf.output("text.pdf")
    await client.send_document(chat_id, document="text.pdf")


