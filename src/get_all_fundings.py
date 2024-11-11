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

LIMIT = 1_000
for vault_info in vault_addresses:
    market_name = vault_info["market_name"]
    vault_addr = vault_info["vault_address"]

    fundings_to_write_single_name = []
    at_or_before = 1_000_000_000
    while True:
        print(f"[{market_name}] querying at or before {at_or_before}")
        r = requests.get(f'{base_url}/perpetualPositions', params={
        'address': vault_addr,  'subaccountNumber': f"{SUBACCOUNT_ID}", 'limit': LIMIT, 'createdBeforeOrAtHeight': at_or_before,
        }, headers = headers)

        r = r.json()

        if "positions" not in r:
            print("no pxns")
            break

        pxns = r["positions"]

        new_fundings_to_write_single_name = []
        for pxn in pxns:
            pxn_height = int(pxn["createdAtHeight"])
            dt = datetime.strptime(pxn["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ")

            # Convert the datetime object to epoch milliseconds
            epoch_milliseconds = int(dt.timestamp() * 1000)

            funding_to_write = {
                "vault_market": market_name,
                "pxn_total_funding": pxn["netFunding"],
                "pxn_height": pxn_height,
                "pxn_ts": epoch_milliseconds,
            }
            if funding_to_write not in fundings_to_write_single_name:
                new_fundings_to_write_single_name.append(funding_to_write)
            

            if pxn_height < at_or_before:
                at_or_before = pxn_height
        
        if len(new_fundings_to_write_single_name) == 0:
            break
        else:
            for funding_to_write in new_fundings_to_write_single_name:
                fundings_to_write_single_name.append(funding_to_write)


        time.sleep(0.2)
    
    fundings_to_write_single_name = list(sorted(fundings_to_write_single_name, key=lambda x: x["pxn_height"]))
    
    with open(f"../data/funding_data/{market_name}.json", "w") as f:
        json.dump(fundings_to_write_single_name, f, indent=4)
   
    
