import asyncio
from pyrogram import Client, filters
from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
from info import DATABASE_NAME, DATABASE_URI, CHAT_ID

MONGODB_URI = DATABASE_URI

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client["price_tracker"]
products_collection = db["products"]

@Client.on_message(filters.command("track"))
async def track_price(client, message):
    # Get product URL and validate
    try:
        product_url = message.text[6:]
        if not product_url:
            raise ValueError("Please provide a product URL to track.")
    except ValueError as e:
        await message.reply_text(str(e))
        return

    # Check if product already tracked
    product_id = product_url
    if products_collection.find_one({"_id": product_id}):
        await message.reply_text(f"Product '{product_id}' already tracked. Use '/price {product_id}' to check its price.")
        return

    # Get website currency
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, "lxml")
    currency_symbol = soup.find("span", class_="currency-symbol").text

    # Save product info to MongoDB
    product_data = {
        "_id": product_id,
        "url": product_url,
        "currency": currency_symbol,
    }
    products_collection.insert_one(product_data)

    await message.reply_text(f"Started tracking product at '{product_url}'. Use '/price {product_id}' to check its price.")

@Client.on_message(filters.command("price"))
async def get_price(client, message):
    # Get product ID from command
    try:
        product_id = message.text[6:]
        if not product_id:
            raise ValueError("Please provide a product ID to check its price.")
    except ValueError as e:
        await message.reply_text(str(e))
        return

    # Get product data from MongoDB
    product_data = products_collection.find_one({"_id": product_id})
    if not product_data:
        await message.reply_text(f"Product '{product_id}' not tracked. Use '/track' to start tracking it.")
        return

    # Get current price and check validity
    current_price = None
    response = requests.get(product_data["url"])
    soup = BeautifulSoup(response.content, "lxml")
    try:
        price_element = soup.find("span", class_="price")
        price_text = price_element.text.replace(product_data["currency"], "")
        current_price = float(price_text)
    except (TypeError, ValueError):
        await message.reply_text(f"Couldn't retrieve price for '{product_id}'.")
        return

    # Reply with current price
    await message.reply_text(f"Current price of '{product_id}' is {current_price} {product_data['currency']}.")
