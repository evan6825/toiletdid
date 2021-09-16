import asyncio
import json
import pprint
import base64
from indy import pool, ledger, wallet, did, anoncreds
from indy.error import IndyError, ErrorCode
from samples.did import sdk,issuer
from samples.schema import schema

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION



async def VC1(params): #여기에는 데이터 값이 들어가는곳 22줄
    #prover1 = params
    # prover = {
    #     "wallet_config" :  json.dumps({"id": prover1["id"]}),
    #     "wallet_credentials" : {"key": prover1["id"]+'_key'},
    #     "link_secret" : prover1["id"]
    # }
    # prover['wallet_config'] = json.dumps(prover["wallet_config"])
    # prover['wallet_credentials'] = json.dumps(prover["wallet_credentials"])
    
    
    prover = {
        "wallet_config" :  json.dumps({"id": params["id"]}),
        "wallet_credentials" : json.dumps({"key": params["id"]+'_key'}),
        "link_secret" : params["id"]
    }
    
    await pool.set_protocol_version(PROTOCOL_VERSION)
    prover['pool'] = await pool.open_pool_ledger(issuer['pool_name'], None)
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
    # (prover['did'],prover['verkey']) = await did.create_and_store_my_did(prover['wallet'],json.dumps({"seed": prover['seed']}))

    #서버연결시 사용
    (prover['did'],prover['verkey']) = await did.create_and_store_my_did(prover['wallet'],"{}")

    # link_secret
    #prover['link_secret'] = 'Jun' #prover의 did는 생성하지않는다 master_secret을 통해 생성한다.
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


    if prover1["gender"] == "male":
        prover1["gender_code"] = "101"
    elif prover1["gender"] == "female":
        prover1["gender_code"] = "99"


    # prover1["name_code"] = base64.b64encode(json.dump([prover1["name"]]))


    prover_information = json.dumps({
        "gender": {"raw": prover1["gender"], "encoded": prover1["gender_code"]},
        "Phone": {"raw": prover1["HP"], "encoded": prover1["HP"]},
        "name": {"raw": prover1["name"], "encoded": "123123123123"}
    })
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
    print(prover["link_secret_id"])
    print(prover1["gender_code"])
    return prover["did"],prover["link_secret_id"]

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(VC1())
    loop.close()



if __name__ == '__main__':
    main()
