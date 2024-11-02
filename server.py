from flask import Flask, jsonify,request
from agent import Agent
from werkzeug.urls import url_decode
  
app = Flask(__name__)
agent_1 = Agent()

def getMapFormatResult(flag,ans):
    res = {
        "code":"",
        "msg":"",
        "data":""
    }
    if flag != True:
        res = {
            # "code":"400",
            "msg":ans
        }
        return jsonify(res)
    res = {
        # "code":"200",
        "data":ans
    }
    return jsonify(res)
  
# 定义一个简单的路由处理函数  
@app.route('/Crop', methods=['GET'])
def hello_world():
    ans = ""
    try:
        msg = request.args.get('msg')
        ans = agent_1.query(msg)
    except Exception as e:
        return getMapFormatResult(False,e)
    return getMapFormatResult(True,ans)
  
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=7777,debug=True)