import asyncio
import websockets
import json
import eth_utils
from eth_typing import ChecksumAddress
import logging
import web3
import httpx
from web3.contract.async_contract import AsyncContract, AsyncContractFunction
from typing import TypeVar, Any, Protocol
from collections.abc import Awaitable
from web3.types import Nonce, Wei, EventData
from hexbytes import HexBytes
import time
import functools
import eth_account
from eth_account.signers.base import BaseAccount
from collections.abc import Callable, Iterable
from decimal import Decimal
import math
import eth_abi


T = TypeVar("T")
QMATIC_TRANSFER_ABI = {
    "inputs": [
        {"internalType": "address", "name": "to", "type": "address"},
        {"internalType": "uint256", "name": "amount", "type": "uint256"},
    ],
    "name": "transferWithLocking",
    "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
    "stateMutability": "nonpayable",
    "type": "function",
}
ERC20_TRANSFER_ABI = {
    "inputs": [
        {"internalType": "address", "name": "to", "type": "address"},
        {"internalType": "uint256", "name": "amount", "type": "uint256"},
    ],
    "name": "transfer",
    "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
    "stateMutability": "nonpayable",
    "type": "function",
}
ERC20_DECIMALS_ABI = {
    "inputs": [],
    "name": "decimals",
    "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
    "stateMutability": "view",
    "type": "function",
}
ERC20_TRANSFER_EVENT_ABI = {
    "anonymous": False,
    "inputs": [
        {"indexed": True, "internalType": "address", "name": "from", "type": "address"},
        {"indexed": True, "internalType": "address", "name": "to", "type": "address"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "value",
            "type": "uint256",
        },
    ],
    "name": "Transfer",
    "type": "event",
}
ERC20_SMARTCONTRACT_ABI = [
    ERC20_TRANSFER_ABI,
    ERC20_DECIMALS_ABI,
    ERC20_TRANSFER_EVENT_ABI,
]
QMATIC_SMARTCONTRACT_ABI = [
    QMATIC_TRANSFER_ABI,
    ERC20_TRANSFER_ABI,
    ERC20_DECIMALS_ABI,
    ERC20_TRANSFER_EVENT_ABI,
]
CODEC = eth_abi.codec.ABICodec(web3._utils.abi.build_strict_registry())
GAS_UNITS = 420_000
TOKENS_PER_DOLLAR = 40
MUMBAI_MTK_ADDRESS = eth_utils.to_checksum_address(
    "0x4AC73A203CB905f0FDee58fD5f44365e520B73d5"
)
MUMBAI_QMATIC_ADDRESS = eth_utils.to_checksum_address(
    "0x2F67AEeC4c48B0634EFfC56fC3B6f991996919cE"
)
MRM_PRIVATE1 = "PRIVATE KEY 1"
MRM_PRIVATE3 = "PRIVATE KEY 2"
MRM_WALLET3 = eth_utils.to_checksum_address(
    "0x45305722116E92CD50899A43085f436a8D8427ae"
)
MR_WALLET3 = eth_utils.to_checksum_address("0xa36e97DeC8eEdA8aFaC05C1acbB85015228DcF58")
MR_WALLET4 = eth_utils.to_checksum_address("0xCeB7A6Ab0e5d2ABf48B840f6876C2E0acf2D305D")


def async_cached(ttl: float = 1.0):
    def wrapper(f):
        lock = asyncio.Lock()
        time_since_last_call = 0
        last_value = None

        @functools.wraps(f)
        async def wrapped(*args, **kwargs):
            nonlocal time_since_last_call, last_value
            async with lock:
                if (
                    time_since_last_call is None
                    or time.monotonic() - time_since_last_call > ttl
                ):
                    last_value = await f(*args, **kwargs)
                    time_since_last_call = time.monotonic()
                return last_value

        return wrapped

    return wrapper


