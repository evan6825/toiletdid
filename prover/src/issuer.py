import asyncio
import json
import pprint


from indy import pool,ledger,wallet,did,anoncreds
from indy.error import IndyError, ErrorCode


import VC as VC1
import VP as VP1



from flask import Flask, request


app = Flask(__name__)


@app.route("/")
def main():
   return "<h1>Hello world!</h1>"


@app.route('/VC')
async def user_VC():
   print("test1")
   if request.is_json :
      params = request.get_json() #서버에서 보내준 회원의정보
   a =  await VC1.VC1(params)
   return a


@app.route('/VP')
async def user_VP():
   if request.is_json:
    params = request.get_json()
   a = await VP1.VP1(params)
   return a





host_addr = "127.0.0.1"
port_num = "8080"

if __name__ == "__main__":
   app.run(host=host_addr,port=port_num)
