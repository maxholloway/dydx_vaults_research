# dYdX Single-Name Vaults Research

*Max Holloway*

## Replicating the results


### Python environment
```bash
python3 -m venv venv && source venv/bin/activate && pip3 install -r requirements.txt
```

### Get perp market info
Necessary for joining the vault with the clob pair that it's quoting.
```bash
curl -X GET https://indexer.dydx.trade/v4/perpetualMarkets | python3 -m json.tool > info/market_info.json
```


### Get vaults info
```bash
TARGET_DIR="<fully/qualified/path/to/this/repo>/info/vaults.yml"
cd ~/dev/v4-chain/protocol
./build/dydxprotocold query vault list-vault --limit 1000 --node https://dydx-rpc.polkachu.com > $TARGET_DIR
cd -
```


### Parse vaults info and market name into json file
```bash
cd src && python3 parse_vault_addresses.py && cd -
```


### Run script to get all fills
```bash
cd src && python3 get_all_fills.py && cd -
```

### Run script to get all funding payments
```bash
cd src && python3 get_all_fundings.py && cd -
```

### [currently broken due to indexer bug] Run script to get all deposits
```bash
cd src && python3 get_all_deposits.py && cd -
```

### Run research notebook
Use jupyter notebook (e.g., I do so in VS Code), to open up `./analysis/overview.ipynb`. All of the cells should run.

