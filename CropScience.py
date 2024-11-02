import glob
import os
import random
import string
from prompt import GET_KEY_TPL,CROP_TPL, ONLY_ABSTRACT_STR, RETRIVAL_PROMPT_TPL
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import requests
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils import get_embeddings_model, get_llm_model
from langchain_community.document_loaders import PyMuPDFLoader,CSVLoader,TextLoader
from langchain_community.vectorstores import Chroma
# 一些功能函数

# 配置玉米科学URL
crop_url = 'http://www.ymkx.com.cn/jms/ajax/search' 
# 配置请求头
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537/36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

vdb = Chroma(
        embedding_function=get_embeddings_model(),
        persist_directory=os.path.join(os.path.dirname(__file__), "./tempDB/vdb")
)

# 定义文档分割标准
text_spliter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 50
)


# 提取路径最后的唯一标识符
def getPdfLastName(strr):
    par = strr.split('?')
    path_str = par[0].split("/")
    return "./tempDB/data/"+path_str[-1] + '.pdf'

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

# 下载pdf
def download_pdf(url):
    # create_directory("./tempDB/data")
    # print("++++++++++++++++++++++++++++++++++++")
    # print("提取前",url)
    url = url[0:10] if len(url) > 10 else url
    print("提取后",url)
    base_url = 'http://www.ymkx.com.cn/'
    for i_url in url:
        filename = getPdfLastName(i_url)
        i_url = base_url + i_url
        try:
            print(i_url)
            # 发送GET请求
            response = requests.get(i_url, stream=True)
            # 检查请求是否成功
            if response.status_code == 200:
                # 将内容写入文件
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"PDF文件已保存为 {filename}")
            else:
                print(f"请求失败，状态码：{response.status_code}")
        except Exception as e:
            print(f"下载过程中出现错误: {e}")

# 清空CropText文件夹
def clear_directory(directory_path):
    files = glob.glob(os.path.join(directory_path, '*'))
    for file_path in files:
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"删除文件 {file_path} 时出错: {e}")
        elif os.path.isdir(file_path):
            clear_directory(file_path)
            os.rmdir(file_path)


# 拿到目标文件夹路径，并分割其中文档
def loadFile(file_path):
    documents = [] # 装文档内容用
    loader = None # 声明一个加载器
    files_list = os.listdir(file_path) # 获取指定目录下的所有文件名
    for ele in files_list:
        if ele.lower().endswith('.pdf'):
            loader = PyMuPDFLoader(file_path+'/'+ele)
        elif ele.lower().endswith('.csv'):
            loader = CSVLoader(file_path+'/'+ele,encoding='utf-8')
        elif ele.lower().endswith('.txt'):
            loader = TextLoader(file_path+'/'+ele,encoding='utf-8')
    
        if loader:
            documents += loader.load_and_split(text_spliter)
    return documents

# 将分割完成后的文档进行向量化
def embeddingText(filePath):
    try:
        documents = loadFile(filePath)
        chunk_size = 10
        for i in range(0, len(documents), chunk_size):
            texts = [doc.page_content for doc in documents[i:i + chunk_size]]
            metadatas = [doc.metadata for doc in documents[i:i + chunk_size]]
            vdb.add_texts(texts, metadatas)
            print(i)
        vdb.persist()
        print("完成向量化")
    except Exception as e:
        print(f"向量化过程中出错: {e}")

# 查询向量化库
def queryTemp_Vdb(query):
    # 执行查询
    results = vdb.similarity_search_with_relevance_scores(query, k=3)
    print(results)

    query_result = [doc[0].page_content for doc in results if doc[1]>0.4]

    prompt = PromptTemplate.from_template(RETRIVAL_PROMPT_TPL)
    retrival_chain = LLMChain(
        llm = get_llm_model(),
        prompt = prompt,
        verbose = True
    )
    inputs = {
        'query': query,
        'query_result': '\n\n'.join(query_result) if len(query_result) else '没有查到'
    }
    return retrival_chain.invoke(inputs)['text']

# 提取用户问题中的关键词
def getKeyWords(query):
    prompt = PromptTemplate.from_template(GET_KEY_TPL)
    chain = LLMChain(
        llm = get_llm_model(),
        prompt = prompt,
        verbose = True
    )
    input = {
        'query':query
    }
    res = chain.invoke(input)['text']
    return res

# 根据关键词获取玉米科学的文章信息（标题、摘要、pdf_url）
def getAbstractArr(keyWords):
    all_data = []
    for key in keyWords:
        body_day = {
            'key' : key
        }
        response = requests.post(crop_url,data=body_day,headers=headers)
        if response.status_code != 200:
            print("请求失败")
        # 获取返回的数据并格式化处理
        res = response.text
        res_data = json.loads(res)
        if res_data['records'] != '0':
            for ele in res_data['rows']:
                all_data.append({'title':ele['title'],'abstract':ele['abstract'],'pdf_url':ele['pdf_url']})
    return all_data


# 随机生成向量库名称
def generate_random_folder_name(length=5):
    # 定义文件夹名称可能包含的字符集
    characters = string.ascii_letters + string.digits
    # 随机选择指定长度的字符
    random_folder_name = ''.join(random.choice(characters) for _ in range(length))
    return random_folder_name

# 查询玉米科学网工具函数
def queryCropScience(msg):
    # 提取关键词组
    keyWords = getKeyWords(msg)
    print(keyWords)
    keyWordss = keyWords.split(":")
    print(keyWordss)
    keyWords_arr = keyWordss[1].split('、')
    print('用户问题中的关键词组',keyWords_arr)

    # 拿到相关文献 标题、摘要、数据
    abstract_arr = getAbstractArr(keyWords_arr)
    abstract_arr = abstract_arr[:10] if len(abstract_arr) > 10 else abstract_arr

    # 获取文献pdf路径，并准备下载
    url = []
    for ele in abstract_arr:
        url.append(ele['pdf_url'])
    if url != []:
        clear_directory("./tempDB/data")
        download_pdf(url)
        # vdb_name = generate_random_folder_name()
        embeddingText("./tempDB/data")
        return queryTemp_Vdb(msg)
    
    return 'i do not konw'

def getAbstract(msg):
    # 提取关键词组
    keyWords = getKeyWords(msg)
    print(keyWords)
    keyWordss = keyWords.split(":")
    print(keyWordss)
    keyWords_arr = keyWordss[1].split('、')
    print('用户问题中的关键词组',keyWords_arr)

    # 拿到相关文献 标题、摘要、数据
    abstract_arr = getAbstractArr(keyWords_arr)
    print("------------------摘要数据-----------------",abstract_arr)
    abstract_arr = abstract_arr[:5] if len(abstract_arr) > 5   else abstract_arr

    abs_str = ""
    for ele in abstract_arr:
        abs_str += ele["abstract"]

    prompt = PromptTemplate.from_template(ONLY_ABSTRACT_STR)
    my_chain = LLMChain(
        llm = get_llm_model(),
        prompt=prompt,
        verbose=True
    )
    inputs = {
        "msg":abs_str,
        "question":msg
    }

    return my_chain.invoke(inputs)['text']
    
    