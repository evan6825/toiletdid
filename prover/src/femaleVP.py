import asyncio
import json
import pprint

from indy import pool, ledger, wallet, did, anoncreds
from indy.error import IndyError, ErrorCode
from samples.did import sdk,issuer
from samples.schema import schema, proof_schema
from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION
params = {
        "id" : "evan6825@naver.com",
        "did" : "Ca6yc7pHjXKqZEVAMwYuMv"
        }
def print_log(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\033[92m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))

async def VP1(params):

    try:
        prover = {
            "wallet_config" :  json.dumps({"id": params["id"]}),
            "wallet_credentials" : json.dumps({"key": params["id"]+'_key'}),
            "link_secret" : params["id"],
            "did" : params["did"]
        }


        await pool.set_protocol_version(PROTOCOL_VERSION)
        try :
            sdk['pool'] = await pool.open_pool_ledger(sdk['pool_name'], None)
        except :
            pass
        prover['wallet'] = await wallet.open_wallet(prover['wallet_config'], prover['wallet_credentials'])


        nonce = await anoncreds.generate_nonce()
        sdk['proof_req'] = json.dumps({
            'nonce': "123123",
            'name': 'proof_req_1',
            'version': '0.1',
            'requested_attributes': {
                'attr1_referent': {'name': 'name'}
            },
            'requested_predicates': {
                'predicate1_referent': {'name': 'gender', 'p_type': '<', 'p_value': 100}
            }
        })
        prover['proof_req'] = sdk['proof_req']

        prover["search_handle"] = \
            await anoncreds.prover_search_credentials_for_proof_req(prover['wallet'],prover["proof_req"],None)

        creds_for_attr1 = await anoncreds.prover_fetch_credentials_for_proof_req(prover['search_handle'],
                                                                                'attr1_referent', 10)
        prover['cred_for_attr1']= json.loads(creds_for_attr1)[0]['cred_info']

        creds_for_predicate1 = await anoncreds.prover_fetch_credentials_for_proof_req(prover['search_handle'],
                                                                                    'predicate1_referent', 10)
        prover['cred_for_predicate1'] = json.loads(creds_for_predicate1)[0]['cred_info']

        await anoncreds.prover_close_credentials_search_for_proof_req(prover['search_handle'])


        prover['requested_creds'] = json.dumps({
            'self_attested_attributes': {},
            'requested_attributes': {'attr1_referent': {'cred_id': prover['cred_for_attr1']['referent'], 'revealed': True}},
            'requested_predicates': {'predicate1_referent': {'cred_id': prover['cred_for_predicate1']['referent']}}
        })



        schemas_json = json.dumps({proof_schema['schema_id']: json.loads(proof_schema['schema'])})
        cred_defs_json = json.dumps({proof_schema['cred_def_id']: json.loads(proof_schema['cred_def'])})
        revoc_states_json = json.dumps({})


        prover['proof'] = await anoncreds.prover_create_proof(prover['wallet'], prover['proof_req'],
                                                            prover['requested_creds'],
                                                            prover['link_secret'], schemas_json, cred_defs_json,
                                                            revoc_states_json)

        proof = {"message" : prover['proof']}

        # schemas_json = json.dumps({schema['schema_id']: json.loads(schema['schema'])})
        # cred_defs_json = json.dumps({proof_schema['cred_def_id']: json.loads(proof_schema['cred_def'])}) 
        # revoc_ref_defs_json = "{}"
        # revoc_regs_json = "{}"

        # assert await anoncreds.verifier_verify_proof(sdk['proof_req'], proof, schemas_json, cred_defs_json,
        #                                             revoc_ref_defs_json, revoc_regs_json)
        print_log("VP을 생성했습니다.")
        await wallet.close_wallet(prover['wallet'])
        try:
            await pool.close_pool_ledger(sdk['pool']) 
        except :
            pass  
        return proof
    except:
        errors = {"did": False}
        await wallet.close_wallet(prover['wallet'])
        return errors



def main(params):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(VP1(params))
    loop.close()


if __name__ == '__main__':
    main(params)
