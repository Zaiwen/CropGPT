
from utils import *

from prompt import *

import os


from langchain.chains import LLMChain, LLMRequestsChain
from langchain.prompts import PromptTemplate
from langchain.vectorstores.chroma import Chroma
import sys
from langchain_community.embeddings import XinferenceEmbeddings


def retrival_func(query):
    # 召回并过滤文档

    bgelarge = XinferenceEmbeddings(server_url="http://12.12.12.101:9997", model_uid="custom-bge-large-zh")
    documents = Chroma(
        persist_directory=os.path.join(os.path.dirname(__file__), './data/db4'),
        embedding_function=bgelarge
    ).similarity_search_with_relevance_scores(query, k=5)

    print(documents)
    query_result = [doc[0].page_content for doc in documents if doc[1] > 0.5]
    # 填充提示词并总结答案
    prompt = PromptTemplate.from_template(RETRIVAL_PROMPT_TPL)
    retrival_chain = LLMChain(
        llm=get_llm_model(),
        prompt=prompt,
        verbose=os.getenv('VERBOSE')
    )
    inputs = {
        'query': query,
        'query_result': '\n\n'.join(query_result) if len(query_result) else '没有查到'
    }
    return retrival_chain.invoke(inputs)['text']
if __name__ == '__main__':
    print(retrival_func(query="The Impact of Mulching Drip Irrigation and Nitrogen Application on the Growth and Yield of Summer Maize in Arid Regions"))