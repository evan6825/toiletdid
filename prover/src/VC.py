import asyncio
import json
import pprint

from indy import pool, ledger, wallet, did, anoncreds
from indy.error import IndyError, ErrorCode
from samples.did import sdk,issuer,prover
from samples.schema import schema
from samples.prover import prover_information
from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION



async def VC(): #여기에는 데이터 값이 들어가는곳 22줄
    await pool.set_protocol_version(PROTOCOL_VERSION)
    prover['pool'] = await pool.open_pool_ledger(prover['pool_name'], None)
    #prover의 지갑 생성
    try:
        await wallet.create_wallet(prover["wallet_config"],prover['wallet_credentials'])
    except IndyError as err:
        if err.error_code == ErrorCode.WalletAlreadyExistsError:
            print("지갑이 이미 생성 되어있습니다.")
            pass 
    
    
    #prover의 지갑 접근
    issuer['wallet'] = await wallet.open_wallet(issuer['wallet_config'], issuer['wallet_credentials'])
    prover['wallet'] = await wallet.open_wallet(prover['wallet_config'], prover['wallet_credentials'])

    #prover의 did생성
    (prover['did'],prover['verkey']) = await did.create_and_store_my_did(prover['wallet'],json.dumps({"seed": prover['seed']}))

    #서버연결시 사용
    #(prover['did'],prover['verkey']) = await did.create_and_store_my_did(prover['wallet'],"{}")

    # link_secret
    prover['link_secret'] = 'Jun' #prover의 did는 생성하지않는다 master_secret을 통해 생성한다.
    prover['link_secret_id'] = await anoncreds.prover_create_master_secret(prover['wallet'],
                                                                        prover['link_secret'])
    


    prover['cred_offer'] = await anoncreds.issuer_create_credential_offer(issuer['wallet'],
                                                                         schema['cred_def_id']) # cred_def_id > schema 에서 cred_def_id
   
    
    #prover['cred_def_id'] = json.dumps(schema['cred_def_id'])
    prover['cred_def'] = json.dumps(schema['cred_def'])

    (prover['cred_req'], prover['cred_req_metadata']) = \
        await anoncreds.prover_create_credential_req(prover['wallet'],
                                                     prover['did'],
                                                     prover['cred_offer'],
                                                     prover['cred_def'],
                                                     prover['link_secret'])
    prover['cred_values'] = prover_information

    (prover['cred'], _, _) = \
        await anoncreds.issuer_create_credential(issuer['wallet'],
                                                     prover['cred_offer'],
                                                     prover['cred_req'],
                                                     prover['cred_values'], None, None)

    await anoncreds.prover_store_credential(prover['wallet'], None,
                                            prover['cred_req_metadata'],
                                            prover['cred'],
                                            prover['cred_def'], None)
    print(prover["did"])
    return prover

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(VC())
    loop.close()


if __name__ == '__main__':
    main()
