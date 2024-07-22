import pandas as pd

def get_keys_and_proxies(file_path):
    df = pd.read_excel(file_path)
    keys_and_proxies = []
    
    for index, row in df.iterrows():
        try:
            proxy_info = row['Proxy']
            private_key = row['Private Key']
            login_password, ip_port = proxy_info.split('@')
            login, password = login_password.split(':')
            ip, port = ip_port.split(':')
            keys_and_proxies.append((private_key, login, password, ip, port))
        except Exception as e:
            print(f"Error processing row {index}: {e}")
    
    return keys_and_proxies

def get_wallet_address(private_key):
    from eth_account import Account
    account = Account.from_key(private_key)
    return account.address
