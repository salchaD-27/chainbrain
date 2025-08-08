from datetime import datetime
from collections import defaultdict

def extract_features(block_data):
    features = {}    
    features['blockNumber'] = block_data['blockNumber']
    
    # Time features from timestamp
    dt = datetime.utcfromtimestamp(block_data['timestamp'])
    features['hour'] = dt.hour
    features['day_of_week'] = dt.weekday()

    # Numeric features
    features['transactionsCount'] = block_data['transactionsCount']
    features['gasUsed'] = int(block_data['gasUsed'])

    # Token transfer aggregates
    token_transfers = block_data.get('tokenTransfers', [])
    features['tokenTransfersCount'] = len(token_transfers)

    token_amounts = defaultdict(int)
    unique_senders = set()
    unique_receivers = set()

    for transfer in token_transfers:
        token_amounts[transfer['tokenAddress']] += int(transfer['amount'])
        unique_senders.add(transfer['from'])
        unique_receivers.add(transfer['to'])

    features['totalTokenAmount'] = sum(token_amounts.values())
    features['uniqueSenders'] = len(unique_senders)
    features['uniqueReceivers'] = len(unique_receivers)

    return features