class SimpleLockManager:
    def __init__(self, burst: int):
        self._lock = asyncio.Lock()
        self._total_access = 0
        self._burst = burst
        self._last_bucket = int(time.monotonic())

    async def acquire(self) -> None:
        async with self._lock:
            if self._total_access >= self._burst:
                await asyncio.sleep(1)
                self._last_bucket = int(time.monotonic())
                self._total_access = 0
            if (current_bucket := int(time.monotonic())) != self._last_bucket:
                self._last_bucket = current_bucket
                self._total_access = 0
            self._total_access += 1


class W3AccountManager:
    def __init__(
        self,
        w3: web3.AsyncWeb3,
        account: BaseAccount,
        lock_manager: SimpleLockManager,
    ):
        self.w3 = w3
        self._account = account
        self._lock_manager = lock_manager
        self._chain_id: int | None = None
        self._tx_count: int | None = None
        self._client = httpx.AsyncClient()

    @property
    def chain_id(self) -> int:
        if self._chain_id is None:
            raise RuntimeError("Manager is not started")
        return self._chain_id

    @property
    def tx_count(self) -> int:
        if self._tx_count is None:
            raise RuntimeError("Manager is not started")
        return self._tx_count

    async def _request(self, coro: Awaitable[T]) -> T:
        await self._lock_manager.acquire()
        return await coro

    async def start(self) -> None:
        self._chain_id = await self._request(self.w3.eth.chain_id)
        self._tx_count = await self._request(
            self.w3.eth.get_transaction_count(self._account.address)
        )

    async def call(self, fn: AsyncContractFunction) -> Any:
        return await self._request(fn.call())

    @async_cached(2.5)
    async def get_high_fees(self) -> tuple[int, int]:
        resp = await self._client.get(
            f"https://gas-api.metaswap.codefi.network/networks/{self.chain_id}/suggestedGasFees",
            headers={"X-Client-Id": "extension"},
        )
        # Raise for errors
        fee_result = resp.json()
        return (
            eth_utils.to_wei(
                (fee_result["high"]["suggestedMaxPriorityFeePerGas"]), "gwei"
            ),
            eth_utils.to_wei(fee_result["high"]["suggestedMaxFeePerGas"], "gwei"),
        )

    def _create_raw_transaction(
        self,
        fn: AsyncContractFunction,
        nonce: Nonce,
        gas: int,
        max_priority_fee_per_gas_wei: int,
        max_fee_per_gas_wei: int,
    ) -> HexBytes:
        return self._account.sign_transaction(  # type: ignore
            web3._utils.contracts.prepare_transaction(
                address=fn.address,
                w3=fn.w3,
                fn_identifier=fn.function_identifier,
                contract_abi=fn.contract_abi,
                fn_abi=fn.abi,
                fn_args=fn.args,
                fn_kwargs=fn.kwargs,
                transaction={
                    "chainId": self.chain_id,
                    "from": self._account.address,
                    "nonce": nonce,
                    "gas": gas,
                    "maxPriorityFeePerGas": Wei(max_priority_fee_per_gas_wei),
                    "maxFeePerGas": Wei(max_fee_per_gas_wei),
                    # "gasPrice": int, # legacy pricing
                    # "type": int,
                    # "value": Wei,
                },
            )
        ).rawTransaction

    async def send_raw_transaction(
        self,
        fn: AsyncContractFunction,
        gas: int,
        max_priority_fee_per_gas_wei: int,
        max_fee_per_gas_wei: int,
    ) -> tuple[Nonce, HexBytes]:
        nonce = Nonce(self.tx_count)
        self._tx_count += 1  # type: ignore
        return nonce, await self._request(
            self.w3.eth.send_raw_transaction(
                self._create_raw_transaction(
                    fn,
                    nonce,
                    gas,
                    max_priority_fee_per_gas_wei,
                    max_fee_per_gas_wei,
                )
            )
        )


