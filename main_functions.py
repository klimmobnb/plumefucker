from modules.file_reader import get_wallet_address
from modules.api_interaction import request_faucet
from modules.contract_interaction import interact_with_proxy_contract
from modules.swap_interaction import swap_tokens
from modules.stake_interaction import stake_tokens
from modules.check_in_interaction import check_in
from modules.prediction_interaction import predict_price_movement
from modules.rwa_interaction import create_rwa_token
from modules.solidviolet_interaction import solidviolet_swap
from config import STRICT_ORDER_MODULES, RANDOM_ORDER_MODULES

import time
import random
import config

def execute_module(keys_and_proxies, module_function, include_proxy=False):
    for key_and_proxy in keys_and_proxies:
        private_key = key_and_proxy[0]
        wallet_address = get_wallet_address(private_key)
        try:
            if include_proxy:
                module_function(private_key, wallet_address, key_and_proxy)
            else:
                module_function(private_key, wallet_address)
        except Exception as e:
            error_message = str(e)
            if "insufficient funds for gas * price + value" in error_message:
                print(f"Skipping wallet {wallet_address} due to insufficient funds.")
            else:
                print(f"Error executing module for wallet {wallet_address}: {e}")
        time.sleep(random.randint(config.wallet_delay_min, config.wallet_delay_max))

def run_faucet_module(private_key, wallet_address, key_and_proxy):
    try:
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
    except Exception as e:
        error_message = str(e)
        if "insufficient funds for gas * price + value" in error_message:
            print(f"Skipping wallet {wallet_address} due to insufficient funds.")
        else:
            print(f"Error in faucet module for wallet {wallet_address}: {e}")

def run_swap_module(private_key, wallet_address):
    try:
        receipt = swap_tokens(private_key)
        print(f"Wallet: {wallet_address}")
        if receipt:
            if receipt['status'] == 1:
                print(f"Swap: Transaction successful. Hash: {receipt['transactionHash'].hex()}")
            else:
                print(f"Swap: Transaction failed. Hash: {receipt['transactionHash'].hex()}")
    except Exception as e:
        error_message = str(e)
        if "insufficient funds for gas * price + value" in error_message:
            print(f"Skipping wallet {wallet_address} due to insufficient funds.")
        else:
            print(f"Error in swap module for wallet {wallet_address}: {e}")

def run_stake_module(private_key, wallet_address):
    try:
        token_address = '0x5c1409a46cD113b3A667Db6dF0a8D7bE37ed3BB3'  # Адрес токена для стейкинга
        receipt = stake_tokens(private_key, token_address)
        print(f"Wallet: {wallet_address}")
        if receipt is not None and receipt.get('status') == 1:
            print(f"Staking: Transaction successful. Hash: {receipt['transactionHash'].hex()}")
        else:
            print(f"Staking: Transaction failed. Receipt: {receipt}")
    except Exception as e:
        error_message = str(e)
        if "insufficient funds for gas * price + value" in error_message:
            print(f"Skipping wallet {wallet_address} due to insufficient funds.")
        else:
            print(f"Error in stake module for wallet {wallet_address}: {e}")

def run_check_in_module(private_key, wallet_address):
    try:
        receipt = check_in(private_key)
        print(f"Wallet: {wallet_address}")
        if receipt['status'] == 1:
            print(f"Check-in: Transaction successful. Hash: {receipt['transactionHash'].hex()}")
        else:
            print(f"Check-in: Transaction failed. Hash: {receipt['transactionHash'].hex()}")
    except Exception as e:
        error_message = str(e)
        if "insufficient funds for gas * price + value" in error_message:
            print(f"Skipping wallet {wallet_address} due to insufficient funds.")
        else:
            print(f"Error in check-in module for wallet {wallet_address}: {e}")

def run_prediction_module(private_key, wallet_address):
    try:
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
    except Exception as e:
        error_message = str(e)
        if "insufficient funds for gas * price + value" in error_message:
            print(f"Skipping wallet {wallet_address} due to insufficient funds.")
        else:
            print(f"Error in prediction module for wallet {wallet_address}: {e}")

def run_rwa_module(private_key, wallet_address):
    try:
        receipt = create_rwa_token(private_key)
        print(f"Wallet: {wallet_address}")
        if receipt['status'] == 1:
            print(f"RWA Token Creation: Transaction successful. Hash: {receipt['transactionHash'].hex()}")
        else:
            print(f"RWA Token Creation: Transaction failed. Hash: {receipt['transactionHash'].hex()}")
    except Exception as e:
        error_message = str(e)
        if "insufficient funds for gas * price + value" in error_message:
            print(f"Skipping wallet {wallet_address} due to insufficient funds.")
        else:
            print(f"Error in rwa module for wallet {wallet_address}: {e}")

def run_solidviolet_module(private_key, wallet_address):
    try:
        receipt = solidviolet_swap(private_key, wallet_address)
        print(f"Wallet: {wallet_address}")
        if receipt:
            if receipt['status'] == 1:
                print(f"SolidViolet: Transaction successful. Hash: {receipt['transactionHash'].hex()}")
            else:
                print(f"SolidViolet: Transaction failed. Hash: {receipt['transactionHash'].hex()}")
    except Exception as e:
        error_message = str(e)
        if "insufficient funds for gas * price + value" in error_message:
            print(f"Skipping wallet {wallet_address} due to insufficient funds.")
        else:
            print(f"Error in solidviolet module for wallet {wallet_address}: {e}")

def execute_custom_route(keys_and_proxies, include_proxy=False):
    for key_and_proxy in keys_and_proxies:
        private_key = key_and_proxy[0]
        wallet_address = get_wallet_address(private_key)
        
        # Выполнение модулей в строгом порядке
        for module_name, times in STRICT_ORDER_MODULES:
            for _ in range(times):
                try:
                    execute_module_by_name(module_name, private_key, wallet_address, key_and_proxy)
                    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
                except Exception as e:
                    print(f"Error executing {module_name} for wallet {wallet_address}: {e}")

        # Выполнение модулей в случайном порядке
        random.shuffle(RANDOM_ORDER_MODULES)
        for module_name, times in RANDOM_ORDER_MODULES:
            for _ in range(times):
                try:
                    execute_module_by_name(module_name, private_key, wallet_address, key_and_proxy)
                    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
                except Exception as e:
                    print(f"Error executing {module_name} for wallet {wallet_address}: {e}")

        time.sleep(random.randint(config.module_delay_min, config.module_delay_max))

def execute_module_by_name(module_name, private_key, wallet_address, key_and_proxy):
    try:
        if module_name == "faucet":
            run_faucet_module(private_key, wallet_address, key_and_proxy)
        elif module_name == "swap":
            run_swap_module(private_key, wallet_address)
        elif module_name == "stake":
            run_stake_module(private_key, wallet_address)
        elif module_name == "check_in":
            run_check_in_module(private_key, wallet_address)
        elif module_name == "prediction":
            run_prediction_module(private_key, wallet_address)
        elif module_name == "rwa":
            run_rwa_module(private_key, wallet_address)
        elif module_name == "solidviolet":
            run_solidviolet_module(private_key, wallet_address) 
    except Exception as e:
        error_message = str(e)
        if "insufficient funds for gas * price + value" in error_message:
            print(f"Skipping wallet {wallet_address} due to insufficient funds.")
        else:
            print(f"Error in module {module_name} for wallet {wallet_address}: {e}")
