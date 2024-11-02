from flask import Flask, request,Response,jsonify
from flask.json import jsonify
from agent import Agent
from judge import JudgeMsg
app = Flask(__name__)

agent = Agent()
app.config['JSON_AS_ASCII'] = False

@app.route('/invoke', methods=['GET'])  # 定义一个具体的路由路径
def get_invoke():
    string1 = request.args.get('question')  # 从查询参数中获取 'question'
    print(string1)
    return agent.query(string1) if string1 else "No question provided"

@app.route('/CropGPT', methods=['GET']) 
def get_res():
    question = request.args.get('question')
    judge = JudgeMsg(question, agent)
    _type, response = judge.dealMsg()
    
    json_response = jsonify({'type': _type, 'response': response})
    return json_response


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5003)

