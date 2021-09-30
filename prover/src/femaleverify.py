import asyncio
import json
import pprint

from indy import pool, ledger, wallet, did, anoncreds
from indy.error import IndyError, ErrorCode
from samples.schema import schema, proof_schema
from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION

def print_log(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\033[92m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))



async def verify(params):
    try:
        proof= json.dumps({
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
        schemas_json = json.dumps({schema['schema_id']: json.loads(schema['schema'])})
        cred_defs_json = json.dumps({proof_schema['cred_def_id']: json.loads(proof_schema['cred_def'])}) 
        revoc_ref_defs_json = "{}"
        revoc_regs_json = "{}"

        await anoncreds.verifier_verify_proof(proof, params, schemas_json, cred_defs_json,
                                                    revoc_ref_defs_json, revoc_regs_json)                                                           
        result = {"message" : True}
        print_log("VP검증에 성공했습니다.")
        return result

    except :
        result = {"message" : False}
        print_log("VP검증에 실패했습니다.")
        return result
        



def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(verify())
    loop.close()



if __name__ == '__main__':
    main()