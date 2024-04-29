import asyncio
import json
import time

from web3 import Web3, AsyncWeb3
from web3.contract import Contract
from aiohttp.client_exceptions import ClientResponseError


ALCHEMY_API_KEY = "API KEY"
NETWORK = "polygon-mumbai"
PRIVATE_PROVIDER_URL = f"https://{NETWORK}.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
PUBLIC_PROVIDER_URL = "https://rpc-mumbai.maticvigil.com"  # 20 req/s
USDT_CONTRACT_ADDRESS = "0x78c731f4a5f01e8C6b826A6ba67c6574AE2DF2Dd"
with open("./usdt_abi.json") as fp:
    usdt_contract_abi = json.load(fp)
w3_private = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(PRIVATE_PROVIDER_URL))
w3_public = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(PUBLIC_PROVIDER_URL))
usdt_contract = w3_public.eth.contract(
    address=USDT_CONTRACT_ADDRESS, abi=usdt_contract_abi
)
monitoring_wallet_addresses = [
    "0x459844736c643a7FEFE944C8cA95D7b31192F524",
    "0xc554c6c066cAE77d6D1C14feC2ec76DFed007e11",
    "0x666fD2761BdC08Da633831091A280AB3a69E8ED5",
    "0xA1d1235DCed1ed364d88410fB161407806D88374",
    "0x1111111111111111111111111111111111111111",
    "0x459844736c643a7FEFE944C8cA95D7b31192F524",
    "0xc554c6c066cAE77d6D1C14feC2ec76DFed007e11",
    "0x666fD2761BdC08Da633831091A280AB3a69E8ED5",
    "0xA1d1235DCed1ed364d88410fB161407806D88374",
    "0x1111111111111111111111111111111111111111",
    "0x459844736c643a7FEFE944C8cA95D7b31192F524",
    "0xc554c6c066cAE77d6D1C14feC2ec76DFed007e11",
    "0x666fD2761BdC08Da633831091A280AB3a69E8ED5",
    "0xA1d1235DCed1ed364d88410fB161407806D88374",
    "0x1111111111111111111111111111111111111111",
    "0x459844736c643a7FEFE944C8cA95D7b31192F524",
    "0xc554c6c066cAE77d6D1C14feC2ec76DFed007e11",
    "0x666fD2761BdC08Da633831091A280AB3a69E8ED5",
    "0xA1d1235DCed1ed364d88410fB161407806D88374",
    "0x1111111111111111111111111111111111111111",
    "0x459844736c643a7FEFE944C8cA95D7b31192F524",
    "0xc554c6c066cAE77d6D1C14feC2ec76DFed007e11",
    "0x666fD2761BdC08Da633831091A280AB3a69E8ED5",
    "0xA1d1235DCed1ed364d88410fB161407806D88374",
    "0x1111111111111111111111111111111111111111",
    "0x459844736c643a7FEFE944C8cA95D7b31192F524",
    "0xc554c6c066cAE77d6D1C14feC2ec76DFed007e11",
    "0x666fD2761BdC08Da633831091A280AB3a69E8ED5",
    "0xA1d1235DCed1ed364d88410fB161407806D88374",
    "0x1111111111111111111111111111111111111111",
    "0x459844736c643a7FEFE944C8cA95D7b31192F524",
    "0xc554c6c066cAE77d6D1C14feC2ec76DFed007e11",
    "0x666fD2761BdC08Da633831091A280AB3a69E8ED5",
    "0xA1d1235DCed1ed364d88410fB161407806D88374",
    "0x1111111111111111111111111111111111111111",
    "0x459844736c643a7FEFE944C8cA95D7b31192F524",
    "0xc554c6c066cAE77d6D1C14feC2ec76DFed007e11",
    "0x666fD2761BdC08Da633831091A280AB3a69E8ED5",
    "0xA1d1235DCed1ed364d88410fB161407806D88374",
    "0x1111111111111111111111111111111111111111",
]


async def _run_for_one_second(lock, coro):
    async with lock:
        res, _ = await asyncio.gather(coro, asyncio.sleep(1))
        return res


async def simple_limiter(burst, coros):
    sem = asyncio.Semaphore(burst)
    return await asyncio.gather(*[_run_for_one_second(sem, c) for c in coros])


async def call_transfers(addresses):
    raise NotImplementedError()


async def main():
    coros = [
        usdt_contract.functions.balanceOf(address).call()
        for address in monitoring_wallet_addresses
    ]
    address_balance = dict(
        zip(monitoring_wallet_addresses, await simple_limiter(20, coros), strict=True)
    )
    wallet_addresses_with_balance = [
        address for address, balance in address_balance.items() if balance > 0
    ]
    await call_transfers(wallet_addresses_with_balance)


if __name__ == "__main__":
    asyncio.run(main())
