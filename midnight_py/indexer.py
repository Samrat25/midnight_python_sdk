import httpx
import json
from typing import AsyncIterator
from .models import ContractState
from .exceptions import ConnectionError as MidnightConnectionError


class IndexerClient:
    """
    Reads public on-chain state from the Midnight indexer.
    Connects to real Midnight GraphQL API.
    """

    def __init__(self, url: str, ws_url: str = None, network_id: str = "undeployed"):
        self.url = url
        self.ws_url = ws_url
        self.network_id = network_id
        self._http = httpx.Client(timeout=30.0)

    def is_alive(self) -> bool:
        try:
            r = self._http.post(
                self.url,
                json={"query": "{ __typename }"},
                headers={"Content-Type": "application/json"},
            )
            return r.status_code == 200
        except Exception:
            return False

    def get_contract_state(self, address: str) -> ContractState:
        """Read the current public ledger state of a contract."""
        query = """
        query GetContractState($address: String!) {
            contractState(address: $address) {
                state
                blockHeight
            }
        }
        """
        try:
            response = self._http.post(
                self.url,
                json={"query": query, "variables": {"address": address}},
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
        except httpx.ConnectError:
            raise MidnightConnectionError("Indexer", self.url)

        data = response.json()
        if "errors" in data:
            raise MidnightConnectionError("Indexer", str(data["errors"]))

        result = data["data"]["contractState"]
        return ContractState(
            address=address,
            state=result["state"],
            block_height=result["blockHeight"],
        )

    def get_transaction(self, tx_hash: str) -> dict:
        """Get transaction details by hash."""
        query = """
        query GetTransaction($hash: String!) {
            transaction(hash: $hash) {
                hash
                blockHeight
                status
            }
        }
        """
        response = self._http.post(
            self.url,
            json={"query": query, "variables": {"hash": tx_hash}},
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json()["data"]["transaction"]

    async def stream_events(self, address: str) -> AsyncIterator[dict]:
        """
        Stream contract events in real-time via WebSocket.
        
        Usage:
            async for event in client.indexer.stream_events("addr123"):
                print(event)
        """
        import websockets
        async with websockets.connect(self.ws_url) as ws:
            await ws.send(json.dumps({
                "type": "start",
                "payload": {
                    "query": """
                    subscription ContractEvents($address: String!) {
                        contractEvents(address: $address) {
                            eventType
                            data
                            blockHeight
                            txHash
                        }
                    }
                    """,
                    "variables": {"address": address},
                },
            }))

            async for raw in ws:
                msg = json.loads(raw)
                if msg.get("type") == "data":
                    yield msg["payload"]["data"]["contractEvents"]
