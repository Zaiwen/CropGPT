
from utils import get_llm_model
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agent import Agent

# 提取用户消息类型
FORMAT_TPL = """
请根据用户输入判断用户消息类型，类型取值从[chat、interaction]中选择。
chat : 代表问答类型消息
interaction : 代表需要执行动作的消息
例如:
用户问题:黑糯305的生育期为?\n输出:chat
用户问题:我想要一个喝的\n输出:interaction
用户问题:干旱胁迫对玉米生长的影响\n输出:chat
用户问题:请给我一个黑糯玉米\n输出:interaction
用户问题:我渴了\n输出:interaction
用户问题:黑糯玉米\n输出:chat
用户问题:我饿了\n输出:interaction
用户问题:今天天气真好\n输出:chat
用户问题:你好\n输出:chat
用户问题:带皮黄玉米\n输出:chat

用户问题:{question}
输出:
"""

JUDGE_TPL = """
根据用户消息分析用户所需要的物体是否在物体列表中存在。
如果存在，返回该满足条件的物体名称；否则，返回“None”。
最后返回的结果不要加上"输出:"。

例如:
用户消息:我需要黑糯玉米\n物体列表:['黄玉米','黑糯']\n输出:黑糯
用户消息:我渴了\n物体列表:['黄玉米','黑糯','稀饭']\n输出:稀饭
用户消息:我渴了\n物体列表:['黑糯']\n输出:None
用户消息:我饿了\n物体列表:['黄玉米','黑糯']\n输出:黄玉米、黑糯
用户消息:我需要一个好看的玉米\n物体列表:['黄玉米','黑糯','花糯']\n输出:花糯
用户消息:我需要富含维生素C的食物\n物体列表:['猪肉','胡萝卜']\n输出:胡萝卜

用户消息:{question}
物体列表:{object_list}
输出:
"""

Answer_right_TPL = """
根据答案判断前一个大模型是否回答了用户问题。
如果回答了，返回true,否则返回false
最终输出只需给出true或者false中的一个

例如:
用户消息:黑糯305的生育期\n答案:91天左右\n输出:true
用户消息:先玉2036的百粒重\n答案:抱歉，暂时无法解答\n输出:false
用户消息:黑糯是什么\n答案:对不起，我未能找到关于黑糯的具体品种信息，它可能需要更详细的描述或者我可能需要检索其他工具。请提供更多信息，以便我能提供准确的帮助。\n输出:false
用户消息:您好\n答案:你好\n输出:true
用户消息:什么食物富含维生素A\n答案:对不起，我未能找到相关资料\n输出:false
用户消息:你是谁\n答案:我是来自华中农业大学信息学院的智能机器人，你可以称呼我为小智。我可以帮助你解答关于玉米以及其他一些问题，有什么我可以帮助你的吗？\n输出:true

用户消息:{question}
答案:{answer}
输出:
"""

class JudgeMsg():
    def __init__(self,msg,agent) -> None:
        self.vocablery = ["花糯","黑糯","黄带皮玉米","花糯带皮玉米","黄玉米","玉米粥"]
        self.msg = msg.strip()
        self.FORMAT_TPL = FORMAT_TPL
        self.agent = agent

    # 统一定义思维链
    def get_chain(self,prompt):
        model = get_llm_model()
        _prompt = PromptTemplate.from_template(prompt)
        _chain = LLMChain(
            llm = model,
            prompt = _prompt,
            verbose = True
        )
        return _chain
    
    # 判断用户消息类型
    def getAtttribute(self):
        _chain = self.get_chain(FORMAT_TPL)
        input = {
            "question" : self.msg
        }
        _type = _chain.invoke(input)['text']
        return _type
    
    # 问答消息获取答案
    def getAnser(self):
        return self.agent.query(self.msg)
    
    # 判断用户需要物体是否存在，存在即返回物体，否则返回None
    def judgeObjectExist(self):
        _chain = self.get_chain(JUDGE_TPL)
        input = {
            'question' : self.msg,
            'object_list' : self.vocablery
        }
        return _chain.invoke(input)['text']

    # 借助大模型推理用户需要的物体
    def getObject(self):
        pass
    
    # 统一入口
    def dealMsg(self):
        if self.msg == '':
            return 'None','None'
        
        # 判别消息类型和
        _type = self.getAtttribute()

        if _type.__contains__("chat"):
            # 如果是普通聊天
            ans = self.getAnser()
            _check = self.judgeAnswerIsRight(ans)
            print("================",_check)
            if _check.__contains__("false"):
                return 'chat',self.Killer()
            return 'chat',ans
        elif _type.__contains__("interaction"):
            # 如果是交互
            res = self.judgeObjectExist()
            if res.__contains__("None"):
                return "chat","None"
            return "interaction",res
    
    # 判断CropGPT是否给出最终答案
    def judgeAnswerIsRight(self,ans):
        _chain = self.get_chain(Answer_right_TPL)
        input = {
            'question' :self.msg,
            'answer':ans
        }
        return _chain.invoke(input)['text']


    # 杀手锏
    def Killer(self):
        model = get_llm_model()
        return model(self.msg).content
            
    
if __name__ == "__main__":
    agent = Agent()
    judge = JudgeMsg("我渴了",agent)
    _type,response = judge.dealMsg()
    _data = {
        "type" : _type,
        "response" : response
    }
    print(_data)