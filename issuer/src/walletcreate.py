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
sdk_did : DID채널을 운영하는 DID
issuer_did : Endpoint server did
"""
async def write_nym_and_query_verkey():
        await pool.set_protocol_version(PROTOCOL_VERSION)
        sdk = {
        'seed': '0000000000000000000000000000sdk1', #seed번호는 33자리 고정으로 되는지 확인
        'wallet_config': json.dumps({'id': 'sdk_wallet'}),
        'wallet_credentials': json.dumps({'key': 'sdk_wallet_key'}),
        'pool_name': 'toilet_pool'
        }

        issuer = {
        'seed': '0000000000000000000000000issuer2',
        'wallet_config': json.dumps({'id': 'sdk_wallet'}),
        'wallet_credentials': json.dumps({'key': 'sdk_wallet_key'})
        }

        # 1. Create_pool_ledger and open_pool_ledger
        sdk['genesis_txn_path'] = get_pool_genesis_txn_path(sdk['pool_name'])
        sdk['pool_config'] = json.dumps({"genesis_txn": str(sdk['genesis_txn_path'])})
        try:
            await pool.create_pool_ledger_config(sdk['pool_name'], sdk['pool_config'])
        except IndyError as ex:
            if ex.error_code == ErrorCode.PoolLedgerConfigAlreadyExistsError:
                pass
        sdk['pool'] = await pool.open_pool_ledger(sdk['pool_name'], None)

        # 2. Create SDK_server wallet and did
        await wallet.create_wallet(sdk['wallet_config'], sdk['wallet_credentials'])
        sdk['wallet'] = await wallet.open_wallet(sdk['wallet_config'], sdk['wallet_credentials'])
        (sdk['did'], sdk['verkey']) = \
        await did.create_and_store_my_did(sdk['wallet'], json.dumps({"seed": sdk['seed']}))   #여기문제 


        # Create Endpoint_did
        # await wallet.create_wallet(issuer['wallet_config'], issuer['wallet_credentials'])
        # issuer['wallet'] = await wallet.open_wallet(issuer['wallet_config'], issuer['wallet_credentials'])
        (issuer['did'], issuer['verkey']) = await did.create_and_store_my_did(sdk['wallet'], json.dumps({"seed": issuer['seed']}))


        # sdk 변수(variable)에 Endpoint_wallet and did 저장
        sdk['issuer_did'] = issuer['did']
        sdk['issuer_verkey'] = issuer['verkey']

        # ENDPOINT(issuer)의 NYM트랜잭션을 준비및 발송 
        nym_req = await ledger.build_nym_request(sdk['did'], sdk['issuer_did'], sdk['issuer_verkey'], None, None)
        await ledger.sign_and_submit_request(sdk['pool'], sdk['wallet'], sdk['did'], nym_req)

        # 저희는 직접 ENDPOINT(issuer)를 관리하기 때문에 rotatekey를 사용하지 않음
        

        #7번의 기능의 확실한 목적은? ENDPOINT에게 INDY_POOL에 접속할 아이피와 포트번호를 전달해주는 API?
        # # 7. issuer send ATTRIB transaction to Ledger
        # attr_req = \
        #     await ledger.build_attrib_request(issuer['did'], issuer['did'], None, '{"endpoint":{"ha":"127.0.0.1:5555"}}', None)
        # resp = await ledger.sign_and_submit_request(issuer['pool'], issuer['wallet'], issuer['did'], attr_req)

        # assert json.loads(resp)['op'] == 'REPLY'


        # wallet and pool close
        await wallet.close_wallet(sdk['wallet'])
        await pool.close_pool_ledger(sdk['pool'])    
        print("sdk_did :")
        print(sdk["did"])
        print("issuer_did :")
        print(sdk["issuer_did"])
        
        return sdk



def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(write_nym_and_query_verkey())
    loop.close()


if __name__ == '__main__':
    main()

