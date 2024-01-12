import pyrogram
from pyrogram import Client, filters

def create_board():
    return [["-" for _ in range(3)] for _ in range(3)]

def check_winner(board):
    # Check rows
    for row in board:
        if all(cell == row[0] for cell in row) and row[0] != "-":
            return True

    # Check columns
    for col in range(3):
        if all(row[col] == board[0][col] for row in board) and board[0][col] != "-":
            return True

    # Check diagonals
    if all(board[i][i] == board[0][0] for i in range(3)) and board[0][0] != "-":
        return True
    if all(board[i][2 - i] == board[0][2] for i in range(3)) and board[0][2] != "-":
        return True

    # Check for tie
    if all(cell != "-" for row in board for cell in row):
        return "tie"

    return False

def make_move(board, player, position):
    row, col = position
    board[row][col] = player

def get_bot_move(board):
    # Simple random move strategy
    available_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == "-"]
    return available_cells[random.randrange(len(available_cells))]

async def update_board_message(chat_id, message_id, board):
    board_string = "\n".join(" | ".join(row) for row in board)
    await app.edit_message_text(chat_id=chat_id, message_id=message_id, text=board_string)

@Client.on_message(filters.command("game"))
async def start_game(client, message):
    board = create_board()
    player_turn = True  # True for user, False for bot

    keyboard = [
        [
            pyrogram.InlineKeyboardButton("Cross ❌", callback_data="cross"),
            pyrogram.InlineKeyboardButton("Circle ⭕", callback_data="circle"),
        ]
    ]
    reply_markup = pyrogram.InlineKeyboardMarkup(keyboard)
    await message.reply("Choose your symbol:", reply_markup=reply_markup)

@Client.on_callback_query()
async def handle_callback(client, callback_query):
    if callback_query.data in ["cross", "circle"]:
        user_symbol = callback_query.data
        bot_symbol = "circle" if user_symbol == "cross" else "cross"
        await play_game(client, callback_query.message, board, user_symbol, bot_symbol)

async def play_game(client, message, board, user_symbol, bot_symbol):
    await update_board_message(message.chat.id, message.message_id, board)

async def play_game(client, message, board, user_symbol, bot_symbol):
    await update_board_message(message.chat.id, message.message_id, board)

    while True:
        try:
            if player_turn:
                # Get user's move
                await message.reply("Your turn. Choose a cell (e.g., 1,2):")
                user_input = await app.get_message(chat_id=message.chat.id, message_id=message.message_id + 1)
                row, col = map(int, user_input.text.split(","))

                if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == "-":
                    make_move(board, user_symbol, (row, col))
                    await update_board_message(message.chat.id, message.message_id, board)

                    if check_winner(board):
                        await message.reply("You won!")
                        break
                    elif check_winner(board) == "tie":
                        await message.reply("It's a tie!")
                        break

            else:
                # Bot's turn
                bot_move = get_bot_move(board)
                make_move(board, bot_symbol, bot_move)
                await update_board_message(message.chat.id, message.message_id, board)

                if check_winner(board):
                    await message.reply("I won!")
                    break
                elif check_winner(board) == "tie":
                    await message.reply("It's a tie!")
                    break

            player_turn = not player_turn

        except Exception as e:
            await message.reply("An error occurred: {}".format(e))
            break

