import random

import gradio as gr

from http import HTTPStatus
import dashscope
dashscope.api_key ='sk-2984cfaeb7544341aeed6ca40f6323df'
from dashscope import Generation
import requests
import json
import time
def gpt_api(query,history):
    print(query, history)
    time.sleep(1)
    messages = []

    if history != []:
        for li in history:
            messages.append({'role': 'user', 'content': li[0]})
            messages.append({'role': 'assistant', 'content': li[1]})
    messages.append({'role': 'user', 'content': query})

    url = "https://api.openai-hk.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "hk-sy1mc810000258919109a80e2e60502fa0d8db20b075cbba"
    }

    data = {
        "max_tokens": 1200,
        "model": "gpt-4-gizmo-(gizmo_id)",
        "temperature": 0.8,
        "top_p": 1,
        "presence_penalty": 1,
        "messages": messages
    }

    response = requests.post(url, headers=headers, data=json.dumps(data).encode('utf-8'))
    result = json.loads(response.content.decode("utf-8"))


    print(result)
    print(type(result))
    return result['choices'][0]['message']['content']



def qwen_api(query,history):
    print(query,history)
    messages = []

    if history!=[]:
        for li in history:
            messages.append({'role': 'user', 'content': li[0]})
            messages.append({'role': 'assistant', 'content': li[1]})
    messages.append({'role': 'user', 'content': query})
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


def chatglm_api(query,history):
    print(query,history)
    messages = []

    if history!=[]:
        for li in history:
            messages.append({'role': 'user', 'content': li[0]})
            messages.append({'role': 'assistant', 'content': li[1]})
    messages.append({'role': 'user', 'content': query})
    responses = Generation.call(
        'chatglm3-6b',
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

qwen_history=[]
gpt_history=[]
glm_history=[]
history_dict={
    'qwen':[],
    'gpt':[],
    'glm':[]
}
his_label=False
def chat(query,history):
    print(query)
    print(history)
    if 'Qwen Assistant:' in query:
        print(history_dict)

        print('='*20)
        print('qwen-api:')
        print(query, history)
        messages = []
        query='Qwen Assistant:'+query

        if history != []:
            for li in history :
                if 'Qwen Assistant:' not in li[0]:
                    continue
                messages.append({'role': 'user', 'content': li[0]})
                messages.append({'role': 'assistant', 'content': li[1]})
        messages.append({'role': 'user', 'content': query})

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

    elif 'ChatGlm Assistant:' in query:
        print('chatgllm'*20)
        print('+'*20)
        print(query, history)
        query = 'Chatglm Assistant:' + query
        messages = []

        if history != []:
            for li in history:
                if 'ChatGlm Assistant:' not in li[0]:
                    continue
                messages.append({'role': 'user', 'content': li[0]})
                messages.append({'role': 'assistant', 'content': li[1]})
        messages.append({'role': 'user', 'content': query})
        responses = Generation.call(
            'chatglm3-6b',
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
    elif 'GPT Assistant:' in query:
        print(query, history)
        time.sleep(1)
        messages = []
        query = 'GPT Assistant:' + query
        if history != []:
            for li in history:
                if 'GPT Assistant:' not in li[0]:
                    continue
                messages.append({'role': 'user', 'content': li[0]})
                messages.append({'role': 'assistant', 'content': li[1]})
        messages.append({'role': 'user', 'content': query})

        url = "https://api.openai-hk.com/v1/chat/completions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "hk-sy1mc810000258919109a80e2e60502fa0d8db20b075cbba"
        }

        data = {
            "max_tokens": 1200,
            "model": "gpt-4-all",
            "temperature": 0.8,
            "top_p": 1,
            "presence_penalty": 1,
            "messages": messages
        }

        response = requests.post(url, headers=headers, data=json.dumps(data).encode('utf-8'))
        result = json.loads(response.content.decode("utf-8"))
        print(result)
        yield result['choices'][0]['message']['content']

    else:
        messages = []
        query = 'Qwen Assistant:' + query

        if history != []:
            for li in history:
                if 'Qwen Assistant:' not in li[0]:
                    continue
                messages.append({'role': 'user', 'content': li[0]})
                messages.append({'role': 'assistant', 'content': li[1]})
        messages.append({'role': 'user', 'content': query})

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
# 定义输入和输出说明
examples = ["Qwen Assistant:",
            "ChatGlm Assistant:",
            "GPT Assistant:"]


# 创建Gradio界面
iface = gr.ChatInterface(fn=chat,

                      title="Chat with Large Language Model",
                      description="Type a message to start chatting!",
                      examples=examples)
# def options():
#     pass
# with iface:
#
#     b1 = gr.Button("qwen")
#     b2 = gr.Button("gpt")
#     b3 = gr.Button("chatglm")
#
#     b1.click(api_name=qwen_api)
#     b2.click(api_name=options)
#     b3.click(api_name=gpt_api)
# 启动应用
iface.launch(share=True)