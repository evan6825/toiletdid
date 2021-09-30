
import VC as VC1
import maleVP as maleVP
import femaleVP as femaleVP
import maleverify as verify1
import femaleverify as verify2

from flask import Flask, request


app = Flask(__name__)


@app.route("/")
def main():
   return "<h1>Hello world!</h1>"


@app.route('/VC', methods = ["POST"])
async def user_VC():
   if request.is_json :
      params = request.get_json() #서버에서 보내준 회원의정보
   a =  await VC1.VC1(params)
   return a


@app.route('/VP1', methods = ["POST"])
async def male_VP():
   if request.is_json:
    params = request.get_json()
   a = await maleVP.VP1(params)
   return a


@app.route('/VP2', methods = ["POST"])
async def female_VP():
   if request.is_json:
    params = request.get_json()
   a = await femaleVP.VP1(params)
   return a


@app.route('/verify', methods = ["POST"])
async def verify():
   if request.is_json:
      params = request.get_json()
      if params["gender"] == "male" :
         a = await verify1.verify(params)
      elif params["gender"] == "female" :
         a = await verify2.verify(params)
   return a





host_addr = "0.0.0.0"
port_num = "5000"

if __name__ == "__main__":
   app.run(host=host_addr,port=port_num)
