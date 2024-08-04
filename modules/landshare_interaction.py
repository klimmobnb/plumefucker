from web3 import Web3
import config
import time
import random

# Адреса контрактов
GNUSD_CONTRACT_ADDRESS = Web3.to_checksum_address('0x5c1409a46cD113b3A667Db6dF0a8D7bE37ed3BB3')
SWAP_CONTRACT_ADDRESS = Web3.to_checksum_address('0xd2AadE12760d5e176F93C8F1C6Ae10667c8FCa8b')
LAND_CONTRACT_ADDRESS = Web3.to_checksum_address('0x45934E0253955dE498320D67c0346793be44BEC0')
STAKING_CONTRACT_ADDRESS = Web3.to_checksum_address('0x5374cf69c5610950526c668a7b540df6686531b4')

# ABI контрактов
GNUSD_ABI = [
    {
        "constant": False,
        "inputs": [
            {"name": "_spender", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    }
]

SWAP_ABI = [
    {"inputs": [{"internalType": "address", "name": "_gnUSD", "type": "address"}, {"internalType": "address", "name": "_LAND", "type": "address"}], "stateMutability": "nonpayable", "type": "constructor"},
    {"inputs": [], "name": "swap", "outputs": [], "stateMutability": "nonpayable", "type": "function"}
]

LAND_ABI = [
    {"constant": False, "inputs": [{"name": "_spender", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "approve", "outputs": [{"name": "", "type": "bool"}], "type": "function"}
]

STAKING_ABI = [
    {"inputs": [{"internalType": "uint256", "name": "_pid", "type": "uint256"}, {"internalType": "uint256", "name": "_amount", "type": "uint256"}], "name": "deposit", "outputs": [], "stateMutability": "nonpayable", "type": "function"}
]

def approve_gnusd(private_key, wallet_address):
    web3 = Web3(Web3.HTTPProvider(config.RPC))
    gnusd_contract = web3.eth.contract(address=GNUSD_CONTRACT_ADDRESS, abi=GNUSD_ABI)
    nonce = web3.eth.get_transaction_count(wallet_address)
    approve_tx = gnusd_contract.functions.approve(SWAP_CONTRACT_ADDRESS, web3.to_wei(1000, 'ether')).build_transaction({
        'from': wallet_address,
        'gas': config.gas_limit,
        'gasPrice': config.gas_price,
        'nonce': nonce,
    })
    signed_approve_tx = web3.eth.account.sign_transaction(approve_tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_approve_tx.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    if receipt.status != 1:
        print(f"Approval for gnUSD failed for wallet {wallet_address}")
        return None
    print(f"Approval for gnUSD: Transaction successful. Hash: {tx_hash.hex()}")
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    return receipt

def swap_gnusd(private_key, wallet_address):
    web3 = Web3(Web3.HTTPProvider(config.RPC))
    swap_contract = web3.eth.contract(address=SWAP_CONTRACT_ADDRESS, abi=SWAP_ABI)
    nonce = web3.eth.get_transaction_count(wallet_address)
    swap_tx = swap_contract.functions.swap().build_transaction({
        'from': wallet_address,
        'gas': config.gas_limit,
        'gasPrice': config.gas_price,
        'nonce': nonce,
    })
    signed_swap_tx = web3.eth.account.sign_transaction(swap_tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_swap_tx.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    if receipt.status != 1:
        print(f"Swap failed for wallet {wallet_address}")
        return None
    print(f"Swap: Transaction successful. Hash: {tx_hash.hex()}")
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    return receipt

def approve_land(private_key, wallet_address):
    web3 = Web3(Web3.HTTPProvider(config.RPC))
    land_contract = web3.eth.contract(address=LAND_CONTRACT_ADDRESS, abi=LAND_ABI)
    nonce = web3.eth.get_transaction_count(wallet_address)
    approve_tx = land_contract.functions.approve(STAKING_CONTRACT_ADDRESS, web3.to_wei(100, 'ether')).build_transaction({
        'from': wallet_address,
        'gas': config.gas_limit,
        'gasPrice': config.gas_price,
        'nonce': nonce,
    })
    signed_approve_tx = web3.eth.account.sign_transaction(approve_tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_approve_tx.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    if receipt.status != 1:
        print(f"Approval for LAND failed for wallet {wallet_address}")
        return None
    print(f"Approval for LAND: Transaction successful. Hash: {tx_hash.hex()}")
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    return receipt

def stake_land(private_key, wallet_address):
    web3 = Web3(Web3.HTTPProvider(config.RPC))
    staking_contract = web3.eth.contract(address=STAKING_CONTRACT_ADDRESS, abi=STAKING_ABI)
    nonce = web3.eth.get_transaction_count(wallet_address)
    stake_tx = staking_contract.functions.deposit(0, web3.to_wei(0.1, 'ether')).build_transaction({
        'from': wallet_address,
        'gas': config.gas_limit,
        'gasPrice': config.gas_price,
        'nonce': nonce,
    })
    signed_stake_tx = web3.eth.account.sign_transaction(stake_tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_stake_tx.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    if receipt.status != 1:
        print(f"Staking failed for wallet {wallet_address}")
        return None
    print(f"Staking: Transaction successful. Hash: {tx_hash.hex()}")
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    return receipt

def landshare_interaction(private_key, wallet_address):
    try:
        # Сделать approve gnUSD
        approve_receipt = approve_gnusd(private_key, wallet_address)
        if not approve_receipt:
            return

        # Выполнить swap
        swap_receipt = swap_gnusd(private_key, wallet_address)
        if not swap_receipt:
            return

        # Сделать approve LAND
        approve_land_receipt = approve_land(private_key, wallet_address)
        if not approve_land_receipt:
            return

        # Выполнить стейкинг LAND
        stake_receipt = stake_land(private_key, wallet_address)
        if not stake_receipt:
            return
    except Exception as e:
        print(f"Error in landshare interaction for wallet {wallet_address}: {e}")

if __name__ == '__main__':
    private_key = 'your_private_key_here'
    wallet_address = 'your_wallet_address_here'
    landshare_interaction(private_key, wallet_address)
