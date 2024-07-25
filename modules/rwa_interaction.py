import random
import string
from web3 import Web3
import config

# Информация о прокси контракте и контракте реализации
PROXY_CONTRACT_ADDRESS = '0x485D972889Ee8fd0512403E32eE94dE5c7a5DC7b'
IMPLEMENTATION_CONTRACT_ADDRESS = '0xe1F9e3D1293f92c1dF87aeC9258C5EE68ebF6087'

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
                "internalType": "string",
                "name": "name",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "symbol",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "description",
                "type": "string"
            },
            {
                "internalType": "uint256",
                "name": "rwaType",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "image",
                "type": "string"
            }
        ],
        "name": "createToken",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

RWA_IMAGES = {
    0: "https://miles.plumenetwork.xyz/images/arc/art.webp",
    1: "https://miles.plumenetwork.xyz/images/arc/collectible-cards.webp",
    2: "https://miles.plumenetwork.xyz/images/arc/farming.webp",
    3: "https://miles.plumenetwork.xyz/images/arc/investment-alcohol.webp",
    4: "https://miles.plumenetwork.xyz/images/arc/investment-cigars.webp",
    5: "https://miles.plumenetwork.xyz/images/arc/investment-watch.webp",
    6: "https://miles.plumenetwork.xyz/images/arc/rare-sneakers.webp",
    7: "https://miles.plumenetwork.xyz/images/arc/real-estate.webp",
    8: "https://miles.plumenetwork.xyz/images/arc/solar-energy.webp",
    9: "https://miles.plumenetwork.xyz/images/arc/tokenized-gpus.webp",
}

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def create_rwa_token(private_key):
    web3 = config.web3
    account = web3.eth.account.from_key(private_key)

    name = generate_random_string(random.randint(5, 10))
    symbol = "ITEM"
    description = generate_random_string(random.randint(5, 10))
    rwa_type = random.randint(0, 9)
    image = RWA_IMAGES[rwa_type]

    implementation_contract = web3.eth.contract(address=IMPLEMENTATION_CONTRACT_ADDRESS, abi=IMPLEMENTATION_ABI)
    data = implementation_contract.encodeABI(fn_name="createToken", args=[name, symbol, description, rwa_type, image])

    proxy_contract = web3.eth.contract(address=PROXY_CONTRACT_ADDRESS, abi=PROXY_ABI)
    nonce = web3.eth.get_transaction_count(account.address)

    transaction = {
        'to': PROXY_CONTRACT_ADDRESS,
        'from': account.address,
        'data': data,
        'gas': config.gas_limit,
        'gasPrice': config.gas_price,
        'nonce': nonce
    }

    signed_tx = web3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt
