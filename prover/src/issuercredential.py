import asyncio
import json
import pprint

from indy import pool, ledger, wallet, did, anoncreds
from indy.error import ErrorCode, IndyError
from samples import sdk,issuer

from createproverwallet import create_prover_wallet
def print_log(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\033[92m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))


async def create_prover_wallet():
    prover = await create_prover_wallet()

    # VC제출용 양식 가져오기
    prover['cred_offer'] = await anoncreds.issuer_create_credential_offer(issuer['wallet'],
                                                                         issuer['cred_def_id']) # cred_def_id > schema 에서 cred_def_id
   