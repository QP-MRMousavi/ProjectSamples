import asyncio
import json
import time

import eth_utils
from eth_typing import HexStr
from hexbytes import HexBytes
from web3 import AsyncWeb3
from web3._utils.contracts import encode_transaction_data, prepare_transaction
from web3.contract.async_contract import AsyncContractFunction
from web3.exceptions import ContractLogicError, TransactionNotFound
from web3.middleware import async_geth_poa_middleware
from web3.types import TxReceipt, BlockData

ALCHEMY_API_KEY = "API KEY"
NETWORK = "polygon-mumbai"
PRIVATE_PROVIDER_URL = f"https://{NETWORK}.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
USDT_CONTRACT_ADDRESS = "0x78c731f4a5f01e8C6b826A6ba67c6574AE2DF2Dd"
with open("./smartwallet_abi.json") as fp:
    smartwallet_contract_abi = json.load(fp)
w3_public = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider("https://rpc-mumbai.maticvigil.com"))
w3_private = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(PRIVATE_PROVIDER_URL))
w3_public.middleware_onion.inject(
    async_geth_poa_middleware, layer=0
)  # Needed for BSC, Polygon and Georli
w3_private.middleware_onion.inject(async_geth_poa_middleware, layer=0)
account = w3_private.eth.account.from_key(
    "KEY"
)
smartwallet_contract_addresses = [
    "0x9894aea517Aa727FF408935cd642bc7e7F3029A6",
    "0x725C2332223E49DC70C5A35Ab05641E42A081e50",
    "0xB3Bb8b56ad11970EEc00D1F37A2C55d928983671",
    "0xa6D44194d3014B9F5628Af785B5c8C783325728d",
    "0x1c57f20Cf6402CB83B76a11d3c9a164142a3A21F",
    "0x57bA3e59474d2abA6cDc6Fe9155973AE9F27ec59",
    "0xC823BFe0b131d19E281c4E0D220D2085EAF9c591",
    "0x7eB3dbc028a242FcE23c48bB843f641ef8D502A2",
    "0xd46784c295025Eb8832C203D4dBB35e8E8d086fe",
    "0x8dC3830e16be8855fFd128125Ba942eb8fdAe482",
    "0x3A0Ac19A36FeB5DAF692F1EB11C990C51d025E99",
    "0xbB817aCb29BEd5f9dA64474eCB759ce27aC9e4B6",
]
smartwallet_contracts = {
    address: w3_public.eth.contract(address=address, abi=smartwallet_contract_abi)
    for address in smartwallet_contract_addresses
}
GAS_UNITS = 200_000


async def _run_for_one_second(lock, coro):
    async with lock:
        res, _ = await asyncio.gather(coro, asyncio.sleep(1))
        return res


async def simple_limiter(burst, coros):
    sem = asyncio.Semaphore(burst)
    return await asyncio.gather(*[_run_for_one_second(sem, c) for c in coros])


def create_raw_transaction(
    fn: AsyncContractFunction,
    chain_id: int,
    nonce: int,
    gas: int,
    max_priority_fee_per_gas_wei: int,
    max_fee_per_gas_wei: int,
) -> HexBytes:
    return fn.w3.eth.account.sign_transaction.sign_transaction(
        prepare_transaction(
            address=fn.address,
            w3=fn.w3,
            fn_identifier=fn.function_identifier,
            contract_abi=fn.contract_abi,
            fn_abi=fn.abi,
            fn_args=fn.args,
            fn_kwargs=fn.kwargs,
            transaction={
                "chainId": chain_id,
                "from": account.address,
                "nonce": nonce,
                "gas": gas,
                "maxPriorityFeePerGas": eth_utils.to_wei(
                    max_priority_fee_per_gas_wei, "wei"
                ),
                "maxFeePerGas": eth_utils.to_wei(max_fee_per_gas_wei, "wei"),
                # "gasPrice": int, # legacy pricing
                # "type": int,
                # "value": Wei,
            },
        )
    ).rawTransaction


def create_transaction_data(fn: AsyncContractFunction) -> HexStr:
    return encode_transaction_data(
        fn.w3, fn.function_identifier, fn.contract_abi, fn.abi, fn.args, fn.kwargs
    )


async def wait_for_transactions(
    transactions: list[HexBytes], timeout: float = 60.0
) -> list[tuple[int, TxReceipt]]:
    start_time = time.monotonic()
    pending_txs = set(transactions)
    receipts = []
    while pending_txs and time.monotonic() < start_time + timeout:
        for tx in pending_txs.copy():
            try:
                receipts.append(
                    (
                        transactions.index(tx),
                        await w3_public.eth.get_transaction_receipt(tx),
                    )
                )
                pending_txs.remove(tx)
            except TransactionNotFound:
                print(f"{tx.hex()} is not ready yet")
    return receipts


async def log_failed_transaction(
    chain_id: int,
    nonce: int,
    fn: AsyncContractFunction,
    receipt: TxReceipt,
) -> None:
    try:
        call_response = await w3_private.eth.call(
            {
                "chainId": chain_id,
                "to": receipt["to"],
                "from": receipt["from"],
                "value": 0,
                "data": create_transaction_data(fn),
                "nonce": nonce,
            },
            receipt["blockNumber"] - 1,
        )
        raise ValueError(f"Something fishy is happening with {call_response = }")
    except ContractLogicError as e:
        print(receipt["transactionHash"].hex(), e)


def calculate_fees_in_gwei(
    priority_fee_estimate: int, latest_block: BlockData
) -> tuple[int, int]:
    return (
        priority_fee_estimate * 11 // 10,
        priority_fee_estimate * 11 // 10 + latest_block["baseFeePerGas"] * 2,
    )


async def transfer(
    chain_id: int,
    nonce: int,
    smartwallet_address_list: list[tuple[str, str]],
) -> int:
    print(chain_id, nonce, len(smartwallet_address_list))
    max_priority_fee_per_gas, max_fee_per_gas = calculate_fees_in_gwei(
        await w3_public.eth.max_priority_fee,
        await w3_public.eth.get_block("latest"),
    )
    transfer_functions = [
        smartwallet_contracts[smartwallet_address].functions.transferERC20Shares(
            currency_address
        )
        for smartwallet_address, currency_address in smartwallet_address_list
    ]
    coros = [
        fn.w3.eth.send_raw_transaction(
            create_raw_transaction(
                fn,
                chain_id,
                nonce + index,
                GAS_UNITS,
                max_priority_fee_per_gas,
                max_fee_per_gas,
            )
        )
        for index, fn in enumerate(transfer_functions)
    ]
    sent_transactions = await simple_limiter(16, coros)
    for tx in sent_transactions:
        print("transaction", tx.hex())
    for index, receipt in await wait_for_transactions(sent_transactions):
        if not receipt["status"]:
            await log_failed_transaction(
                chain_id, nonce + index, transfer_functions[index], receipt
            )
    return len(smartwallet_address_list)


async def main():
    chain_id = await w3_public.eth.chain_id
    tx_count = await w3_public.eth.get_transaction_count(account.address)
    smartwallet_address_list = [
        (address, USDT_CONTRACT_ADDRESS) for address in smartwallet_contract_addresses
    ]
    tx_count += await transfer(chain_id, tx_count, smartwallet_address_list)


if __name__ == "__main__":
    asyncio.run(main())
