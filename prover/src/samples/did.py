import json


#sdk = Node를 제공해주는 did회사
#이후 필요한 값은 did와 wallet_handle에 접근하기 위한 wallet_config, wallet_credentials
sdk = {
        'did': 'PyVK9GNMH4mBmTZrdb6Uia',
        'wallet_config': json.dumps({'id': 'sdk_wallet'}),
        'wallet_credentials': json.dumps({'key': 'sdk_wallet_key'}),
        'pool_name': 'toilet_pool',
        'cred_def_id': 'EYYre24MSmo3tQwC9S1YWr:3:CL:EYYre24MSmo3tQwC9S1YWr:2:toilet:1.0:cred_def_tag'
    }


# issuer = End_Point(toilet_app_server)
issuer = {
        'did': 'EYYre24MSmo3tQwC9S1YWr',
        'wallet_config': json.dumps({'id': 'sdk_wallet'}),
        'wallet_credentials': json.dumps({'key': 'sdk_wallet_key'}),
        'pool_name': 'toilet_pool'
    }

prover = {
        'seed': '0000000000000000000000000prover2',
        'did' : 'GDJNoToAxu95mWvwgk2K2E',
        'wallet_config': json.dumps({'id': 'prover_wallet'}), #prover에 회원의 아이디가 들어간다.
        'wallet_credentials': json.dumps({'key': 'prover1_wallet_key'}),
        'pool_name': 'toilet_pool',
        'master_secret_id' : 'Jun'

}

verifier ={

}