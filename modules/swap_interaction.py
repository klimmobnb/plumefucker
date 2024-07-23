from web3 import Web3
import time

#  информация о контракте свапа и параметрах
SWAP_CONTRACT_ADDRESS = '0x4c722A53Cf9EB5373c655E1dD2dA95AcC10152D1'
SWAP_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "base", "type": "address"},
            {"internalType": "address", "name": "quote", "type": "address"},
            {"internalType": "uint256", "name": "poolIdx", "type": "uint256"},
            {"internalType": "bool", "name": "isBuy", "type": "bool"},
            {"internalType": "bool", "name": "inBaseQty", "type": "bool"},
            {"internalType": "uint128", "name": "qty", "type": "uint128"},
            {"internalType": "uint16", "name": "tip", "type": "uint16"},
            {"internalType": "uint128", "name": "limitPrice", "type": "uint128"},
            {"internalType": "uint128", "name": "minOut", "type": "uint128"},
            {"internalType": "uint8", "name": "reserveFlags", "type": "uint8"}
        ],
        "name": "swap",
        "outputs": [
            {"internalType": "int128", "name": "baseFlow", "type": "int128"},
            {"internalType": "int128", "name": "quoteFlow", "type": "int128"}
        ],
        "stateMutability": "payable",
        "type": "function"
    }
]

BASE = Web3.to_checksum_address('0x5c1409a46cd113b3a667db6df0a8d7be37ed3bb3')
QUOTE = Web3.to_checksum_address('0xba22114ec75f0d55c34a5e5a3cf384484ad9e733')
POOL_IDX = 36000
IS_BUY = False
IN_BASE_QTY = False
QTY = 100000000000000000  # Примерное количество токенов
TIP = 0
LIMIT_PRICE = 65537
MIN_OUT = 9690103065591420100  # Примерное минимальное количество выхода (корректировка на 1 ноль)
RESERVE_FLAGS = 0

def swap_tokens(private_key):
    web3 = Web3(Web3.HTTPProvider('https://testnet-rpc.plumenetwork.xyz/http'))

    swap_contract = web3.eth.contract(address=SWAP_CONTRACT_ADDRESS, abi=SWAP_ABI)
    account = web3.eth.account.from_key(private_key)
    
    # Установка лимита газа и цены газа
    gas_limit = 500000
    gas_price = web3.to_wei('1', 'gwei')  # Цена газа с запасом

    tx = swap_contract.functions.swap(BASE, QUOTE, POOL_IDX, IS_BUY, IN_BASE_QTY, QTY, TIP, LIMIT_PRICE, MIN_OUT, RESERVE_FLAGS).build_transaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': gas_limit,
        'gasPrice': gas_price
    })
    
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    return receipt
