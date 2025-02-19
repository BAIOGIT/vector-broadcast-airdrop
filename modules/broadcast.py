import requests

# URL of the endpoint
VECTOR_API_URL = "https://mainnet-api.vector.fun/graphql"
AUTH_TOKEN = "your_auth_token"

# Function to send a broadcast
def send_broadcast(wallet, signature, message="LFG"):
    # Headers for the request
    headers = {
        "Host": "mainnet-api.vector.fun",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Accept": "*/*",
        "X-App-Name": "Vector",
        "X-App-Version": "1.2.1",
        "X-App-Build-Number": "242",
        "Accept-Language": "it-IT;q=1,en-IT;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "Vector/242 CFNetwork/1494.0.7 Darwin/23.4.0"
    }

    # Payload for the request
    payload = {
        "query": """mutation sendBroadcastMutation(
          $chain: Chain!
          $wallet: String!
          $txSig: String!
          $message: String
          $expiresAt: Timestamp
          $groups: [String!]!
        ) {
          broadcastTrade(chain: $chain, wallet: $wallet, txSig: $txSig, message: $message, expiresAt: $expiresAt, groups: $groups)
        }""",
        "variables": {
            "chain": "SOLANA",
            "wallet": wallet,
            "txSig": signature,
            "message": message,
            "expiresAt": None,
            "groups": [
                "ALL"
            ]
        }
    }

    try:
        # Send the POST request
        response = requests.post(VECTOR_API_URL, json=payload, headers=headers)
        
        # Check for errors
        if response.status_code == 200:
            print("Broadcast sent successfully!")
        else:
            print(f"Failed to send broadcast. Status Code: {response.status_code}")
            print("Response Body:", response.text)
    except requests.RequestException as e:
        print("Error occurred while sending the broadcast:", e)