from secrets import token_hex
from web3 import Web3
from decimal import Decimal, ROUND_DOWN

# информация о прокси контракте и контракте реализации
PROXY_CONTRACT_ADDRESS = '0xA34420e04DE6B34F8680EE87740B379103DC69f6'
IMPLEMENTATION_CONTRACT_ADDRESS = '0x7b0a6d394bBD09Faee9dD5Ff27407D4158d495D1'
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
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "stake",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_spender", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"name": "success", "type": "bool"}],
        "type": "function"
    }
]

def get_token_balance(web3, token_address, wallet_address):
    token_contract = web3.eth.contract(address=token_address, abi=ERC20_ABI)
    return token_contract.functions.balanceOf(wallet_address).call()

def approve_token(private_key, token_address, spender_address, amount):
    web3 = Web3(Web3.HTTPProvider('https://testnet-rpc.plumenetwork.xyz/http'))
    account = web3.eth.account.from_key(private_key)
    
    contract = web3.eth.contract(address=token_address, abi=ERC20_ABI)
    
    # Одобрение контракта на использование токенов
    nonce = web3.eth.get_transaction_count(account.address)
    approval_tx = contract.functions.approve(spender_address, amount).build_transaction({
        'chainId': 161221135,
        'gas': 500000,  # Увеличиваем лимит газа
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': nonce
    })
    signed_approval_tx = web3.eth.account.sign_transaction(approval_tx, private_key)
    approval_tx_hash = web3.eth.send_raw_transaction(signed_approval_tx.raw_transaction)
    approval_receipt = web3.eth.wait_for_transaction_receipt(approval_tx_hash)
    
    return approval_receipt

def round_balance(balance):
    # Превращаем баланс в строку и заменяем последние 17 цифр на нули
    balance_str = str(balance)
    rounded_balance_str = balance_str[:len(balance_str)-17] + '0' * 17
    return int(rounded_balance_str)

def stake_tokens(private_key, token_address):
    web3 = Web3(Web3.HTTPProvider('https://testnet-rpc.plumenetwork.xyz/http'))

    proxy_contract = web3.eth.contract(address=PROXY_CONTRACT_ADDRESS, abi=PROXY_ABI)
    implementation_contract = web3.eth.contract(address=IMPLEMENTATION_CONTRACT_ADDRESS, abi=IMPLEMENTATION_ABI)
    account = web3.eth.account.from_key(private_key)
    wallet_address = account.address
    
    # Получаем баланс токена
    balance = get_token_balance(web3, token_address, wallet_address)
    
    # Выводим текущий баланс токена
    print(f"Current token balance: {balance}")
    
    # Округляем баланс до ближайшего целого числа токенов
    rounded_balance = round_balance(balance)
    
    if rounded_balance <= 0:
        print("Insufficient balance to stake. Balance must be greater than 0.")
        return

    # Одобряем контракт для использования токенов
    approval_receipt = approve_token(private_key, token_address, PROXY_CONTRACT_ADDRESS, rounded_balance)
    if approval_receipt['status'] != 1:
        print(f"Approval failed. Transaction hash: {approval_receipt['transactionHash'].hex()}")
        return approval_receipt

    # Данные для вызова функции stake контракта реализации
    stake_data = implementation_contract.encodeABI(fn_name="stake", args=[rounded_balance])
    
    # Установка лимита газа и цены газа
    gas_limit = 700000
    gas_price = web3.to_wei('1', 'gwei')

    tx = {
        'to': PROXY_CONTRACT_ADDRESS,
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'data': stake_data,
        'gas': gas_limit,
        'gasPrice': gas_price
    }
    
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    return receipt
