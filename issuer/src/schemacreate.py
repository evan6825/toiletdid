import asyncio
import json
import pprint

from indy import pool, ledger, wallet, did, anoncreds
from indy.error import IndyError, ErrorCode

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION
from walletcreate import write_nym_and_query_verkey
from samples import sdk,issuer

# issuer = sdk
schema = {
        'name': 'toilet',
        'version': '1.0',
        'attributes': '["gender", "phone", "name"]'
}
async def schema_build_and_request():
    # issuer = await write_nym_and_query_verkey()
    issuer['pool'] = await pool.open_pool_ledger(issuer['pool_name'], None)
    issuer['wallet'] = await wallet.open_wallet(issuer['wallet_config'], issuer['wallet_credentials'])

    issuer['schema_id'], issuer['schema'] = await anoncreds.issuer_create_schema(issuer['did'], schema['name'],
                                                                                 schema['version'],
                                                                                 schema['attributes'])
    
    
    cred_def = {
        'tag': 'cred_def_tag',
        'type': 'CL',
        'config': json.dumps({"support_revocation": False})
    }
    
    issuer['schema_req'] = await ledger.build_schema_request(issuer['did'],issuer['schema'])
    issuer['schema_res'] = \
        await ledger.sign_and_submit_request(issuer["pool"],
                                            issuer["wallet"],
                                            issuer["did"],
                                            issuer["schema_req"])
    issuer['cred_def_tag'] = 'TAG1'
    issuer['cred_def_type'] = 'CL'
    issuer['cred_def_config'] = json.dumps({"support_revocation": False})


    (issuer['cred_def_id'],issuer['cred_def']) = \
        await anoncreds.issuer_create_and_store_credential_def(issuer['wallet'],
                                                                issuer['did'], #여기부분을 steward_did로 수정
                                                                issuer['schema'],
                                                                cred_def['tag'],
                                                                cred_def['type'],
                                                                cred_def['config'])
    await wallet.close_wallet(issuer['wallet'])
    await pool.close_pool_ledger(issuer['pool'])
    print("schema")
    print(issuer["schema"])
    print("cred_def")
    print(issuer['cred_def'])


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(schema_build_and_request())
    loop.close()


if __name__ == '__main__':
    main()