class W3WebsocketClient:
    def __init__(self, url: str):
        self._url = url
        self._lock = asyncio.Lock()
        self._started_event = asyncio.Event()
        self._subscription_queue: asyncio.Queue[str] = asyncio.Queue(1)
        self._callbacks: dict[str, Callable] = {}
        self._receiver_task = None
        self._connection = None

    async def subscribe(self, params: list[Any], callback: Callable):
        async with self._lock:
            if self._connection is None:
                raise RuntimeError("Client is not started")
            print("subscribe", params)
            await self._connection.send(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "eth_subscribe",
                        "params": params,
                    }
                )
            )
            subscription_id = await self._subscription_queue.get()
            self._callbacks[subscription_id] = callback

    async def _receiver(self):
        async for connection in websockets.connect(self._url):
            self._started_event.set()
            self._connection = connection
            try:
                async for raw_msg in connection:
                    msg = json.loads(raw_msg)
                    print("received", msg)
                    if "result" in msg:
                        self._subscription_queue.put_nowait(msg["result"])
                    elif msg["method"] == "eth_subscription":
                        asyncio.create_task(
                            self._callbacks[msg["params"]["subscription"]](
                                msg["params"]["result"]
                            )
                        )
                    else:
                        raise RuntimeError("Unknown message", msg)
            except websockets.ConnectionClosed:
                continue

    async def start(self):
        self._receiver_task = asyncio.create_task(self._receiver())
        await self._started_event.wait()

    async def stop(self):
        self._receiver_task.cancel()
        self._started_event.clear()


class TransferableTokenContract(Protocol):
    @property
    def address(self) -> ChecksumAddress:
        ...

    @property
    def decimals(self) -> int:
        ...

    async def transfer_fast(
        self, to: ChecksumAddress, amount: int
    ) -> tuple[Nonce, HexBytes]:
        ...


class ERC20Contract:
    def __init__(
        self,
        address: ChecksumAddress,
        w3_account_manager: W3AccountManager,
    ):
        self._w3_account_manager = w3_account_manager
        self._w3_contract = self._w3_account_manager.w3.eth.contract(
            address=address, abi=ERC20_SMARTCONTRACT_ABI
        )
        self._decimals: int | None = None

    @property
    def address(self) -> ChecksumAddress:
        return self._w3_contract.address

    @property
    def decimals(self) -> int:
        if self._decimals is None:
            raise RuntimeError("Contract is not started")
        return self._decimals

    async def start(self):
        self._decimals = await self._w3_account_manager.call(
            self._w3_contract.functions.decimals()
        )

    async def transfer_fast(
        self, to: ChecksumAddress, amount: int
    ) -> tuple[Nonce, HexBytes]:
        max_priority_fee, max_fee = await self._w3_account_manager.get_high_fees()
        print("==============TRANSFER", to, amount, max_priority_fee, max_fee)
        return await self._w3_account_manager.send_raw_transaction(
            self._w3_contract.functions.transfer(to, amount),
            GAS_UNITS,
            max_priority_fee,
            max_fee,
        )


class QmaticContract:
    def __init__(
        self,
        address: ChecksumAddress,
        w3_account_manager: W3AccountManager,
    ):
        self._w3_account_manager = w3_account_manager
        self._w3_contract = self._w3_account_manager.w3.eth.contract(
            address=address, abi=QMATIC_SMARTCONTRACT_ABI
        )
        self._decimals: int | None = None

    @property
    def address(self) -> ChecksumAddress:
        return self._w3_contract.address

    @property
    def decimals(self) -> int:
        return 18

    async def transfer_fast(
        self, to: ChecksumAddress, amount: int
    ) -> tuple[Nonce, HexBytes]:
        max_priority_fee, max_fee = await self._w3_account_manager.get_high_fees()
        print("==============TRANSFER", to, amount, max_priority_fee, max_fee)
        return await self._w3_account_manager.send_raw_transaction(
            self._w3_contract.functions.transferWithLocking(to, amount),
            GAS_UNITS,
            max_priority_fee,
            max_fee,
        )


