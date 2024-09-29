import requests
import json
import os
from telegram import Bot
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load Telegram configuration
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
USER_ID = os.getenv('TELEGRAM_USER_ID')

# Dynamically load addresses and aliases
ADDRESSES = []
ALIASES = {}

# Loop through environment variables to find addresses and aliases
index = 1
while True:
    address_key = f'BITCOIN_ADDRESS_{index}'
    alias_key = f'BITCOIN_ALIAS_{index}'
    
    address = os.getenv(address_key)
    if not address:
        break  # No more addresses found, break the loop
    
    alias = os.getenv(alias_key)
    ADDRESSES.append(address)
    
    # If an alias exists for the address, store it
    if alias:
        ALIASES[address] = alias
    
    index += 1

MEMPOOL_API_URL = os.getenv('MEMPOOL_API_URL', 'http://mempool.space/api')

# Path to the local JSON file used to store transaction data
TX_DATABASE_FILE = "/app/mempool_transactions.json"

def get_alias(address):
    """Get the alias for the address, or return the address if no alias exists."""
    return ALIASES.get(address, address)

def load_existing_transactions():
    """Load the existing mempool transactions from the local JSON file."""
    if os.path.exists(TX_DATABASE_FILE):
        with open(TX_DATABASE_FILE, "r") as file:
            return json.load(file)
    else:
        return {}

def save_transactions(transactions):
    """Save the current mempool transactions to the local JSON file."""
    try:
        with open(TX_DATABASE_FILE, "w") as file:
            json.dump(transactions, file, indent=4)
    except Exception as e:
        print(f"Error saving transactions: {e}", flush=True)

def fetch_mempool_transactions(address):
    """Fetch the latest mempool transactions for a specific address."""
    try:
        response = requests.get(f"{MEMPOOL_API_URL}/address/{address}/txs/mempool")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching from Mempool API for address {address}: {e}", flush=True)
        return []

def send_telegram_message(message):
    """Send a message to the user via Telegram."""
    try:
        bot = Bot(TOKEN)
        bot.send_message(chat_id=USER_ID, text=message, parse_mode='Markdown')
        print("Message sent:", message, flush=True)
    except Exception as e:
        print(f"Error sending Telegram message: {e}", flush=True)

def detect_changes(existing_txs, current_txs):
    """Detect new transactions and confirmed transactions."""
    existing_tx_ids = set(existing_txs.keys())
    current_tx_ids = {tx['txid'] for tx in current_txs}

    # Transactions that are new in the mempool
    new_txs = current_tx_ids - existing_tx_ids

    # Transactions that were in the mempool but are now confirmed
    confirmed_txs = existing_tx_ids - current_tx_ids

    return new_txs, confirmed_txs

def format_message_by_address(address, alias, txs, message_type="new"):
    """Format the message for transactions grouped by address, using aliases if available."""
    if message_type == "new":
        message_lines = [
            f"Transaction ID: {txid}\n[Ordiscan](https://ordiscan.com/tx/{txid}), [Mempool](https://mempool.space/tx/{txid})"
            for txid in txs
        ]
        if alias != address:
            return f"🚀 New unconfirmed transaction(s) for {alias}:\n\n" + "\n\n".join(message_lines)
        else:
            return f"🚀 New unconfirmed transaction(s) for {address}:\n\n" + "\n\n".join(message_lines)

    elif message_type == "confirmed":
        message_lines = [
            f"Transaction ID: {txid}\n[Ordiscan](https://ordiscan.com/tx/{txid}), [Mempool](https://mempool.space/tx/{txid})"
            for txid in txs
        ]
        if alias != address:
            return f"✅ Confirmed transaction(s) for {alias}:\n\n" + "\n\n".join(message_lines)
        else:
            return f"✅ Confirmed transaction(s) for {address}:\n\n" + "\n\n".join(message_lines)

def process_mempool_transactions():
    """Main logic to process mempool transactions for multiple addresses."""
    # Load previous transactions from the local JSON file
    existing_transactions = load_existing_transactions()

    # Initialize a separate store for transactions per address
    updated_transactions_by_address = {}

    # Collect transactions across all addresses
    for address in ADDRESSES:
        print(f"Fetching transactions for address: {address}")
        current_transactions = fetch_mempool_transactions(address)

        # Get existing transactions for this address (or initialize an empty dict)
        existing_for_address = existing_transactions.get(address, {})

        # Detect changes for this specific address
        new_txs, confirmed_txs = detect_changes(existing_for_address, current_transactions)

        # Handle new transactions for each address
        if new_txs:
            alias = get_alias(address)
            print(f"New transactions detected for {alias}: {new_txs}")
            message = format_message_by_address(address, alias, new_txs, message_type="new")
            send_telegram_message(message)

        # Handle confirmed transactions for each address
        if confirmed_txs:
            alias = get_alias(address)
            print(f"Confirmed transactions for {alias}: {confirmed_txs}")
            message = format_message_by_address(address, alias, confirmed_txs, message_type="confirmed")
            send_telegram_message(message)

        # Update transaction store for this address
        updated_transactions_by_address[address] = {tx['txid']: tx for tx in current_transactions}

    # Save updated transactions to the local database
    save_transactions(updated_transactions_by_address)

if __name__ == "__main__":
    process_mempool_transactions()
