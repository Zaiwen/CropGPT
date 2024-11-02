from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatBaichuan
from langchain_community.embeddings import BaichuanTextEmbeddings
from langchain_community.chat_models import ChatZhipuAI
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from py2neo import Graph
from config import *
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.embeddings import XinferenceEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

# 向量化模型
def get_embeddings_model():
    model_map = {
        'openai': OpenAIEmbeddings(
            model = os.getenv('OPENAI_EMBEDDINGS_MODEL')
        ),
        'baichuanai': BaichuanTextEmbeddings(),
        # 'bge-large': HuggingFaceBgeEmbeddings(
        #     model_name="BAAI/bge-large-zh",
        #     model_kwargs={'device': 'cpu'},
        #     encode_kwargs={'normalize_embeddings': True}
        # )
        'Xinference':XinferenceEmbeddings(server_url="http://12.12.12.101:9997", model_uid="custom-bge-m3")
    }
    return model_map.get(os.getenv('EMBEDDINGS_MODEL'))

# 对话大模型
def get_llm_model():
    model_map = {
        'openai': ChatOpenAI(
            model = os.getenv('OPENAI_LLM_MODEL'),
            temperature = os.getenv('TEMPERATURE'),
            max_tokens = os.getenv('MAX_TOKENS'),
        ),
        'baichuan': ChatBaichuan(
            model = os.getenv('BAICHUAN_LLM_MODEL'),
            temperature = os.getenv('TEMPERATURE'),
        ),
        'zhipuai':ChatZhipuAI(
            model = os.getenv('ZHIPUAI_LLM_MODEL'),
            temperture = os.getenv('TEMPERTURE'),
        )
#        'qwen':ChatTongyi(
#            model = os.getenv('QWEN_LLM_MODEL'),
#            temperture = os.getenv('TEMPERTURE'),
#        )
    }
    return model_map.get(os.getenv('LLM_MODEL'))


def structured_output_parser(response_schemas):
    text = '''
    请从以下文本中，抽取出实体信息，并按json格式输出，json包含首尾的 "```json" 和 "```"。
    以下是字段含义和类型，要求输出json中，必须包含下列所有字段：\n
    '''
    for schema in response_schemas:
        text += schema.name + ' 字段，表示：' + schema.description + '，类型为：' + schema.type + '\n'
    return text


def replace_token_in_string(string, slots):
    for key, value in slots:
        string = string.replace('%'+key+'%', value)
    return string


def get_neo4j_conn():
    return Graph(
        os.getenv('NEO4J_URI'), 
        auth = (os.getenv('NEO4J_USERNAME'), os.getenv('NEO4J_PASSWORD'))
    )

if __name__ == '__main__':
    llm_model = get_llm_model()
    print(llm_model.invoke('中国玉米的主要种植区域是哪里？'))