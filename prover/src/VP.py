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

    prover['get_schema_request'] = await ledger.build_get_schema_request(sdk['did'],schema['schema_id'])

    prover['schema'] = await ledger.submit_request(sdk['pool'],prover['get_schema_request'])

    prover['get_cred_def_req'] = await ledger.build_get_cred_def_request(sdk['did'],schema['cred_def_id'])

    prover['cred_def'] = await ledger.submit_request(sdk['pool'],prover['get_cred_def_request'])

    prover['get_revoc_reg_def_req'] = await ledger.build_get_revoc_reg_def_request(sdk['did'],)

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(VP())
    loop.close()


if __name__ == '__main__':
    main()
