from http import HTTPStatus
from dashscope import Generation
import dashscope
dashscope.api_key ='sk-eab2838a42bc4090a6fdee30392d19bb'

def call_with_messages():
    messages = [
        {'role': 'system', 'content':'You are a helpful assistant.'},
        {'role': 'user', 'content': '介绍下杭州'}]
    gen = Generation()
    response = gen.call(
        'chatglm3-6b',
        messages=messages,
        result_format='message',  # set the result is message format.
    )
    print(response)

if __name__ == '__main__':
    call_with_messages()