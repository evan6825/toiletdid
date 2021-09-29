import asyncio
import json
from os import error
import pprint
import base64
from indy import pool, ledger, wallet, did, anoncreds
from indy.error import IndyError, ErrorCode, errorcode_to_exception
from samples.did import sdk,issuer
from samples.schema import schema

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION

def print_log(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\033[92m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))

params = {
        "id" : "evan6825@naver.com",
        "did" : "Ca6yc7pHjXKqZEVAMwYuMv"
        }

async def VC1(params): #여기에는 데이터 값이 들어가는곳 22줄
    try:
        #prover1 = params
        # prover = {
        #     "wallet_config" :  json.dumps({"id": prover1["id"]}),
        #     "wallet_credentials" : {"key": prover1["id"]+'_key'},
        #     "link_secret" : prover1["id"]
        # }
        # prover['wallet_config'] = json.dumps(prover["wallet_config"])
        # prover['wallet_credentials'] = json.dumps(prover["wallet_credentials"])
        # params = {
        # "id" : "evan12@naver.com",
        # "gender" : "female",
        # "phone": "01022126825",
        # "name" : "준홍"
        # }
        prover = {
            "wallet_config" :  json.dumps({"id": params["id"]}),
            "wallet_credentials" : json.dumps({"key": params["id"]+'_key'}),
            "link_secret" : params["id"]
        }
        await pool.set_protocol_version(PROTOCOL_VERSION)
        try :
            sdk['pool'] = await pool.open_pool_ledger(issuer['pool_name'], None)
        except :
            pass
        #prover의 지갑 생성
        # try:
        #     await wallet.create_wallet(prover["wallet_config"],prover['wallet_credentials'])
        # except IndyError as err:
        #     if err.error_code == ErrorCode.WalletAlreadyExistsError:ㄴ
        #         print("지갑이 이미 생성 되어있습니다.")
        try:
            await wallet.create_wallet(prover["wallet_config"],prover['wallet_credentials'])
        except :
            return print("이미 생성된 지갑입니다.")
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

        # mystring = prover1["name"]
        # mybytes = mystring.encode('utf-8')
        # myint = int.from_bytes(mybytes, 'little')


        if params["gender"] == "male":
            params["gender_code"] = "101"
        elif params["gender"] == "female":
            params["gender_code"] = "99"


        # prover1["name_code"] = base64.b64encode(json.dump([prover1["name"]]))


        prover_information = json.dumps({
            "gender": {"raw": params["gender"], "encoded": params["gender_code"]},
            "name" : {"raw": params["name"], "encoded":"123123123123"},
            "phone": {"raw": params["phone"], "encoded": params["phone"]}
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
        print(params["gender_code"])
        
        user_did = {"did": prover["did"]}
        print_log("VC에 성공했습니다")        



#추가한 부분
        await wallet.close_wallet(issuer['wallet'])
        await wallet.close_wallet(prover['wallet'])
        try:
            await pool.close_pool_ledger(sdk['pool']) 
        except :
            pass
#추가한 부분

        return user_did
    except IndyError as e:
        errors = {"did": False}
        print('Error occurred: %s' % e)
        return errors
def main(params):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(VC1(params))
    loop.close()



if __name__ == '__main__':
    main(parmas)