import requests
from web3 import Web3
import time
import config
import random

# Конфигурация
RPC = config.RPC
BLOCKSCOUT_API_URL = 'https://testnet-explorer.plumenetwork.xyz/api'
web3 = Web3(Web3.HTTPProvider(RPC))

# Адреса контрактов
MINT_CONTRACT_ADDRESS = config.MINT_CONTRACT_ADDRESS
TOKEN_CONTRACT_ADDRESS = '0x763Ccc2Cb06Eb8932208C5714ff5c010894Ac98d'
PROXY_CONTRACT_ADDRESS = '0xA4E9ddAD862A1B8b5F8e3d75a3AAd4C158E0faaB'
IMPLEMENTATION_CONTRACT_ADDRESS = '0x88EccD1fB3bd79902731aC1f37748c8540426Fb0'

# ABI контрактов
MINT_ABI = [
    {
        "inputs": [],
        "name": "mintAICK",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

TOKEN_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

PROXY_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "address", "name": "previousAdmin", "type": "address"},
            {"indexed": False, "internalType": "address", "name": "newAdmin", "type": "address"}
        ],
        "name": "AdminChanged",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "beacon", "type": "address"}
        ],
        "name": "BeaconUpgraded",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "implementation", "type": "address"}
        ],
        "name": "Upgraded",
        "type": "event"
    },
    {
        "stateMutability": "payable",
        "type": "fallback"
    },
    {
        "stateMutability": "payable",
        "type": "receive"
    }
]

IMPLEMENTATION_ABI = [
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "sellBond",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

def fetch_token_id_from_receipt(receipt):
    try:
        for log in receipt['logs']:
            if len(log['topics']) == 4:
                token_id_hex = log['topics'][3].hex()
                token_id = int(token_id_hex, 16)
                print(f"Token ID: {token_id}")
                return token_id
        print("TokenId not found in transaction receipt")
        return None
    except Exception as e:
        print(f"Error fetching tokenId from receipt: {e}")
        return None

def mint_and_transfer_nft(private_key, wallet_address):
    try:
        mint_contract = web3.eth.contract(address=MINT_CONTRACT_ADDRESS, abi=MINT_ABI)
        token_contract = web3.eth.contract(address=TOKEN_CONTRACT_ADDRESS, abi=TOKEN_ABI)
        proxy_contract = web3.eth.contract(address=PROXY_CONTRACT_ADDRESS, abi=IMPLEMENTATION_ABI)

        # Минтим токен
        nonce = web3.eth.get_transaction_count(wallet_address)
        tx = mint_contract.functions.mintAICK().build_transaction({
            'from': wallet_address,
            'gas': config.gas_limit,
            'gasPrice': config.gas_price,
            'nonce': nonce,
        })
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        time.sleep(90)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status != 1:
            print(f"Minting NFT failed for wallet {wallet_address}")
            return
        print(f"Minting NFT: Transaction successful. Hash: {tx_hash.hex()}")
        token_id = fetch_token_id_from_receipt(receipt)
        if not token_id:
            print(f"TokenId not found for wallet {wallet_address}")
            return

        # Добавляем задержку
        time.sleep(random.randint(config.module_delay_min, config.module_delay_max))

        # Одобряем прокси контракту
        nonce = web3.eth.get_transaction_count(wallet_address)
        approve_tx = token_contract.functions.approve(PROXY_CONTRACT_ADDRESS, token_id).build_transaction({
            'from': wallet_address,
            'gas': config.gas_limit,
            'gasPrice': config.gas_price,
            'nonce': nonce,
        })
        signed_approve_tx = web3.eth.account.sign_transaction(approve_tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_approve_tx.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status != 1:
            print(f"Approval for proxy contract failed for wallet {wallet_address}")
            return
        print(f"Approval for proxy contract: Transaction successful. Hash: {tx_hash.hex()}")

        # Добавляем задержку
        time.sleep(random.randint(config.module_delay_min, config.module_delay_max))

        # Продаем токен через прокси контракт
        nonce = web3.eth.get_transaction_count(wallet_address)
        sell_tx = proxy_contract.functions.sellBond(token_id).build_transaction({
            'from': wallet_address,
            'gas': config.gas_limit,
            'gasPrice': config.gas_price,
            'nonce': nonce,
        })
        signed_sell_tx = web3.eth.account.sign_transaction(sell_tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_sell_tx.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status != 1:
            print(f"Selling bond failed for wallet {wallet_address}")
            return
        print(f"Selling bond: Transaction successful. Hash: {tx_hash.hex()}")
    except Exception as e:
        print(f"Error in kuma module for wallet {wallet_address}: {e}")
