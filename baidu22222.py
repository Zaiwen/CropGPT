from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from utils import get_llm_model


# 配置 ChromeDriver
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')  # 必需的参数，避免沙箱错误
    chrome_options.add_argument('--disable-dev-shm-usage')  # 共享内存不足问题



    driver = webdriver.Chrome(options=chrome_options)

    return driver


driver = init_driver()


# 百度学术查询函数
def search_baidu_scholar(query):
    driver.get("https://xueshu.baidu.com/")
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input#kw"))
    )
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = []
    for item in soup.find_all('div', class_='result')[:5]:
        title = item.find('h3', class_='t').text
        link = item.find('h3', class_='t').find('a')['href']
        results.append({'title': title, 'link': link})

    results2 = []
    for i, result in enumerate(results):
        driver.get(result['link'])

        # 等待页面加载
        time.sleep(3)  # 可以根据需要调整为WebDriverWait

        soup1 = BeautifulSoup(driver.page_source, 'html.parser')

        # title = soup1.find('div',class_='main-info').find('h3').text
        # print(title)
        title1=result['title']

        author = soup1.find('p', class_='author_text').text
        print(author)

        abstract = soup1.find('p', class_='abstract').text
        print(abstract)

        try:
            DOI = soup1.find('div', class_='doi_wr').text
        except Exception:
            DOI = '未给出'
        print(DOI)

        year = soup1.find('div', class_='year_wr').text
        print(year)

        journal = soup1.find('div', class_='container_right').find('a', class_='journal_title').text
        print(journal)

        results2.append({
            'title': title1,
            'author': author,
            'abstract': abstract,
            'DOI': DOI,
            'year': year,
            'journal': journal
        })

    return results2


# 定义LangChain的Prompt模板
template = """
你是一位学术研究专家。基于以下来自百度学术的文献摘要以及标题，使用中文给出一个清晰简洁的总结。
并且按照标准引用格式，给出总结中所使用到的文献，包含文献名称，作者，期刊来源，DOI，年份,文献链接URL:
使用中文进行回答
{results}

最后按照summary: 

reference:
1.Author: 作者名称
2.Title：文献名称
3.Journal：该文献来自哪本期刊或者会议
4.Year：发表年份
的格式给出回答
"""

prompt = PromptTemplate(
    input_variables=["results"],
    template=template,
)


# 构建LangChain
def generate_summary_from_academic_results(query):
    # Step 1: 查询百度学术
    baidu_results = search_baidu_scholar(query)

    # Step 2: 构建LLMChain并生成总结
    chain = LLMChain(llm=get_llm_model(), prompt=prompt)
    summary = chain.run(results=baidu_results)

    return summary


# 测试查询
query = "转座子的作用"
summary = generate_summary_from_academic_results(query)
print(summary)
