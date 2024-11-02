import time

import gradio as gr
import re
from agent import Agent
from service import Service

clean=False

agent = Agent()

dnafile='example.txt'
def agriculture_bot(message, history,dna_sequence):
    global clean
    if clean:
        print("yes")
        del history[-2:]

    if(len(message)==0 and len(dna_sequence) and re.fullmatch(r'([ATGC]+)', dna_sequence)):
        with open(dnafile, "w") as f:  
            f.write(dna_sequence)
        clean=True
        

    elif(len(message) and len(dna_sequence) and re.fullmatch(r'([ATGC]+)', dna_sequence)):
        with open(dnafile, "w") as f:  
            f.write(dna_sequence)
        print('写入成功！！')
        #文件写入成功后，可以继续按照源流程调用表型预测工具
        service = Service()
        clean=False
        return service.answer(message, history)

    elif(len(dna_sequence) and not re.fullmatch(r'([ATGC]+)', dna_sequence)):
        clean=True
        return '请输入正确的DNA序列😄'

    elif(len(message)==0 and len(dna_sequence)==0):
        clean=True
        return '请输入您的问题😀'

    else:
        # service = Service()
        clean=False
        # return service.answer(message, history)
        return agent.query(message)

css = '''
.gradio-container {
    max-width: 1800px !important;
    margin: 20px auto !important;
    font-family: 'Arial', sans-serif;
    background-color: lightblue;
    background-image: url('https://s2.loli.net/2024/07/20/UbBhnZxyvj1YrMT.jpg'); /* 替换为你的图片路径 */  
    background-repeat: no-repeat;  
    background-size: 1800px 1600px;  
    background-position: bottom;  

    border-radius: 10px;
    border: 4px solid #ccc;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.message {
    padding: 10px !important;
    font-size: 14px !important;
}
h1 {
    background-image: url('https://s2.loli.net/2024/07/24/cdbDuwfPiLA697N.png');
    background-repeat: no-repeat;  
    background-size:260px 45px;
    background-position:right;
    font-size: 35px;
    color: #000080;
    text-align: center;
    margin-bottom: 20px;
}

.chatbox {
    background-color: #FFFFF0;
    background-repeat: no-repeat;  
    border: 2px solid #ccc;
    background-size:22%,22%;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.textbox {
    color: 	#008B45;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px;
}

#submit-btn, #clear-btn {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    border-radius: 5px;
    margin-top: 10px;
}
.submit-btn {
    background-color: #4CAF50;
    color: #228B22;
    border: none;
    font-size: 22px;
}
#clear-btn {
    background-color: #f44336;
    color: white;
    border: none;
    font-size: 16px;
}
.example_word{
    color:#A020F0
    font-size: 19px;
}

footer {visibility: hidden}
'''

demo = gr.ChatInterface(
    css=css,
    fn=agriculture_bot,
    title='CropGPT v1.0 ',
    chatbot=gr.Chatbot(height=400, bubble_full_width=False
                       , avatar_images=('image/man.jpg'
                                        , 'image/robot.jpg'),
                       elem_classes="chatbox"),
    theme=gr.themes.Default(spacing_size='sm', radius_size='sm'),
    textbox=gr.Textbox(placeholder="在此输入您的问题", container=False, scale=7, elem_classes="textbox"),
    additional_inputs=[
        gr.Textbox(placeholder="请输入正确的DNA序列",max_lines=30, label="dna_sequence"),  # 添加一个文本输入框，用于输入系统提示
    ],
    examples=[['适合温室栽培的玉米品种有哪些'], ['玉米是属于哪一科的植物'], ['玉米种子有几部分组成？'],
              ['适合玉米生长的温度湿度'], ['中国玉米的主要种植区域是哪里？'], ['代森锰锌主要治什么病？'],
              ['华中农业大学选育的玉米品种有哪些'], ['玉米如何烹饪'], ['如何使用玉米制作爆米花'],
              ['不同施肥处理对玉米品质的影响 '], ['干旱胁迫对玉米生长的影响'],
              ['请根据当前的基因序列，预测河北地区本作物的开花期'], ['黑糯305的生育期'],
              ['黑糯305的百粒重'], ['先玉2036的穗长'], ['先玉2036的播种时间'], ['先玉2036的播种密度'], ['云苓是什么植物'],
              ['膨大剂属于哪种植物生长调节剂？'], ['不同区域的小麦杂交育种应注意什么要点,以获得较高的产量?'],
              ['紫背天葵是什么植物'],
              ['爬山虎是什么类型的植物'], ['我打算在湖南省的黄绵土上进行有机耕作，应该选择哪些作物品种比较合适？'],
              ['请问预测接下来在云南省是否有大范围的干旱发生的可能性？'],
              ['我发现我的小麦田里有蚜虫出现，该如何处理？'],
              ['当前大豆的市场价格是多少？预计下个季度的价格走势如何？']],
    submit_btn=gr.Button('🌽提 交🌽', variant='primary', elem_classes="submit-btn"),
    retry_btn=gr.Button('🔄重试一次'),
    undo_btn=gr.Button('↩️撤回'),
    clear_btn=gr.Button('🗑️清空记录'),
    concurrency_limit=1,
    # retry_btn = None,
    # undo_btn = None,
)

if __name__ == '__main__':
    demo.launch(share=True,server_name='0.0.0.0')