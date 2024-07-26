import gradio as gr
from service import Service

def agriculture_bot(message, history):
    service = Service()
    return service.answer(message, history)

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
    css = css,
    fn = agriculture_bot,
    title='狮子山大模型-CropGPT v1.0 ',
    chatbot = gr.Chatbot(height=400, bubble_full_width=False
            ,avatar_images=('https://s2.loli.net/2024/07/21/Mct8UDnWTgXVapH.jpg'
            ,'https://s2.loli.net/2024/07/21/KUOzfdua6GSVAIj.jpg'),elem_classes="chatbox"),
    theme = gr.themes.Default(spacing_size='sm', radius_size='sm'),
    textbox=gr.Textbox(placeholder="在此输入您的问题", container=False, scale=7,elem_classes="textbox"),
    examples = ['培育适合机械化生产的鲜食玉米品种', '不同施肥处理对玉米品质的影响 ','预测一下河北地区的农作物在example1.txt 文件中所记录的株高','云苓是什么植物','云苓属于什么类别','紫背天葵是什么植物','白屈菜结什么样的果实？','墨西哥玉米结什么样的果实？','墨西哥玉米属于什么类别？','我打算在湖南省的黄绵土上进行有机耕作，应该选择哪些作物品种比较合适？','请问预测接下来在云南省是否有大范围的干旱发生的可能性？','我在河北省有一块土地，土壤类型为沙壤土，最近的天气预报显示温度会在22°C到30°C之间，我想知道如果现在播种玉米，它们的生长趋势如何？','我发现我的小麦田里有蚜虫出现，该如何处理？','在春季，哪些蔬菜作物的种植最佳实践需要特别注意？','当前大豆的市场价格是多少？预计下个季度的价格走势如何？'],
    submit_btn = gr.Button('🌽提 交🌽', variant='primary',elem_classes="submit-btn"),
    retry_btn  = gr.Button('🔄重试一次'),
    undo_btn   = gr.Button('↩️撤回'),
    clear_btn = gr.Button('🗑️清空记录'),
    # retry_btn = None,
    # undo_btn = None,
)

if __name__ == '__main__':
    demo.launch(server_name='0.0.0.0',share=True)