class ERC20TokenObserver:
    def __init__(
        self,
        contract: TransferableTokenContract,
        destination_contract: TransferableTokenContract,
        w3_websocket_client: W3WebsocketClient,
        receiving_addresses: Iterable[ChecksumAddress] | None = None,
    ):
        self._contract = contract
        self._destination_contract = destination_contract
        self._w3_websocket_client = w3_websocket_client
        self._receiving_addresses = set(receiving_addresses or [])
        self._decimals = None

    async def start(self):
        for destination_address in self._receiving_addresses:
            await self._w3_websocket_client.subscribe(
                [
                    "logs",
                    {
                        "address": self._contract.address,
                        "topics": web3._utils.events.construct_event_topic_set(
                            ERC20_TRANSFER_EVENT_ABI,
                            CODEC,
                            {"to": destination_address},
                        ),
                        #     eth_utils.to_hex(
                        #         eth_utils.keccak(b"Transfer(address,address,uint256)")
                        #     ),
                    },
                ],
                self._process_log,
            )

    async def _process_log(self, log_entry: dict) -> None:
        if log_entry["removed"]:
            return
        log_entry["topics"] = [
            eth_utils.to_bytes(hexstr=rec) for rec in log_entry["topics"]
        ]
        event: EventData = web3._utils.events.get_event_data(
            CODEC, ERC20_TRANSFER_EVENT_ABI, log_entry
        )
        event_address, event_from, event_to = (
            eth_utils.to_checksum_address(r)
            for r in (event["address"], event["args"]["from"], event["args"]["to"])
        )
        if event_address != self._contract.address:
            raise ValueError("Bad address", event_address)
        if event_to not in self._receiving_addresses:
            raise ValueError("Bad destination", event_to)
        transfer_amount = math.floor(
            Decimal(event["args"]["value"])
            / 10 ** self._contract.decimals
            * TOKENS_PER_DOLLAR
            * 10 ** self._destination_contract.decimals
        )
        print(
            await self._destination_contract.transfer_fast(event_from, transfer_amount)
        )


async def main():
    w3_websocket_client = W3WebsocketClient(
        # "wss://polygon-testnet.blastapi.io/7c2da2db-eea8-40e5-8fc2-6fca3b15ccd0"
        "wss://ws-polygon-mumbai.chainstacklabs.com"
    )
    await w3_websocket_client.start()

    w3_account_manager = W3AccountManager(
        web3.AsyncWeb3(
            web3.providers.async_rpc.AsyncHTTPProvider(
                # "https://polygon-testnet.blastapi.io/7c2da2db-eea8-40e5-8fc2-6fca3b15ccd0"
                "https://polygon-mumbai.chainstacklabs.com"
            ),
            [web3.middleware.geth_poa.async_geth_poa_middleware],
        ),
        eth_account.Account.from_key(MRM_PRIVATE3),
        SimpleLockManager(25),
    )
    await w3_account_manager.start()

    mtk_contract = ERC20Contract(MUMBAI_MTK_ADDRESS, w3_account_manager)
    await mtk_contract.start()

    qmatic_contract = QmaticContract(MUMBAI_QMATIC_ADDRESS, w3_account_manager)

    mtk_observer = ERC20TokenObserver(
        mtk_contract,
        qmatic_contract,
        w3_websocket_client,
        [MR_WALLET3, MR_WALLET4],
    )
    await mtk_observer.start()

    await w3_websocket_client._receiver_task


# w3_account_manager = PublicW3AccountManager(
#     web3.AsyncWeb3(
#         web3.providers.async_rpc.AsyncHTTPProvider(
#             "https://polygon-testnet.blastapi.io/7c2da2db-eea8-40e5-8fc2-6fca3b15ccd0"
#         ),
#         [web3.middleware.geth_poa.async_geth_poa_middleware],
#     ),
#     eth_account.Account.from_key(
#         ""
#     ),
#     SimpleLockManager(25),
#     {"0x4AC73A203CB905f0FDee58fD5f44365e520B73d5": ERC20_TRANSFER_SMARTCONTRACT},
# )
# w3_websocket_client = W3WebsocketClient(
#     "wss://polygon-mainnet.blastapi.io/7c2da2db-eea8-40e5-8fc2-6fca3b15ccd0"
# )
logging.basicConfig(level=logging.DEBUG)
asyncio.run(main())
