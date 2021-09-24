
import VC as VC1
import VP as VP1
import verify as verify1


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


@app.route('/VP', methods = ["POST"])
async def user_VP():
   if request.is_json:
    params = request.get_json()
   a = await VP1.VP1(params)
   return a


@app.route('/verify1', methods = ["POST"])
async def verify_male():
   if request.is_json:
    params = request.get_json()
   a = await verify1.verify(params)
   return a




host_addr = "0.0.0.0"
port_num = "5000"

if __name__ == "__main__":
   app.run(host=host_addr,port=port_num)
