from dotenv import load_dotenv
load_dotenv()
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatBaichuan
from langchain_community.embeddings import BaichuanTextEmbeddings
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from py2neo import Graph
from config import *
import os

# def get_embeddings_model():
#     model_map = {
#         'openai': OpenAIEmbeddings(
#             model = os.getenv('OPENAI_EMBEDDINGS_MODEL')
#         ),
#         'baichuanai': BaichuanTextEmbeddings(),
#     }
#     return model_map.get(os.getenv('EMBEDDINGS_MODEL'))
import chromadb
from chromadb.utils import embedding_functions
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings

baichuanai_ef = embedding_functions.BaichuanAIEmbeddingFunction(
    api_key="sk-b7f752076296ddf6c77557420b711473",
    model_name="baichuanai"
)
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size = 800, #块的大小
#     chunk_overlap = 80 #重叠部分
# )
# # 读取并分割文件
# dir_path = os.path.join(os.path.dirname(__file__), './data/inputs/') #目录的路径
# documents = []
# for file_path in glob(dir_path + '*.*'):
#     loader = None
#     if '.csv' in file_path:
#         loader = CSVLoader(file_path,encoding='utf-8')
#     if '.pdf' in file_path:
#         loader = PyMuPDFLoader(file_path)
#     if '.txt' in file_path:
#         loader = TextLoader(file_path,encoding='utf-8')
#     if loader:
#         documents += loader.load_and_split(text_splitter)
# print(documents)
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="my_collection",embedding_function=baichuanai_ef)
# 使用enumerate来获取索引和文档文本，但是只为了计算文档的数量
for index, doc in enumerate(documents, start=1):
    pass

# 基于上面计算出的文档数量来生成ids列表
ids = [f"id{index}" for index in range(1, len(documents) + 1)]
collection.add(
    documents=[
        "This is a document about hhhhhhh",
        "This is a document about abjasfkgdhbgdjgk"
    ],
    ids=["id1", "id2"],
)
results = collection.query(
    query_texts=["This is a query document about saodjigo"], # Chroma will embed this for you
    n_results=2 # how many results to return
)
chromadb.PersistentClient(path="./data/tizi365.db")
print(results)

# from sentence_transformers import SentenceTransformer

# model = SentenceTransformer("BAAI/bge-large-zh-v1.5")