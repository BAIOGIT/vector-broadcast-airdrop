import requests
import sqlite3

# Replace this with the actual Solana API endpoint (e.g., Solana RPC)
SOLANA_API_URL = "your_solana_rpc"
VECTOR_PROGRAM_ID = "VFeesufQJnGunv2kBXDYnThT1CoAYB45U31qGDe5QjU"

def fetch_latest_transactions(wallet):
    """
    Fetch the latest transactions for the given wallet address.
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [wallet, {"limit": 3}]
    }

    response = requests.post(SOLANA_API_URL, json=payload)
    if response.status_code == 200:
        result = response.json().get("result", [])
        return result
    else:
        print(f"Error fetching transactions: {response.status_code} - {response.text}")
        return []

def fetch_transaction_details(signature):
    """
    Fetch transaction details by signature.
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTransaction",
        "params": [signature, {"encoding": "jsonParsed","maxSupportedTransactionVersion": 0}]
    }

    response = requests.post(SOLANA_API_URL, json=payload)
    if response.status_code == 200:
        result = response.json().get("result", {})
        return result
    else:
        print(f"Error fetching transaction details: {response.status_code} - {response.text}")
        return None

def save_transaction(signature, status, db_conn):
    """
    Save the transaction to the database if it doesn't already exist.
    """
    try:
        cursor = db_conn.cursor()
        cursor.execute('''
            INSERT INTO trades (signature, status)
            VALUES (?, ?)
        ''', (signature, status, ))
        db_conn.commit()
        print(f"Saved!")
    except sqlite3.IntegrityError:
        pass

def extract_swap_details(transaction):
    """
    Check if the transaction involves the specified VECTOR_PROGRAM_ID.
    """
    if not transaction:
        return None

    try:
        # Get the instructions from the transaction
        instructions = transaction.get("transaction", {}).get("message", {}).get("instructions", [])
        for instruction in instructions:
            # Compare the programId with VECTOR_PROGRAM_ID
            if instruction.get("programId") == VECTOR_PROGRAM_ID:
                # print("Transaction involves the Vector program.")
                return True

        # print("Transaction does not involve the Vector program.")
        return False
    except Exception as e:
        print(f"Error parsing transaction details: {e}")
        return None

def process_transaction(signature, db_conn):
    """
    Fetch transaction details and check if it involves the Vector program.
    """
    transaction = fetch_transaction_details(signature)
    if not transaction:
        print(f"Transaction {signature} could not be fetched.")
        return

    involves_vector = extract_swap_details(transaction)

    if involves_vector:
        print(f"Transaction {signature} involves the Vector program!")
        save_transaction(signature, 'found', db_conn)
        return True
    else:
        print(f"Transaction {signature} does not involve the Vector program.")
        save_transaction(signature, 'null', db_conn)
        return False
