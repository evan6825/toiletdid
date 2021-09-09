import asyncio
import json
import pprint

from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION

def print_log(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\033[92m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))

"""
issuer_did : SDK server did
toilet_did : Endpoint server did
"""
async def write_nym_and_query_verkey():
        await pool.set_protocol_version(PROTOCOL_VERSION)
        toilet = {
        'seed': '0000000000000000000000000toilet1',
        'wallet_config': json.dumps({'id': 'toilet_wallet'}),
        'wallet_credentials': json.dumps({'key': 'toilet_wallet_key'}),
        'pool_name': 'toilet_pool'
        }

        user = {
        'seed': '0000000000000000000000000toilet2',
        'wallet_config': json.dumps({'id': 'user_wallet'}),
        'wallet_credentials': json.dumps({'key': 'user_wallet_key'})
        }

        # 1. Create_pool_ledger and open_pool_ledger
        toilet['genesis_txn_path'] = get_pool_genesis_txn_path(toilet['pool_name'])
        toilet['pool_config'] = json.dumps({"genesis_txn": str(toilet['genesis_txn_path'])})
        try:
            await pool.create_pool_ledger_config(toilet['pool_name'], toilet['pool_config'])
        except IndyError as ex:
            if ex.error_code == ErrorCode.PoolLedgerConfigAlreadyExistsError:
                pass


        toilet['pool'] = await pool.open_pool_ledger(toilet['pool_name'], None)

        # 2. Create SDK_server = 
        await wallet.create_wallet(toilet['wallet_config'], toilet['wallet_credentials'])
        toilet['wallet'] = await wallet.open_wallet(toilet['wallet_config'], toilet['wallet_credentials'])
        
        # 3. Create Trustee DID
        (toilet['did'], toilet['verkey']) = \
        await did.create_and_store_my_did(toilet['wallet'], json.dumps({"seed": toilet['seed']}))   


        # Create Endpoint_wallet and Endpoint_did
        await wallet.create_wallet(user['wallet_config'], user['wallet_credentials'])
        user['wallet'] = await wallet.open_wallet(user['wallet_config'], user['wallet_credentials'])
        (user['did'], user['verkey']) = await did.create_and_store_my_did(user['wallet'], json.dumps({"seed": user['seed']}))


        # toilet 변수(variable)에 Endpoint_wallet and did 저장
        toilet['toilet_did'] = user['did']
        toilet['toilet_verkey'] = user['verkey']
        nym_req = await ledger.build_nym_request(toilet['did'], toilet['toilet_did'], toilet['toilet_verkey'], None, None)
        await ledger.sign_and_submit_request(toilet['pool'], toilet['wallet'], toilet['did'], nym_req)
        await wallet.close_wallet(toilet['wallet'])
        await pool.close_pool_ledger(toilet['pool'])    
        print("issuer_did :")
        print(toilet["did"])
        print("issuer_verkey : ")
        print(toilet["verkey"])
        print("toilet_did :")
        print(toilet["toilet_did"])
        print("toilet_verkey : ")
        print(toilet["toilet_verkey"])
        
        return toilet

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(write_nym_and_query_verkey())
    loop.close()


if __name__ == '__main__':
    main()

