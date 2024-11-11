from datetime import datetime
import json
import time
from typing import Dict, List
import requests

headers = {
  'Accept': 'application/json'
}
 
# For the deployment by DYDX token holders, use
base_url = 'https://indexer.dydx.trade/v4'

DEPOSITOR_ADDRESS = "dydx1sln5f4plkajfnlslyw48waw2dvh3gk2qgjzvec"
SUBACCOUNT_ID = 0 # same subaccount_id for all vaults

with open("../info/vault_addresses.json", "r") as f:
    vault_addresses = json.load(f)

def find_vault_associated_market(vault_address: str):
    for vault_info in vault_addresses:
        if vault_info["vault_address"] == vault_address:
            return vault_info["market_name"]
    
    return None
    

LIMIT = 1_000
r = requests.get(f'{base_url}/transfers', params={
    'address': DEPOSITOR_ADDRESS,  'subaccountNumber': f"{SUBACCOUNT_ID}", 'limit': LIMIT,
}, headers = headers)

r = r.json()
transfers = r["transfers"]
if "transfers" not in r:
    assert False

transfers_to_write: Dict[str, List[Dict]] = {}
for transfer in transfers:
    recipient_address = transfer["recipient"]["address"]
    market_name = find_vault_associated_market(recipient_address)
    if market_name is None:
        print(f"market '{recipient_address}' is none")
        continue
    else:
        print(recipient_address)

    transfer_height = int(transfer["createdAtHeight"])
    
    # Convert the datetime object to epoch milliseconds
    dt = datetime.strptime(transfer["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
    epoch_milliseconds = int(dt.timestamp() * 1000)
    transfer_to_write = {
        "vault_market": market_name,
        "transfer_id": transfer["id"],
        "asset": transfer["symbol"],
        "type": "TRANSFER_IN" if transfer["type"] == "TRANSFER_OUT" else None,
        "amount": transfer["size"],
        "tx_hash": transfer["transactionHash"],
        "transfer_height": transfer_height,
        "transfer_ts": epoch_milliseconds,
    }

    if market_name not in transfers_to_write:
        transfers_to_write[market_name] = []
    
    transfers_to_write[market_name].append(transfer_to_write)


for (market_name, transfers_to_write_single_name) in transfers_to_write.items():
    transfers_to_write_single_name = list(sorted(transfers_to_write_single_name, key=lambda x: x["transfer_height"]))
    
    with open(f"../data/transfer_data/{market_name}.json", "w") as f:
        json.dump(transfers_to_write_single_name, f, indent=4)


# https://indexer.dydx.trade/v4/transfers?address=dydx1sln5f4plkajfnlslyw48waw2dvh3gk2qgjzvec&subaccountNumber=0&limit=1000

# for vault_info in vault_addresses:
#     market_name = vault_info["market_name"]
#     vault_addr = vault_info["vault_address"]


#     transfers_to_write_single_name = []
#     print(f"[{market_name}] querying")
#     r = requests.get(f'{base_url}/transfers', params={
#     'address': vault_addr,  'subaccountNumber': f"{SUBACCOUNT_ID}", 'limit': 100,
#     }, headers = headers)

#     r = r.json()

#     if "transfers" not in r:
#         break
#     transfers = r["transfers"]
#     assert len(transfers) < LIMIT, "Expected < {LIMIT} transfers per vault."


#     time.sleep(0.2)
    
#     transfers_to_write_single_name = list(sorted(transfers_to_write_single_name, key=lambda x: x["transfer_height"]))
    
#     with open(f"../data/transfer_data/{market_name}.json", "w") as f:
#         json.dump(transfers_to_write_single_name, f, indent=4)
   
    
