from modules.file_reader import get_wallet_address
from modules.api_interaction import request_faucet
from modules.contract_interaction import interact_with_proxy_contract
from modules.swap_interaction import swap_tokens
from modules.stake_interaction import stake_tokens
from modules.check_in_interaction import check_in
from modules.prediction_interaction import predict_price_movement
import time
import random
import config

def run_faucet_module(private_key, wallet_address, key_and_proxy):
    salt, signature = request_faucet(wallet_address, key_and_proxy, token="ETH")
    receipt = interact_with_proxy_contract(private_key, salt, signature, token="ETH")
    print(f"Wallet: {wallet_address}")
    if receipt['status'] == 1:
        print(f"ETH Faucet: Transaction successful. Hash: {receipt.transactionHash.hex()}")
    else:
        print(f"ETH Faucet: Transaction failed. Hash: {receipt.transactionHash.hex()}")
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    salt, signature = request_faucet(wallet_address, key_and_proxy, token="GOON")
    receipt = interact_with_proxy_contract(private_key, salt, signature, token="GOON")
    print(f"Wallet: {wallet_address}")
    if receipt['status'] == 1:
        print(f"GOON Faucet: Transaction successful. Hash: {receipt.transactionHash.hex()}")
    else:
        print(f"GOON Faucet: Transaction failed. Hash: {receipt.transactionHash.hex()}")

def run_swap_module(private_key, wallet_address):
    receipt = swap_tokens(private_key)
    print(f"Wallet: {wallet_address}")
    if receipt:
        if receipt['status'] == 1:
            print(f"Swap: Transaction successful. Hash: {receipt['transactionHash'].hex()}")
        else:
            print(f"Swap: Transaction failed. Hash: {receipt['transactionHash'].hex()}")

def run_stake_module(private_key, wallet_address):
    token_address = '0x5c1409a46cD113b3A667Db6dF0a8D7bE37ed3BB3'  # Адрес токена для стейкинга
    receipt = stake_tokens(private_key, token_address)
    print(f"Wallet: {wallet_address}")
    if receipt['status'] == 1:
        print(f"Staking: Transaction successful. Hash: {receipt['transactionHash'].hex()}")
    else:
        print(f"Staking: Transaction failed. Hash: {receipt['transactionHash'].hex()}")

def run_check_in_module(private_key, wallet_address):
    receipt = check_in(private_key)
    print(f"Wallet: {wallet_address}")
    if receipt['status'] == 1:
        print(f"Check-in: Transaction successful. Hash: {receipt['transactionHash'].hex()}")
    else:
        print(f"Check-in: Transaction failed. Hash: {receipt['transactionHash'].hex()}")

def run_prediction_module(private_key, wallet_address):
    print(f"Running prediction module for {wallet_address}")
    receipts = predict_price_movement(private_key)
    print(f"Wallet: {wallet_address}")
    for receipt in receipts:
        if receipt:
            if receipt['status'] == 1:
                print(f"Prediction: Transaction successful. Hash: {receipt['transactionHash'].hex()}")
            else:
                print(f"Prediction: Transaction failed. Hash: {receipt['transactionHash'].hex()}")
        else:
            print(f"Prediction: No receipt returned for transaction.")

def run_all_modules_for_key(private_key, wallet_address, key_and_proxy):
    run_faucet_module(private_key, wallet_address, key_and_proxy)
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    run_swap_module(private_key, wallet_address)
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    run_stake_module(private_key, wallet_address)
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    run_check_in_module(private_key, wallet_address)
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    run_prediction_module(private_key, wallet_address)

def run_faucet_swap_stake_for_key(private_key, wallet_address, key_and_proxy):
    run_faucet_module(private_key, wallet_address, key_and_proxy)
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    run_swap_module(private_key, wallet_address)
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    run_stake_module(private_key, wallet_address)
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    run_prediction_module(private_key, wallet_address)

def execute_module(keys_and_proxies, module_function, include_proxy=False):
    for key_and_proxy in keys_and_proxies:
        private_key = key_and_proxy[0]
        wallet_address = get_wallet_address(private_key)
        if include_proxy:
            module_function(private_key, wallet_address, key_and_proxy)
        else:
            module_function(private_key, wallet_address)
        time.sleep(random.randint(config.wallet_delay_min, config.wallet_delay_max))
