from typing import TypedDict, List

import requests

from stacks_monitor.constants import *


class RosettaTransactionIdentifier(TypedDict):
    hash: str


class RosettaTransaction(TypedDict):
    transaction_identifier: RosettaTransactionIdentifier


class RosettaBlockIdentifier(TypedDict):
    hash: str
    index: int


class RosettaBlock(TypedDict):
    block_identifier: RosettaBlockIdentifier
    parent_block_identifier: RosettaBlockIdentifier
    timestamp: int
    transactions: List[RosettaTransaction]


class RosettaBlockResponse(TypedDict):
    block: RosettaBlock


def rosetta_get_block(block_height: int = 0) -> RosettaBlockResponse:
    payload = {
        "network_identifier": {
            "blockchain": ROSETTA_BLOCKCHAIN, "network": ROSETTA_NETWORK
        },
        "block_identifier": {
            "index": block_height
        }
    }

    resp = requests.post("{}/rosetta/v1/block".format(STACKS_API_BASE), json=payload, timeout=5)

    return resp.json()


class Transaction(TypedDict):
    tx_id: str
    # ...


def get_transaction(tx_hash: str) -> Transaction:
    u = "{}/extended/v1/tx/{}".format(STACKS_API_BASE, tx_hash)

    return requests.get(u, timeout=5).json()
