import asyncio
import json
import pprint

from indy import pool, ledger, wallet, did, anoncreds
from indy.error import IndyError, ErrorCode

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION


def print_log(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\033[92m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))




async def create_prover_wallet(): #여기에는 데이터 값이 들어가는곳 22줄
    await pool.set_protocol_version(PROTOCOL_VERSION)
    prover = {
        'wallet_config': json.dumps({'id': 'prover_wallet'}), #prover에 회원의 아이디가 들어간다.
        'wallet_credentials': json.dumps({'key': 'prover_wallet_key'}),
        'pool_name': 'toilet_pool'
    }
    prover['pool'] = await pool.open_pool_ledger(prover['pool_name'], None)
    #prover의 지갑 생성
    await wallet.create_wallet(prover['wallet_config'], prover['wallet_credentials'])
    
    #prover의 지갑 접근
    prover['wallet'] = await wallet.open_wallet(prover['wallet_config'], prover['wallet_credentials'])

    #prover의 did생성
    (prover['did'], prover['verkey']) = \
        await did.create_and_store_my_did(prover['wallet'], json.dumps({"seed": prover['seed']}))
    

    # link_secret
    prover['link_secret'] = 'link_secret' #지갑이름이 되는 
    prover['link_secret_id'] = await anoncreds.prover_create_master_secret(prover['wallet'],
                                                                     prover['link_secret'])

    return prover
    # VC제출용 양식 가져오기
    # prover['cred_offer'] = await anoncreds.issuer_create_credential_offer(issuer['wallet'],
    #                                                                      cred_def_id) # cred_def_id > schema id
   