from utils import *
from config import *
from prompt import *
from typing import Annotated
import subprocess
import os
import re
import onnx_model
from langchain.chains import LLMChain, LLMRequestsChain
from langchain.prompts import PromptTemplate
from langchain.vectorstores.chroma import Chroma
from langchain.vectorstores.faiss import FAISS
from langchain.schema import Document
from langchain.agents import ZeroShotAgent, AgentExecutor, Tool, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain import hub
from joblib import load


class Agent():
    def __init__(self):
        self.vdb = Chroma(
            persist_directory = os.path.join(os.path.dirname(__file__), './data/db'), 
            embedding_function = get_embeddings_model()
        )

    def generic_func(self, x, query):
        prompt = PromptTemplate.from_template(GENERIC_PROMPT_TPL)
        llm_chain = LLMChain(
            llm = get_llm_model(), 
            prompt = prompt,
            verbose = os.getenv('VERBOSE')
        )
        return llm_chain.invoke(query)['text']

    def retrival_func(self, x, query):
        # 召回并过滤文档
        documents = self.vdb.similarity_search_with_relevance_scores(query, k=5)
        print(documents)
        query_result = [doc[0].page_content for doc in documents if doc[1]>0.5]
        # 填充提示词并总结答案
        prompt = PromptTemplate.from_template(RETRIVAL_PROMPT_TPL)
        retrival_chain = LLMChain(
            llm = get_llm_model(),
            prompt = prompt,
            verbose = os.getenv('VERBOSE')
        )
        inputs = {
            'query': query,
            'query_result': '\n\n'.join(query_result) if len(query_result) else '没有查到'
        }
        return retrival_chain.invoke(inputs)['text']

    def graph_func(self, x, query):
        # 命名实体识别
        response_schemas = [
            ResponseSchema(type='list', name='crop', description='作物名称实体'),
            ResponseSchema(type='list', name='weather', description='天气名称实体')
        ]

        output_parser = StructuredOutputParser(response_schemas=response_schemas)
        format_instructions = structured_output_parser(response_schemas)

        ner_prompt = PromptTemplate(
            template = NER_PROMPT_TPL,
            partial_variables = {'format_instructions': format_instructions},
            input_variables = ['query']
        )

        ner_chain = LLMChain(
            llm = get_llm_model(),
            prompt = ner_prompt,
            verbose = os.getenv('VERBOSE')
        )

        result = ner_chain.invoke({
            'query': query
        })['text']
        
        ner_result = output_parser.parse(result)

        # 命名实体识别结果，填充模板
        graph_templates = []
        for key, template in CROP_GRAPH_TEMPLATE.items():
            slot = template['slots'][0]
            slot_values = ner_result[slot]
            for value in slot_values:
                graph_templates.append({
                    'question': replace_token_in_string(template['question'], [[slot, value]]),
                    'cypher': replace_token_in_string(template['cypher'], [[slot, value]]),
                    'answer': replace_token_in_string(template['answer'], [[slot, value]]),
                })
        if not graph_templates:
            return 
        
        # 计算问题相似度，筛选最相关问题
        graph_documents = [
            Document(page_content=template['question'], metadata=template)
            for template in graph_templates
        ]
        db = FAISS.from_documents(graph_documents, get_embeddings_model())
        graph_documents_filter = db.similarity_search_with_relevance_scores(query, k=3)
        # print(graph_documents_filter)

        # 执行CQL，拿到结果
        query_result = []
        neo4j_conn = get_neo4j_conn()
        for document in graph_documents_filter:
            question = document[0].page_content
            cypher = document[0].metadata['cypher']
            answer = document[0].metadata['answer']
            try:
                result = neo4j_conn.run(cypher).data()
                if result and any(value for value in result[0].values()):
                    answer_str = replace_token_in_string(answer, list(result[0].items()))
                    query_result.append(f'问题：{question}\n答案：{answer_str}')
            except:
                pass
            
        # 总结答案
        prompt = PromptTemplate.from_template(GRAPH_PROMPT_TPL)
        graph_chain = LLMChain(
            llm = get_llm_model(),
            prompt = prompt,
            verbose = os.getenv('VERBOSE')
        )
        inputs = {
            'query': query,
            'query_result': '\n\n'.join(query_result) if len(query_result) else '没有查到'
        }
        return graph_chain.invoke(inputs)['text']
    
    def translate_to_abbreviation(self, region_chinese, phenotype_chinese):
    # 这里是 translate_to_abbreviation 方法的示例实现
        region_abbreviations = {
            "河北": "HeB",
            "吉林": "JL",
            "辽宁": "LN",
            "北京": "BJ",
            "河南": "HN",
        } 
        phenotype_abbreviations = {
            "开花期": "DTT",
            "株高": "PH",
            "穗重": "EW",
        }
        region = region_abbreviations.get(region_chinese, None)
        phenotype = phenotype_abbreviations.get(phenotype_chinese, None)
        return region, phenotype

    def parse_query(self, query):
        # 使用正则表达式匹配地区、表型和文件名
        region_pattern = r"河北|吉林|辽宁|北京|河南"
        phenotype_pattern = r"开花期|株高|穗重"
        dna_pattern = r'([ATGC]+)'
        my_string = re.findall(dna_pattern, query, re.IGNORECASE)
        # file_pattern = r"example\d+\.txt"
        dna_sequence = ''.join(my_string)
        with open("example.txt", "w") as file:
            # 将字符串写入到文件中
            file.write(dna_sequence)
        region_match = re.search(region_pattern, query)
        phenotype_match = re.search(phenotype_pattern, query)
        # file_match = re.search(file_pattern, query)

        # 获取中文地区名和表型
        region_chinese = region_match.group(0) if region_match else None
        phenotype_chinese = phenotype_match.group(0) if phenotype_match else None
        # dna_sequence_file = file_match.group(0) if file_match else None
        dna_sequence_file = 'example.txt'
        
        # 将中文地区名和表型转换为英文缩写
        print(region_chinese,phenotype_chinese)
        region, phenotype = self.translate_to_abbreviation(region_chinese, phenotype_chinese)

        if not region or not phenotype or not dna_sequence_file:
            raise ValueError("无法从查询中提取足够的信息")

        return region, phenotype, dna_sequence_file

    def model_func(self,query):
        """
        调用外部作物预测模型进行预测
        region: 地区名
        phenotype: 作物类型
        dna_sequence_file: 文档标识符或文件名
        """
        prompt = PromptTemplate.from_template(MODEL_PROMPT_TPL)
        model_chain = LLMChain(
            llm = get_llm_model(),
            prompt = prompt,
            verbose = os.getenv('VERBOSE')
        )
        region, phenotype, dna_sequence_file = self.parse_query(query)
       
        # 构建用于调用外部脚本的命令
        script = r"C:\Users\Roied\Desktop\新建文件夹\Code\code\project\corn_demo\predict.py"
        input_file = f"C:\\Users\\Roied\\Desktop\\新建文件夹\\Code\\code\\project\\{dna_sequence_file}"
        command = f"python {script} {input_file} --diquname {region} --name {phenotype}"
        print(f"Executing command: {command}")

        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout.strip()  # 去除可能的首尾空白字符
            query_result = "预测结果为：" + output
            print(query_result)
            return query_result
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e.stderr}")
            query_result =f"预测过程中出错：{e.stderr}"

    def extract_dna_sequence(self,query):
        # DNA序列由字符集[A,T,G,C]组成
        dna_pattern = r'([ATGC]+)'
        dna_sequence = re.findall(dna_pattern, query, re.IGNORECASE)
        # 返回找到的所有DNA序列
        return dna_sequence

    def predict_func(self, query):
        prompt = PromptTemplate.from_template(PREDICT_PROMPT_TPL)
        dna_sequence = self.extract_dna_sequence(query)
        try:
            prediction = onnx_model.predict_with_onnx(dna_sequence)
            print(prediction)
            prediction_str = f"预测的启动子富集值: {prediction}"
            return prediction_str
        except Exception as e:
            # 如果出现错误，返回错误信息
            return f"预测时发生错误: {e}"
        
    def search_func(self, query):
        prompt = PromptTemplate.from_template(SEARCH_PROMPT_TPL)
        llm_chain = LLMChain(
            llm = get_llm_model(),
            prompt = prompt,
            verbose = os.getenv('VERBOSE')
        )
        llm_request_chain = LLMRequestsChain(
            llm_chain = llm_chain,
            requests_key = 'query_result'
        )
        inputs = {
            'query': query,
            'url': 'https://www.google.com/search?q='+query.replace(' ', '+')
        }
        return llm_request_chain.invoke(inputs)['output']

    # def weather_warning_predict(self, query):
    #     # 假设的气象预警处理逻辑
    #     return f"Weather warning prediction for: {query}"

    # def crop_growth_predict(self, query):
    #     # 假设的作物生长预测处理逻辑
    #     return f"Crop growth prediction for: {query}"    

    # def crop_variety_selection(self, query):
    #     # 假设的作物种类选择处理逻辑
    #     return f"crop variety selection: {query}" 

    # def agricultural_technical_consulting_tools(self, query):
    #     # 假设的回答关于农作物种植的问题，并提供最佳实践建议逻辑
    #     return f"Agricultural Technical Consulting Tools for: {query}"    

    # def crop_market_analysis_tools(self, query):
    #     # 假设的了解当前的农作物市场趋势，包括价格波动、需求预测和市场机会逻辑
    #     return f"crop market analysis tools: {query}" 
    
    # def Pest_monitoring_and_control(self, query):
    #     # 提供病虫害监测、预警和防治方案，帮助农民及时应对病虫害危害。
    #     return f"Pest monitoring and control: {query}" 


    # agent.py
    def parse_tools(self, tools, query):
        prompt = PromptTemplate.from_template(PARSE_TOOLS_PROMPT_TPL)
        llm_chain = LLMChain(
            llm = get_llm_model(),
            prompt = prompt,
            verbose = os.getenv('VERBOSE')
        )
        # 拼接工具描述参数
        tools_description = ''
        for tool in tools:
            tools_description += tool.name + ':' + tool.description + '\n'
        result = llm_chain.invoke({'tools_description':tools_description, 'query':query})
        # 解析工具函数
        for tool in tools:
            if tool.name == result['text']:
                return tool
        return tools[0]

    def query(self, query):
        tools = [
            Tool(
                name = 'generic_func',
                func = lambda x: self.generic_func(x, query),
                description = '可以解答通用领域的知识，例如打招呼，问你是谁等问题',
            ),
            Tool(
                name = 'retrival_func',
                func = lambda x: self.retrival_func(x, query),
                description = '与玉米相关的问题，或者问题里面包含玉米的字，就用该工具回答',
                # 询问玉米的相关现状，意义，实验等，
            ),
            # 用于回答水稻种植相关问题
            Tool(
                name = 'graph_func',
                func = lambda x: self.graph_func(x, query),
                description = '用于回答植物种类、类别相关问题',  
            ),
            # Tool(
            #     name = 'predict_func',
            #     func = self.predict_func,
            #     description = '用于回答给出一段DNA序列时预测启动富集值的问题，注意，该工具只预测富集值',
            # ),
            Tool(
                name = 'search_func',
                func = self.search_func,
                description = '其他工具没有正确答案时，通过搜索引擎，回答通用类问题',
            ),
            # Tool(
            #     name = 'model_func',
            #     func = self.model_func,
            #     description = '当用户问题中明确给出某地区玉米在的某个基因序列，需要表型的预测结果时，表型有株高，穗重，开花期三种，调用此模型，注意，该工具只预测某地区玉米序列的某个表型预测值，信息缺一不可。'
            # ),
            # Tool(
            #     name = 'weather_warning_predict',
            #     func = lambda x: self.weather_warning_predict(query),
            #     description = '用于回答气象预警，农田应该注意事项相关问题',
            # ),
            # Tool(
            #     name = 'crop_variety_selection',
            #     func = lambda x: self.crop_variety_selection(query),
            #     description = '根据地理位置和土壤条件推荐适合的作物品种,用于回答作物品种选择的问题',
            # ),
            # Tool(
            #     name = 'crop_growth_predict',
            #     func = lambda x: self.crop_growth_predict(query),
            #     description = '用于回答作物，在什么时间，什么环境下种植，作物的生长预测的问题',
            # ),
            # Tool(
            #     name = 'Pest_monitoring_and_control',
            #     func = lambda x: self.Pest_monitoring_and_control(query),
            #     description = '提供病虫害监测、预警和防治方案，帮助农民及时应对病虫害危害。',
            # ),
            # Tool(
            #     name = 'crop_market_analysis_tools',
            #     func = lambda x: self.crop_market_analysis_tools(query),
            #     description = '帮助了解当前的农作物市场趋势，包括价格波动、需求预测和市场机会。',
            # ),
            # Tool(
            #     name = 'agricultural_technical_consulting_tools',
            #     func = lambda x: self.agricultural_technical_consulting_tools(query),
            #     description = '回答关于农作物种植的问题，并提供最佳实践建议。',
            # )
        ]

        # tool = self.parse_tools(tools, query)
        # return tool.func(query)

        prompt = hub.pull('hwchase17/react-chat')
        # prompt.template = '请用中文回答问题！Final Answer 必须尊重 Obversion 的结果，不能改变语义。\n\n' + prompt.template
        prompt.template = '请用中文回答问题！Final Answer 不必考虑 Obversion ，不能改变语义。\n\n' + prompt.template
        agent = create_react_agent(llm=get_llm_model(), tools=tools, prompt=prompt)
        memory = ConversationBufferMemory(memory_key='chat_history')
        agent_executor = AgentExecutor.from_agent_and_tools(
            agent = agent, 
            tools = tools, 
            memory = memory, 
            handle_parsing_errors = True,
            verbose = os.getenv('VERBOSE')
        )
        return agent_executor.invoke({"input": query})['output']


if __name__ == '__main__':
    agent = Agent()