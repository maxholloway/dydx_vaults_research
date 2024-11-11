from datetime import datetime
import json
import time
import requests

headers = {
  'Accept': 'application/json'
}
 
# For the deployment by DYDX token holders, use
base_url = 'https://indexer.dydx.trade/v4'

SUBACCOUNT_ID = 0 # same subaccount_id for all vaults

with open("../info/vault_addresses.json", "r") as f:
    vault_addresses = json.load(f)

for vault_info in vault_addresses:
    market_name = vault_info["market_name"]
    vault_addr = vault_info["vault_address"]

    cur_before_or_at_height = 1_000_000_000 # start dummy high
    fills_to_write_single_name = []
    while True:
        print(f"[{market_name}] querying w min height {cur_before_or_at_height}")
        r = requests.get(f'{base_url}/fills', params={
        'address': vault_addr,  'subaccountNumber': f"{SUBACCOUNT_ID}", 'createdBeforeOrAtHeight': cur_before_or_at_height
        }, headers = headers)

        r = r.json()

        if "fills" not in r:
            break
        fills = r["fills"]

        fills_to_write = []
        min_height = cur_before_or_at_height
        for fill in fills:
            fill_height = int(fill["createdAtHeight"])
            dt = datetime.strptime(fill["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ")

            # Convert the datetime object to epoch milliseconds
            epoch_milliseconds = int(dt.timestamp() * 1000)

            fill_to_write = {
                "fill_id": fill["id"],
                "side": fill["side"],
                "liquidity": fill["liquidity"],
                "fee": fill["fee"],
                "market": fill["market"],
                "price": fill["price"],
                "size": fill["size"],
                "fill_height": fill_height,
                "fill_ts": epoch_milliseconds,
            }

            fills_to_write.append(fill_to_write)
            
            #  print(f"fh: {fill_height}")
            if fill_height < min_height:
                min_height = fill_height
        
        for fill in fills_to_write:
            if fill not in fills_to_write_single_name:
                fills_to_write_single_name.append(fill)

        if min_height == cur_before_or_at_height:
            print("brk", min_height)
            break

        cur_before_or_at_height = min_height

        # print(json.dumps(fills_to_write, indent=4))
        time.sleep(0.2)
    
    fills_to_write_single_name = list(sorted(fills_to_write_single_name, key=lambda x: x["fill_height"]))
    
    with open(f"../data/fill_data/{market_name}.json", "w") as f:
        json.dump(fills_to_write_single_name, f, indent=4)
   
    
