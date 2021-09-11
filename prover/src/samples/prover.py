import json

prover_information = json.dumps({
    "gender": {"raw": "male", "encoded": "100"},
    "Phone": {"raw": "01022126825", "encoded": "01022126825"},
    "name": {"raw": "junhong", "encoded": "123123123123"}
})

#데이터가 들어올때 이 페이지에서 raw칸의 정보와 encoded의 정보가 바뀌도록하기
"""
    기입양식 예제
    cred_values_json = json.dumps({
        "sex": {"raw": "male", "encoded": "5944657099558967239210949258394887428692050081607692519917050011144233"},
        "name": {"raw": "준홍", "encoded": "1139481716457488690172217916278103335"},
        "height": {"raw": "175", "encoded": "175"},
        "age": {"raw": "28", "encoded": "28"}
        })
"""
