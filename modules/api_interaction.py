import requests
import json

def request_faucet(wallet_address, proxy, token):
    url = "https://faucet.plumenetwork.xyz/api/faucet"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "walletAddress": wallet_address,
        "token": token
    }
    
    proxy_url = f"http://{proxy[1]}:{proxy[2]}@{proxy[3]}:{proxy[4]}"
    proxies = {"http": proxy_url, "https": proxy_url}
    
    response = requests.post(url, headers=headers, data=json.dumps(payload), proxies=proxies)
    
    if response.status_code == 200 or response.status_code == 202:
        data = response.json()
        return data.get('salt'), data.get('signature')
    else:
        raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")
