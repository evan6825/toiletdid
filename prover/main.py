

from flask import Flask ,request



app = Flask(__name__) #flask프로젝트를 초기화시켜서 app에 저장 

@app.route('/',methods=['POST']) #앱에 주소
def hello_world(): #주소에 들어오면 이 함수를 실행
    return "Hello World!"



# @app.route('')



if __name__ == '__main__':
    app.run()
