# from utils import *

# import os
# from glob import glob #遍历文件夹下的所有文件
# from langchain.vectorstores.chroma import Chroma
# from langchain_community.document_loaders import CSVLoader, PyMuPDFLoader, TextLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# def doc2vec():
#     # 定义文本分割器
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size = 800, #块的大小
#         chunk_overlap = 80 #重叠部分
#     )

#     # 读取并分割文件
#     dir_path = os.path.join(os.path.dirname(__file__), './data/inputs') #目录的路径
#     documents = []
#     for file_path in glob(dir_path + '*.*'):
#         loader = None
#         if '.csv' in file_path:
#             loader = CSVLoader(file_path,encoding='utf-8')
#         if '.pdf' in file_path:
#             loader = PyMuPDFLoader(file_path)
#         if '.txt' in file_path:
#             loader = TextLoader(file_path,encoding='utf-8')
#         if loader:
#             documents += loader.load_and_split(text_splitter)
#     print(documents)
#     # exit()

#     # print(get_embeddings_model())
#     # 向量化并存储
#     # if documents:
#     #     vdb = Chroma.from_documents(
#     #         documents = documents, 
#     #         embedding = get_embeddings_model(),
#     #         persist_directory = os.path.join(os.path.dirname(__file__), './data/db/') #持久化
#     #     )
#     #     vdb.persist()


#     if documents:
#         vdb = Chroma(
#             embedding_function = get_embeddings_model(),
#             persist_directory = os.path.join(os.path.dirname(__file__), './data/db/')
#         )
#         chunk_size = 10
#         for i in range(0, len(documents), chunk_size):
#             texts = [doc.page_content for doc in documents[i:i+chunk_size]]
#             metadatas = [doc.metadata for doc in documents[i:i+chunk_size]]
#             vdb.add_texts(texts, metadatas)
#         vdb.persist()


# if __name__ == '__main__':
#     doc2vec()



# 从特定目录读取文本文件（包括 CSV、PDF 和 TXT 文件），
# 将其分割成小块，然后将这些小块文本向量化并存储在一个持久化数据库中

from utils import *

import os
from glob import glob #遍历文件夹下的所有文件
from langchain.vectorstores.chroma import Chroma
from langchain_community.document_loaders import CSVLoader, PyMuPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def doc2vec():
    # 定义文本分割器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800, #块的大小
        chunk_overlap = 80 #重叠部分
    )
    # 读取并分割文件
    dir_path = os.path.join(os.path.dirname(__file__), './data/input/') #目录的路径
    documents = []

    for file_path in glob(dir_path + '*.*'):

        loader = None
        if '.csv' in file_path:
            loader = CSVLoader(file_path,encoding='utf-8')
        if '.pdf' in file_path:
            loader = PyMuPDFLoader(file_path)
        if '.txt' in file_path:
            loader = TextLoader(file_path,encoding='utf-8')
        if loader:
            documents += loader.load_and_split(text_splitter)

    if documents:
        vdb = Chroma(
            embedding_function = get_embeddings_model(),
            persist_directory = os.path.join(os.path.dirname(__file__), './data/db2')
        )
        chunk_size = 10
        for i in range(0, len(documents), chunk_size):
            texts = [doc.page_content for doc in documents[i:i+chunk_size]]
            metadatas = [doc.metadata for doc in documents[i:i+chunk_size]]
            vdb.add_texts(texts, metadatas)
            print(i)
        vdb.persist()
        print(1)

if __name__ == '__main__':
    doc2vec()
