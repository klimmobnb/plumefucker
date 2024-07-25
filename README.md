# Plumefucker

Plumefucker by Klimmo. Dickpicks in DM, donations here 0xd22e6ea4b557db527077f3341a3c6df90c4e6c03

## Описание

Этот скрипт позволяет взаимодействовать с различными смарт-контрактами на блокчейне, выполняя такие действия, как:
- Запрос токенов из крана (faucet)
- Обмен токенов (swap)
- Стейкинг токенов (stake)
- Чекин (check-in)
- Взаимодействие с рынком предсказаний (prediction)
- Создание NFT токенов  (RWA)

## Требования

- Python 3.10+
- Следующие пакеты Python:
  - web3==6.2.0
  - pandas==1.5.3
  - numpy==1.26.4
  - requests==2.31.1
  - openpyxl==3.0.10

## Установка

1. **Клонировать репозиторий**:
    ```bash
    git clone https://github.com/klimmobnb/plumefucker.git
    cd plumefucker
    ```

2. **Создать и активировать виртуальное окружение**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # В Windows используйте `venv\Scripts\activate`
    ```

3. **Установить необходимые пакеты**:
    ```bash
    pip install -r requirements.txt
    ```

## Конфигурация

1. **Данные аккаунтов**:
   - Подготовьте файл `accounts_data.xlsx` с вашими ключами и прокси. Скрипт будет считывать этот файл для получения необходимых ключей и адресов прокси.


  | Private Key                      | Proxy Address                      |
  |----------------------------------|------------------------------------|
  | YourPrivateKey1                  | username:password@proxyserver:port |
  | YourPrivateKey2                  | username:password@proxyserver:port |


2. **Настройка файла config.py**: 
  -Заполните файл `config.py` следующими параметрами:

    - `module_delay_min`: минимальная задержка между выполнением модулей (в секундах)
    - `module_delay_max`: максимальная задержка между выполнением модулей (в секундах)
    - `wallet_delay_min`: минимальная задержка между кошельками (в секундах)
    - `wallet_delay_max`: максимальная задержка между кошельками (в секундах)
    - `gas_limit`: лимит газа для транзакций
    - `gas_price`: цена газа для транзакций
    - `STRICT_ORDER_MODULES`: список модулей, которые будут выполняться в строгом порядке
    - `RANDOM_ORDER_MODULES`: список модулей, которые будут выполняться в случайном порядке

## Использование

Запустите скрипт и следуйте инструкциям меню для выбора модуля, который вы хотите выполнить.
