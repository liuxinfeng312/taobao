from http import HTTPStatus
import dashscope
dashscope.api_key ='sk-eab2838a42bc4090a6fdee30392d19bb'
import random
from http import HTTPStatus
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role


def multi_round_conversation():
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': '请介绍一下上海有什么好玩的地方'}]
    response = Generation.call(
        'qwen-1.8b-chat',
        messages=messages,
        # set the random seed, optional, default to 1234 if not set
        seed=random.randint(1, 10000),
        result_format='message',  # set the result to be "message"  format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
        messages.append({'role': response.output.choices[0]['message']['role'],
                         'content': response.output.choices[0]['message']['content']})
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
    messages.append({'role': Role.USER, 'content': '能否缩短一些，只讲三点'})
    print(messages)
    response = Generation.call(
        'qwen-1.8b-chat',
        messages=messages,
        result_format='message',  # set the result to be "message"  format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))

def multi_round_conversation_api(messages= [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': '请介绍一下上海有什么好玩的地方'}]):
    # messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
    #             {'role': 'user', 'content': '请介绍一下上海有什么好玩的地方'}]
    response = Generation.call(
        'qwen-1.8b-chat',
        messages=messages,
        # set the random seed, optional, default to 1234 if not set
        seed=random.randint(1, 10000),
        result_format='message',  # set the result to be "message"  format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
        messages.append({'role': response.output.choices[0]['message']['role'],
                         'content': response.output.choices[0]['message']['content']})
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
    result = response
    return result

def call_stream_with_messages():
    messages = [
        {'role': 'user', 'content': '用萝卜、土豆、茄子做饭，给我个菜谱'}]
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
            print(response)
            print(response.output.choices[0]['message']['content'])
            yield response.output.choices[0]['message']['content']
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
    #print('Full content: \n' + full_content)

if __name__ == '__main__':
    #multi_round_conversation()
    call_stream_with_messages()