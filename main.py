from modules.file_reader import get_keys_and_proxies
from modules.ascii_art import display_ascii_art
from modules.main_functions import execute_module, run_faucet_module, run_swap_module, run_stake_module, run_check_in_module, run_all_modules_for_key, run_faucet_swap_stake_for_key, run_prediction_module
import random
import config

def main_menu():
    display_ascii_art()
    print("Plumefucker by Klimmo for Doubletop. Dickpicks in DM, donations here 0xd22e6ea4b557db527077f3341a3c6df90c4e6c03")
    print("Выберите модуль для запуска:")
    print("1. Запустить все модули")
    print("2. Faucet-Swap-Stake-Prediction Route")
    print("3. Faucet Module")
    print("4. Swap Module")
    print("5. Stake Module")
    print("6. Check-in Module")
    print("7. Prediction Module")
    print("8. Выйти")
    choice = input("Введите номер опции: ")

    file_path = 'accounts_data.xlsx'
    keys_and_proxies = get_keys_and_proxies(file_path)
    
    if not keys_and_proxies:
        print("Error: No valid keys and proxies found in file.")
        return

    random.shuffle(keys_and_proxies)

    if choice == '1':
        execute_module(keys_and_proxies, run_all_modules_for_key, include_proxy=True)
    elif choice == '2':
        execute_module(keys_and_proxies, run_faucet_swap_stake_for_key, include_proxy=True)
    elif choice == '3':
        execute_module(keys_and_proxies, run_faucet_module, include_proxy=True)
    elif choice == '4':
        execute_module(keys_and_proxies, run_swap_module) 
    elif choice == '5':
        execute_module(keys_and_proxies, run_stake_module)
    elif choice == '6':
        execute_module(keys_and_proxies, run_check_in_module)
    elif choice == '7':
        execute_module(keys_and_proxies, run_prediction_module)
    elif choice == '8':
        print("Выход...")
        return
    else:
        print("Неверный выбор. Пожалуйста, попробуйте снова.")
    
    main_menu()

if __name__ == "__main__":
    main_menu()
