import random
import time
import config
import requests

PROXY_CONTRACT_ADDRESS = '0x032139f44650481f4d6000c078820B8E734bF253'
IMPLEMENTATION_CONTRACT_ADDRESS = '0x1a29c466817408768c2D21708cF9041A971d9A78'

PROXY_ABI = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "implementation",
                "type": "address"
            },
            {
                "internalType": "bytes",
                "name": "_data",
                "type": "bytes"
            }
        ],
        "stateMutability": "payable",
        "type": "constructor"
    },
    {
        "stateMutability": "payable",
        "type": "fallback"
    }
]

IMPLEMENTATION_ABI = [
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "pairIndex",
                "type": "uint256"
            },
            {
                "internalType": "bool",
                "name": "isLong",
                "type": "bool"
            }
        ],
        "name": "predictPriceMovement",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

def send_transaction(web3, transaction, private_key):
    try:
        signed_tx = web3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt
    except Exception as e:
        print(f"Error sending transaction: {e}")
        return None

def predict_price_movement(private_key):
    web3 = config.web3
    proxy_contract = web3.eth.contract(address=PROXY_CONTRACT_ADDRESS, abi=PROXY_ABI)
    implementation_contract = web3.eth.contract(address=IMPLEMENTATION_CONTRACT_ADDRESS, abi=IMPLEMENTATION_ABI)
    account = web3.eth.account.from_key(private_key)
    
    receipts = []

    for _ in range(config.retry_attempts):
        try:
            nonce = web3.eth.get_transaction_count(account.address)
            break
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}. Retrying in {config.retry_delay} seconds...")
            time.sleep(config.retry_delay)
    else:
        print("Max retries exceeded. Exiting...")
        return receipts

    for pair_index in range(7):  # От 0 до 7
        is_long = random.choice([True, False])
        data = implementation_contract.encodeABI(fn_name="predictPriceMovement", args=[pair_index, is_long])
        
        tx = {
            'to': PROXY_CONTRACT_ADDRESS,
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'data': data,
            'gas': config.gas_limit,
            'gasPrice': config.gas_price
        }
        
        receipt = send_transaction(web3, tx, private_key)
        receipts.append(receipt)
        time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    
    return receipts
