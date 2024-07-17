import gradio as gr
from service import Service

def agriculture_bot(message, history):
    service = Service()
    return service.answer(message, history)

css = '''
.gradio-container { max-width:850px !important; margin:20px auto !important;}
.message { padding: 10px !important; font-size: 14px !important;}
'''

demo = gr.ChatInterface(
    css = css,
    fn = agriculture_bot, 
    title = '基于知识图谱的农业大模型',
    chatbot = gr.Chatbot(height=400, bubble_full_width=False),
    theme = gr.themes.Default(spacing_size='sm', radius_size='sm'),
    textbox=gr.Textbox(placeholder="在此输入您的问题", container=False, scale=7),
    examples = ['培育适合机械化生产的鲜食玉米品种', '不同施肥处理对玉米品质的影响 ','预测一下河北地区的农作物在example1.txt 文件中所记录的株高','云苓是什么植物','云苓属于什么类别','紫背天葵是什么植物','白屈菜结什么样的果实？','墨西哥玉米结什么样的果实？','墨西哥玉米属于什么类别？','我打算在湖南省的黄绵土上进行有机耕作，应该选择哪些作物品种比较合适？','请问预测接下来在云南省是否有大范围的干旱发生的可能性？','我在河北省有一块土地，土壤类型为沙壤土，最近的天气预报显示温度会在22°C到30°C之间，我想知道如果现在播种玉米，它们的生长趋势如何？','我发现我的小麦田里有蚜虫出现，该如何处理？','在春季，哪些蔬菜作物的种植最佳实践需要特别注意？','当前大豆的市场价格是多少？预计下个季度的价格走势如何？'],
    submit_btn = gr.Button('提交', variant='primary'),
    clear_btn = gr.Button('清空记录'),
    retry_btn = None,
    undo_btn = None,
)

if __name__ == '__main__':
    demo.launch(share=True)