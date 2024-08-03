import random
from decimal import Decimal, getcontext
from web3 import Web3
import config
from modules.file_reader import get_keys_and_proxies

# Установление точности для операций с Decimal
getcontext().prec = 18

# Функция для конвертации эфира в доллары
def eth_to_usd(eth_amount, eth_usd_rate):
    usd_amount = eth_amount * eth_usd_rate
    return usd_amount

# Функция для конвертации долларов в токены (на примере 1,000,000 единиц токенов на 1 доллар)
def usd_to_tokens(usd_amount):
    tokens = int(usd_amount * 1000000)
    return tokens

# ABI вашего контракта
abi = [
    {
        "inputs": [
            {
                "components": [
                    {
                        "components": [
                            {"internalType": "address", "name": "swapper", "type": "address"},
                            {"internalType": "address", "name": "settler", "type": "address"},
                            {"internalType": "address", "name": "tokenIn", "type": "address"},
                            {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
                            {"internalType": "address", "name": "tokenOut", "type": "address"},
                            {"internalType": "uint256", "name": "minAmountOut", "type": "uint256"},
                            {"internalType": "uint256", "name": "expiry", "type": "uint256"},
                            {"internalType": "uint256", "name": "salt", "type": "uint256"}
                        ],
                        "internalType": "struct OrderParameters",
                        "name": "parameters",
                        "type": "tuple"
                    },
                    {
                        "components": [
                            {"internalType": "address", "name": "target", "type": "address"},
                            {"internalType": "bytes", "name": "data", "type": "bytes"},
                            {"internalType": "uint256", "name": "value", "type": "uint256"}
                        ],
                        "internalType": "struct FunctionCallData[]",
                        "name": "calls",
                        "type": "tuple[]"
                    }
                ],
                "internalType": "struct OrderFill",
                "name": "orderFill",
                "type": "tuple"
            }
        ],
        "name": "executeSwap",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }
]

# Адрес контракта (с проверкой EIP-55 checksum)
contract_address = Web3.to_checksum_address('0x06107C39D3Fd57a059Bc4Abae09f3b2b3d75D64E')

# Создание объекта контракта
contract = config.web3.eth.contract(address=contract_address, abi=abi)

def solidviolet_swap(private_key, wallet_address):
    account = config.web3.eth.account.from_key(private_key)
    swapper_address = Web3.to_checksum_address(account.address)

    # Получение баланса кошелька
    balance_wei = config.web3.eth.get_balance(swapper_address)

    # Процент от баланса для использования (например, 3%)
    percent_to_use = 3  # Укажите процент
    eth_amount = Web3.from_wei(balance_wei * percent_to_use / 100, 'ether')

    # Преобразование значения eth_amount в Decimal
    eth_amount = Decimal(eth_amount)

    # Параметры конвертации
    eth_usd_rate = Decimal('3153.40')  # Текущий курс эфира (можно получить из API или другого источника)

    # Конвертация суммы в доллары
    usd_amount = eth_to_usd(eth_amount, eth_usd_rate)

    # Конвертация суммы в токены (умножена на 1,000,000)
    tokens_amount = usd_to_tokens(usd_amount)

    # Генерация случайного salt
    salt = random.randint(0, 100)

    # Данные для свапа с динамическим amountIn и minAmountOut
    order_parameters = {
        'swapper': swapper_address,
        'settler': Web3.to_checksum_address('0x06107C39D3Fd57a059Bc4Abae09f3b2b3d75D64E'),
        'tokenIn': Web3.to_checksum_address('0x0000000000000000000000000000000000000000'),
        'amountIn': int(balance_wei * percent_to_use / 100),  # Используем процент от баланса
        'tokenOut': Web3.to_checksum_address('0x4194dddfb5938293621e78dd72e9bb22e59515d0'),
        'minAmountOut': tokens_amount,  # Динамическое значение
        'expiry': 0,
        'salt': salt
    }

    # Динамическое формирование значений 'data' в вызовах функций
    function_calls = [
        {
            'target': Web3.to_checksum_address('0xe76fda9882510850439cba890960ced1d1dc195e'),
            'data': '0xd0e30db0',  # Используйте соответствующие байты для функции
            'value': int(balance_wei * percent_to_use / 100)
        },
        {
            'target': Web3.to_checksum_address('0xe76fda9882510850439cba890960ced1d1dc195e'),
            'data': f'0xa9059cbb0000000000000000000000004181803232280371e02a875f51515be57b215231{hex(int(balance_wei * percent_to_use / 100))[2:].zfill(64)}',
            'value': 0
        },
        {
            'target': Web3.to_checksum_address('0x4194dddfb5938293621e78dd72e9bb22e59515d0'),
            'data': f'0x40c10f1900000000000000000000000006107c39D3Fd57a059Bc4Abae09f3b2b3d75D64E{hex(tokens_amount)[2:].zfill(64)}',
            'value': 0
        }
    ]

    # Подготовка транзакции
    transaction = contract.functions.executeSwap(
        {
            'parameters': order_parameters,
            'calls': function_calls
        }
    ).build_transaction({
        'from': swapper_address,
        'nonce': config.web3.eth.get_transaction_count(swapper_address),
        'value': int(balance_wei * percent_to_use / 100),
        'gas': config.gas_limit,
        'gasPrice': config.gas_price
    })

    # Подписание транзакции
    signed_txn = config.web3.eth.account.sign_transaction(transaction, private_key=private_key)

    # Отправка транзакции
    tx_hash = config.web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    receipt = config.web3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt

def main():
    file_path = 'accounts_data.xlsx'
    keys_and_proxies = get_keys_and_proxies(file_path)

    if not keys_and_proxies:
        print("Ошибка: не найдены действительные ключи и прокси в файле.")
        return

    for private_key, login, password, ip, port in keys_and_proxies:
        wallet_address = config.web3.eth.account.from_key(private_key).address
        receipt = solidviolet_swap(private_key, wallet_address)
        print(f"Wallet: {wallet_address}")
        if receipt:
            if receipt['status'] == 1:
                print(f"SolidViolet: Transaction successful. Hash: {receipt['transactionHash'].hex()}")
            else:
                print(f"SolidViolet: Transaction failed. Hash: {receipt['transactionHash'].hex()}")

if __name__ == "__main__":
    main()
