import json
import yaml

# Read the file content
with open('../info/vaults.yml', 'r') as file:
    data = yaml.safe_load(file)

with open('../info/market_info.json', 'r') as file:
    all_markets_info = json.load(file)["markets"]

def get_market_name(clob_pair_id: int) -> str:
    for (market_name, single_market_info) in all_markets_info.items():
        if int(single_market_info["clobPairId"]) == clob_pair_id:
            return market_name
    
    raise Exception(f"Market name not found for clob_pair_id '{clob_pair_id}'.")


# Extract owner and vault_id into a list
owner_vault_list = [
    {"vault_address": vault['subaccount_id']['owner'], "market_name": get_market_name(vault["vault_id"]["number"])}
    for vault in data['vaults']
]

with open("../info/vault_addresses.json", "w") as f:
    json.dump(owner_vault_list, f, indent=4)

# print(json.dumps(owner_vault_list, indent=4))
