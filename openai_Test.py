from openai import OpenAI
# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://12.12.12.101:8080/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

chat_response = client.chat.completions.create(
    model="/home/zwfeng4/tyqw/qwen/Qwen1___5-14B-Chat/",
    messages=[
        {"role": "system", "content": "你是一个助手，只提供请求的具体信息，不添加额外的解释或细节."},
        {"role": "user", "content": "给我讲讲日常生活中的娱乐项目"},
    ],
    temperature=0.7,
    top_p=0.8,
    max_tokens=512,
)
print("Chat response:", chat_response.choices[0].message.content)