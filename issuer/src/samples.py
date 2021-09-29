import json


#sdk = Node를 제공해주는 did회사
#이후 필요한 값은 did와 wallet_handle에 접근하기 위한 wallet_config, wallet_credentials
sdk = {
        'did': 'PyVK9GNMH4mBmTZrdb6Uia',
        'wallet_config': json.dumps({'id': 'sdk_wallet'}),
        'wallet_credentials': json.dumps({'key': 'sdk_wallet_key'}),
        'pool_name': 'toilet_pool'
    }


# issuer = End_Point(toilet_server)
issuer = {
        'did': 'EYYre24MSmo3tQwC9S1YWr',
        'wallet_config': json.dumps({'id': 'sdk_wallet'}),
        'wallet_credentials': json.dumps({'key': 'sdk_wallet_key'}),
        'pool_name': 'toilet_pool'
    }