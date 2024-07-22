from modules.file_reader import get_keys_and_proxies, get_wallet_address
from modules.api_interaction import request_faucet
from modules.contract_interaction import interact_with_proxy_contract
from modules.swap_interaction import swap_tokens
from modules.stake_interaction import stake_tokens
from modules.check_in_interaction import check_in
from modules.ascii_art import display_ascii_art
import time
import random
import config

def get_random_key_and_proxy(keys_and_proxies):
    return random.choice(keys_and_proxies)

def run_faucet_module(private_key, wallet_address, key_and_proxy):
    # Запрос для токена ETH
    salt, signature = request_faucet(wallet_address, key_and_proxy, token="ETH")
    receipt = interact_with_proxy_contract(private_key, salt, signature, token="ETH")
    print(f"Wallet: {wallet_address}")
    if receipt['status'] == 1:
        print(f"ETH Faucet: Transaction successful. Hash: {receipt.transactionHash.hex()}")
    else:
        print(f"ETH Faucet: Transaction failed. Hash: {receipt.transactionHash.hex()}")

    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))

    # Запрос для токена GOON
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

def run_all_modules_for_key(private_key, wallet_address, key_and_proxy):
    run_faucet_module(private_key, wallet_address, key_and_proxy)
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    run_swap_module(private_key, wallet_address)
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    run_stake_module(private_key, wallet_address)
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    run_check_in_module(private_key, wallet_address)

def run_faucet_swap_stake_for_key(private_key, wallet_address, key_and_proxy):
    run_faucet_module(private_key, wallet_address, key_and_proxy)
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    run_swap_module(private_key, wallet_address)
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    run_stake_module(private_key, wallet_address)

def main_menu():
    display_ascii_art()
    print("Plumefucker by Klimmo for Doubletop. Dickpicks in DM, donations here 0xd22e6ea4b557db527077f3341a3c6df90c4e6c03")
    print("Выберите модуль для запуска:")
    print("1. Faucet Module")
    print("2. Swap Module")
    print("3. Stake Module")
    print("4. Check-in Module")
    print("5. Запустить все модули")
    print("6. Faucet-Swap-Stake Route")
    print("7. Выйти")
    choice = input("Введите номер опции: ")

    file_path = 'accounts_data.xlsx'
    keys_and_proxies = get_keys_and_proxies(file_path)
    
    if not keys_and_proxies:
        print("Error: No valid keys and proxies found in file.")
        return

    if choice == '1':
        for key_and_proxy in keys_and_proxies:
            private_key = key_and_proxy[0]
            wallet_address = get_wallet_address(private_key)
            run_faucet_module(private_key, wallet_address, key_and_proxy)
            time.sleep(random.randint(config.wallet_delay_min, config.wallet_delay_max))
    elif choice == '2':
        for key_and_proxy in keys_and_proxies:
            private_key = key_and_proxy[0]
            wallet_address = get_wallet_address(private_key)
            run_swap_module(private_key, wallet_address)
            time.sleep(random.randint(config.wallet_delay_min, config.wallet_delay_max))
    elif choice == '3':
        for key_and_proxy in keys_and_proxies:
            private_key = key_and_proxy[0]
            wallet_address = get_wallet_address(private_key)
            run_stake_module(private_key, wallet_address)
            time.sleep(random.randint(config.wallet_delay_min, config.wallet_delay_max))
    elif choice == '4':
        for key_and_proxy in keys_and_proxies:
            private_key = key_and_proxy[0]
            wallet_address = get_wallet_address(private_key)
            run_check_in_module(private_key, wallet_address)
            time.sleep(random.randint(config.wallet_delay_min, config.wallet_delay_max))
    elif choice == '5':
        for key_and_proxy in keys_and_proxies:
            private_key = key_and_proxy[0]
            wallet_address = get_wallet_address(private_key)
            run_all_modules_for_key(private_key, wallet_address, key_and_proxy)
            time.sleep(random.randint(config.wallet_delay_min, config.wallet_delay_max))
    elif choice == '6':
        for key_and_proxy in keys_and_proxies:
            private_key = key_and_proxy[0]
            wallet_address = get_wallet_address(private_key)
            run_faucet_swap_stake_for_key(private_key, wallet_address, key_and_proxy)
            time.sleep(random.randint(config.wallet_delay_min, config.wallet_delay_max))
    elif choice == '7':
        print("Выход...")
        return
    else:
        print("Неверный выбор. Пожалуйста, попробуйте снова.")
    
    main_menu()

if __name__ == "__main__":
    main_menu()
