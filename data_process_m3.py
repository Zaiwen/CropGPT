from utils import *

import os
from glob import glob #遍历文件夹下的所有文件
from langchain.vectorstores.chroma import Chroma
from langchain_community.document_loaders import CSVLoader, PyMuPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
def doc2vec():
    # 定义文本分割器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 8000, #块的大小
        chunk_overlap = 20 #重叠部分
    )
    # 读取并分割文件
    documents = []
    for root, dirs, files in os.walk('./data/test'):
        for file in files:
            loader = None
            file_path = os.path.join(root, file)
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
            persist_directory = os.path.join(os.path.dirname(__file__), './data/m3_test')
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
