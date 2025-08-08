# The script uses Alchemy SDK to poll for new blocks continuously.
# For each new block, it fetches detailed block data including transactions.
# Extracts high-level metrics (transactions count, gas used) and placeholders for token transfers.
# Sends the structured JSON data to Kafka topic "ethereum-data".
# Runs in a loop, polling every 5 seconds to keep the data stream updated.

from alchemy import Alchemy, Network
from kafka import KafkaProducer
import json
import time
import os
from dotenv import load_dotenv
load_dotenv()  # loads environment variables from the .env file
from validation import validate_block_data

# Kafka config
KAFKA_TOPIC = "ethereum-data"
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Initialize Alchemy client
alchemy = Alchemy(api_key=os.getenv('ALCHEMY_API_KEY'), network=Network.ETH_MAINNET)

def fetch_latest_block_number():
    latest_block = alchemy.core.get_block_number()
    return latest_block

def fetch_block_data(block_number):
    block = alchemy.core.get_block(block_number, True)  # True: include transactions
    return block

def bytes32_to_address(topic_bytes):
    # topic_bytes is expected to be bytes of length 32
    # Ethereum addresses are right-padded 20 bytes i.e. last 20 bytes are the address
    return '0x' + topic_bytes[-20:].hex()

def extract_relevant_data(block):
    # Example data extraction - customize as needed
    transactions = block['transactions']
    tx_count = len(transactions)
    total_gas_used = block['gasUsed']
    token_transfers = []
    
    TRANSFER_EVENT_SIG = os.getenv("TRANSFER_EVENT_SIG")
    # Extract token transfers from transactions logs (simplified)
    # You can expand to parse logs for ERC20 transfer events.
    # For each transaction in the block, you get its transaction receipt using alchemy.core.get_transaction_receipt(tx_hash) to access logs.
    # Each log represents an event emitted by the contract.
    # You filter logs where the first topic matches the ERC-20 Transfer event signature.
    # The topics and topics fields store the from and to addresses as indexed event parameters, hex encoded but padded to 32 bytes, so you extract the last 40 hex characters (20 bytes) and prefix with 0x.
    # The data field holds the transferred amount as a hex string, converted to int then to string.
    # You accumulate these parsed transfer events in token_transfers list.
    # This enriches your block data with actual token transfer details for Kafka streaming and later ML consumption.
    for i,tx in enumerate(transactions):
        # receipt fetch debugging (every 100th)
        if(i%100==0): print(f"Fetching receipt for tx {i+1}/{len(transactions)}: {tx['hash']}")
        receipt = alchemy.core.get_transaction_receipt(tx['hash'])
        # Fetch full tx receipt to get logs
        receipt = alchemy.core.get_transaction_receipt(tx['hash'])
        if not receipt: continue

        logs = receipt.get('logs', [])
        for log in logs:
            # Check if this log is a Transfer event for an ERC-20 token
            if len(log['topics']) >= 3 and log['topics'][0].lower() == TRANSFER_EVENT_SIG:
                token_address = log['address']
                
                # Topics 1 and 2 are indexed from and to addresses (padded 32-byte hex)
                # from_address = '0x' + log['topics'][1][26:].lower()
                # to_address = '0x' + log['topics'][2][26:].lower()
                from_address = bytes32_to_address(log['topics'][1])
                to_address = bytes32_to_address(log['topics'][2])

                # The 'data' field contains the value transferred as hex (uint256)
                amount = str(int(log['data'], 16))

                token_transfers.append({
                    "tokenAddress": token_address,
                    "from": from_address,
                    "to": to_address,
                    "amount": amount
                })

    data = {
        "blockNumber": block['number'],
        "transactionsCount": tx_count,
        # "gasUsed": total_gas_used,
        "gasUsed": str(total_gas_used),
        "tokenTransfers": token_transfers,
        "timestamp": block['timestamp']
    }
    return data

def main():
    last_processed_block = fetch_latest_block_number() - 1

    while True:
        try:
            current_block = fetch_latest_block_number()
            if current_block > last_processed_block:
                for block_num in range(last_processed_block + 1, current_block + 1):
                    block_data = fetch_block_data(block_num)
                    extracted_data = extract_relevant_data(block_data)
                    # This integration ensures your streamed data adheres to the schema contract, preventing bad or malformed data from entering Kafka.
                    # After extracting data
                    validate_block_data(extracted_data)
                    # proceed to send to Kafka after successful validation
                    producer.send(KAFKA_TOPIC, extracted_data)

                    # Send to Kafka
                    producer.send(KAFKA_TOPIC, extracted_data)
                    producer.flush()
                    print(f"\n---------------------\n---------------------\nSent block {block_num} data to Kafka\n---------------------\n---------------------\n")

                last_processed_block = current_block

            time.sleep(5)  # Poll interval in seconds

        except Exception as e:
            print(f"Error fetching/sending data: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()