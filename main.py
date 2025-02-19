import os
import time

from modules.database import setup_database, get_transactions_hashes
from modules.scan import fetch_latest_transactions, process_transaction
from modules.broadcast import send_broadcast

# Replace this with the absolute path inside your container or desired location
# DB_PATH = '/usr/src/app/db/vector.db'
DB_PATH = './db/vector.db'
WALLET_ADDRESS = "your_wallet_address"  # Replace with your wallet address

def main():
    # Ensure the data directory exists
    os.makedirs('db', exist_ok=True)

    # Database setup
    conn = setup_database(DB_PATH)

    print(f"Monitoring wallet {WALLET_ADDRESS} for new transactions...")
    while True:
        # Fetch the latest transaction for the wallet
        transactions = fetch_latest_transactions(WALLET_ADDRESS)

        if transactions:
            for tx in transactions:
                signature = tx.get("signature")

                if signature in get_transactions_hashes(DB_PATH):
                    # print(f"Transaction already processed.")
                    continue
                else:
                    print(f"Processing transaction {signature}")
                    isVectorTx = process_transaction(signature, conn)

                    if isVectorTx:
                        print(f"Creating broadcast...")

                        # Create a caption for the broadcast
                        caption = f"Fadoors"
                        
                        # Send the broadcast
                        send_broadcast(WALLET_ADDRESS, signature, caption)

        else:
            print(f"No new transactions found.")

        # Wait for 2 seconds before the next iteration
        time.sleep(2)

if __name__ == "__main__":
    main()