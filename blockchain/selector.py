import web3
import requests
import time
from collections import defaultdict


def get_bep20_transactions(filtered_address, start_block=0):
    time.sleep(5)
    return requests.get(
        "https://api.bscscan.com/api",
        params={
            "module": "account",
            # "action": "txlist",
            "address": filtered_address,
            "startblock": start_block,
            "endblock": 99999999,
            "page": 0,
            "offset": 100,
            "sort": "asc",
            # "apikey": "YourApiKeyToken",
            # ====================
            "action": "tokentx",
            # "contractaddress": "",
        },
    ).json()["result"]


address = "0x76de186cc58f75bb425e6072c8e3aafc3948080d"
valid_contract_addresses = {
    "0x55d398326f99059ff775485246999027b3197955",
    "0xe9e7cea3dedca5984780bafc599bd69add087d56",
}
smartwallet_addresses = {
    web3.Web3.to_checksum_address(a)
    for a in (
        "0x59e591E41A16f1A3591929ACefB289fa6797a608",
        "0x16CE75aEED8c2de0C884E3A7f5a8e0Ba0Aa8bb27",
        "0x2f773AD7893A2dD6c0D5eF30F3f7192FF27De358",
        "0x274a23896c8b6c0D20e760c6C8a10856b5aD3272",
        "0x2F0082Fc203424EC0815e7b3e2A3d9aB87c8b396",
        "0x321328CAcE9d8D295cDfa9a20c2dF26fA2B40F7C",
        "0xeaf046E492a176d0f8Be08784e432c8f88a99401",
        "0xB464a5f29F3b24bF87ae31E341667d3fc5831d25",
        "0x8D1DD6C10898E3B048E132A610B52D17C7D3FB5E",
        "0x48542D156D45A5CC6C235FEF08247354A87B18D1",
    )
}


transactions = get_bep20_transactions(address)
tx_srcs = defaultdict(lambda: defaultdict(int))
for t in transactions:
    if t["to"] == address and t["contractAddress"] in valid_contract_addresses:
        tx_srcs[t["contractAddress"]][web3.Web3.to_checksum_address(t["from"])] += int(
            t["value"]
        )

result = {}
for contract_address, contract_txs in tx_srcs.items():
    direct_payments = {
        a: contract_txs[a] for a in set(contract_txs.keys()) - smartwallet_addresses
    }
    selected_smartwallets = set(contract_txs.keys()).intersection(smartwallet_addresses)
    sw_bep20_txs = {sw: get_bep20_transactions(sw) for sw in selected_smartwallets}
    result[contract_address] = {
        web3.Web3.to_checksum_address(r["from"]): contract_txs[sw]
        for sw, txs in sw_bep20_txs.items()
        for r in txs
        if web3.Web3.to_checksum_address(r["to"]) == sw
    } | direct_payments
print(result)
