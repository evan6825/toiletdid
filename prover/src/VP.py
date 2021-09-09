import asyncio
import json
import pprint

from indy import pool, ledger, wallet, did, anoncreds
from indy.error import IndyError, ErrorCode
from samples.did import sdk,issuer,prover
from VC import create_prover_wallet
from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION


async def create_prover_wallet():
    