from web3 import Web3
# Конфигурационный файл для настройки задержек между модулями и кошельками

#настройки RPC
RPC = 'https://testnet-rpc.plumenetwork.xyz/http'
web3 = Web3(Web3.HTTPProvider(RPC))

#настройки газа
gas_limit = 2000000
gas_price = web3.to_wei(3, 'gwei')

# Задержка между модулями в секундах (минимальная и максимальная)
module_delay_min = 10
module_delay_max = 120

# Задержка между использованием разных кошельков в секундах (минимальная и максимальная)
wallet_delay_min = 10
wallet_delay_max = 120

# Повторная отправка неудачных транзакций
retry_attempts = 5
retry_delay = 10


# Настройка маршрута модулей
# Доступные модули:
# "faucet" - Модуль крана
# "swap" - Модуль обмена
# "stake" - Модуль стейкинга
# "check_in" - Модуль чек-ина
# "prediction" - Модуль предсказания
# "rwa": - модуль RWA
# Пример:
# STRICT_ORDER_MODULES = [
#     ("faucet", 1),       # Запускает модуль крана один раз
#     ("swap", 1),         # Запускает модуль обмена один раз
#     ("stake", 1)         # Запускает модуль стейкинга один раз
# ]
# RANDOM_ORDER_MODULES = [
#     
#     ("check_in", 1),     # Запускает модуль регистрации один раз
#     ("prediction", 1)    # Запускает модуль предсказания один раз
#     ("rwa", 2)           # Запускает модуль RWA два раза
#     ("kuma", 1)           # Запускает модуль KUMA два раза
# ]

STRICT_ORDER_MODULES = [
    ("faucet", 1),
    ("swap", 1),
    ("stake", 1)
]

RANDOM_ORDER_MODULES = [
    #("check_in", 1),
    ("prediction", 1),
    ("rwa", 1),
    ("solidviolet", 1)
]