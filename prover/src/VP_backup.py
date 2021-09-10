import asyncio
import json
import pprint

from indy import pool, ledger, wallet, did, anoncreds
from indy.error import IndyError, ErrorCode
from samples.did import sdk,issuer,prover
from samples.schema import schema
from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION


async def VP():
    await pool.set_protocol_version(PROTOCOL_VERSION)
    sdk['pool'] = await pool.open_pool_ledger(sdk['pool_name'], None)
    sdk['wallet'] = await wallet.open_wallet(sdk['wallet_config'], sdk['wallet_credentials'])
    prover['wallet'] = await wallet.open_wallet(prover['wallet_config'], prover['wallet_credentials'])


    nonce = await anoncreds.generate_nonce()
    sdk['proof_req'] = json.dumps({
        'nonce': nonce,
        'name': 'proof_req_1',
        'version': '0.1',
        'requested_attributes': {
            'attr1_referent': {'name': 'name'}
        },
        'requested_predicates': {
            'predicate1_referent': {'name': 'gender', 'p_type': '>', 'p_value': 99}
        }
    })
    prover['proof_req'] = sdk['proof_req']

    prover["search_handle"] = \
        await anoncreds.prover_search_credentials_for_proof_req(prover['wallet'],prover["proof_req"],None)

    creds_for_attr1 = await anoncreds.prover_fetch_credentials_for_proof_req(prover['search_handle'],
                                                                             'attr1_referent', 1)
    prover['cred_for_attr1']= json.loads(creds_for_attr1)[0]['cred_info']

    creds_for_predicate1 = await anoncreds.prover_fetch_credentials_for_proof_req(prover['search_handle'],
                                                                                  'predicate1_referent', 1)
    prover['cred_for_predicate1'] = json.loads(creds_for_predicate1)[0]['cred_info']

    await anoncreds.prover_close_credentials_search_for_proof_req(prover['search_handle'])


    prover['requested_creds'] = json.dumps({
        'self_attested_attributes': {},
        'requested_attributes': {'attr1_referent': {'cred_id': prover['cred_for_attr1']['referent'], 'revealed': True}},
        'requested_predicates': {'predicate1_referent': {'cred_id': prover['cred_for_predicate1']['referent']}}
    })



    schemas_json = json.dumps({schema['schema_id']: json.loads(schema['schema'])})
    cred_defs_json = json.dumps({schema['cred_def_id']: json.loads(schema['cred_def'])})
    revoc_ref_defs_json = "{}"
    revoc_regs_json = "{}"

    prover['proof'] = await anoncreds.prover_create_proof(prover['wallet'], prover['proof_req'],
                                                          prover['requested_creds'],
                                                          prover['master_secret_id'], schemas_json, cred_defs_json,
                                                          "{}")

    sdk['proof'] = prover['proof']

    proof = json.loads(sdk['proof'])

    return proof

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(VP())
    loop.close()


if __name__ == '__main__':
    main()
