import asyncio
import json
import pprint

from indy import pool, ledger, wallet, did, anoncreds
from indy.error import IndyError, ErrorCode
from samples.did import sdk,issuer
from samples.schema import schema, proof_schema
from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION
from samples.verfiy import params


async def verify():

    nonce = await anoncreds.generate_nonce()
    print("test1")
    proof= json.dumps({
        'nonce': nonce,
        'name': 'proof_req_1',
        'version': '0.1',
        'requested_attributes': {
            'attr1_referent': {'name': 'name'}
        },
        'requested_predicates': {
            'predicate1_referent': {'name': 'gender', 'p_type': '>=', 'p_value': 100}
        }
    })

    schemas_json = json.dumps({schema['schema_id']: json.loads(schema['schema'])})
    cred_defs_json = json.dumps({proof_schema['cred_def_id']: json.loads(proof_schema['cred_def'])}) 
    revoc_ref_defs_json = "{}"
    revoc_regs_json = "{}"
    print("test2")
    assert await anoncreds.verifier_verify_proof(proof, params, schemas_json, cred_defs_json,
                                                revoc_ref_defs_json, revoc_regs_json)

    print("true")
    return True




def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(verify())
    loop.close()



if __name__ == '__main__':
    main()