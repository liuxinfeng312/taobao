import random

import gradio as gr

from http import HTTPStatus
import dashscope
dashscope.api_key ='sk-eab2838a42bc4090a6fdee30392d19bb'
from dashscope import Generation
def call_stream_with_messages(query):
    messages = [
        {'role': 'user', 'content': query}]
    responses = Generation.call(
        'qwen-1.8b-chat',
        messages=messages,
        seed=random.randint(1, 10000),  # set the random seed, optional, default to 1234 if not set
        result_format='message',  # set the result to be "message"  format.
        stream=True,
        output_in_full=True  # get streaming output incrementally
    )
    full_content = ''
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            full_content += response.output.choices[0]['message']['content']

            yield response.output.choices[0]['message']['content']
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
# def chat_with_model(query):
#     # 使用模型进行回复
#     response = chat_pipeline(query=query, max_length=100, num_return_sequences=1)[0]['generated_text']
#     return response

# 定义输入和输出说明
examples = ["Hello, how are you?",
            "What do you think about AI?",
            "Can you tell me a joke?"]

# 创建Gradio界面
iface = gr.Interface(fn=call_stream_with_messages,
                      inputs="text",
                      outputs="text",
                      title="Chat with Large Language Model",
                      description="Type a message to start chatting!",
                      examples=examples)

# 启动应用
iface.launch()