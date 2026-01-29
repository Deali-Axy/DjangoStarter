import json
import time
import asyncio
from typing import AsyncGenerator
from django.http import StreamingHttpResponse
from ninja import Router

router = Router(tags=['流式响应示例'])

# Mock LLM Service
class MockLLMService:
    def polish_text(self, text: str) -> str:
        """
        模拟文本润色功能，实际只是简单地添加一些修饰词
        """
        return f"经过智能润色后的内容：{text} (更加专业、流畅、有说服力)"

def get_llm_service():
    return MockLLMService()

llm_service = get_llm_service()


def create_sse_response(generator_func, *args, **kwargs) -> StreamingHttpResponse:
    """创建 SSE 响应的辅助函数"""
    response = StreamingHttpResponse(
        generator_func(*args, **kwargs),
        content_type='text/event-stream'
    )
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'  # 禁用 Nginx 缓冲
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'Cache-Control'
    return response


def simple_counter_stream():
    """简单的计数器流式响应示例"""
    for i in range(1, 11):
        data = {
            'type': 'counter',
            'count': i,
            'message': f'当前计数: {i}',
            'timestamp': time.time()
        }
        yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
        time.sleep(1)  # 模拟延迟
    
    # 发送完成事件
    final_data = {
        'type': 'complete',
        'message': '计数完成！',
        'timestamp': time.time()
    }
    yield f"data: {json.dumps(final_data, ensure_ascii=False)}\n\n"
    
    # 发送流结束标记
    yield "data: [DONE]\n\n"


def llm_text_stream(text: str):
    """模拟 LLM 流式文本生成"""
    # 模拟 LLM 逐字输出
    words = text.split()
    generated_text = ""
    
    for i, word in enumerate(words):
        generated_text += word + " "
        
        data = {
            'type': 'text_chunk',
            'chunk': word + " ",
            'full_text': generated_text.strip(),
            'progress': (i + 1) / len(words),
            'timestamp': time.time()
        }
        yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
        time.sleep(0.2)  # 模拟生成延迟
    
    # 发送完成事件
    final_data = {
        'type': 'complete',
        'full_text': generated_text.strip(),
        'message': '文本生成完成',
        'timestamp': time.time()
    }
    yield f"data: {json.dumps(final_data, ensure_ascii=False)}\n\n"
    
    # 发送流结束标记
    yield "data: [DONE]\n\n"


def chat_simulation_stream(message: str):
    """模拟聊天对话流式响应"""
    # 模拟思考阶段
    thinking_data = {
        'type': 'thinking',
        'message': '正在思考中...',
        'timestamp': time.time()
    }
    yield f"data: {json.dumps(thinking_data, ensure_ascii=False)}\n\n"
    time.sleep(1)
    
    # 模拟回复生成
    responses = [
        "我理解您的问题。",
        "让我为您详细解答。",
        "根据您提供的信息，",
        "我建议您可以考虑以下几个方面：",
        "1. 首先分析问题的核心",
        "2. 然后制定解决方案",
        "3. 最后实施并验证结果",
        "希望这些建议对您有帮助！"
    ]
    
    full_response = ""
    for i, response_part in enumerate(responses):
        full_response += response_part + " "
        
        data = {
            'type': 'response_chunk',
            'chunk': response_part + " ",
            'full_response': full_response.strip(),
            'progress': (i + 1) / len(responses),
            'timestamp': time.time()
        }
        yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
        time.sleep(0.5)
    
    # 发送完成事件
    final_data = {
        'type': 'complete',
        'full_response': full_response.strip(),
        'message': '回复完成',
        'timestamp': time.time()
    }
    yield f"data: {json.dumps(final_data, ensure_ascii=False)}\n\n"
    
    # 发送流结束标记
    yield "data: [DONE]\n\n"


def real_time_data_stream():
    """模拟实时数据推送"""
    import random
    
    for i in range(20):
        # 模拟实时数据（如股价、传感器数据等）
        data = {
            'type': 'real_time_data',
            'id': i + 1,
            'value': round(random.uniform(10, 100), 2),
            'status': random.choice(['正常', '警告', '异常']),
            'timestamp': time.time()
        }
        yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
        time.sleep(0.5)
    
    # 发送结束事件
    end_data = {
        'type': 'stream_end',
        'message': '数据流结束',
        'timestamp': time.time()
    }
    yield f"data: {json.dumps(end_data, ensure_ascii=False)}\n\n"
    
    # 发送流结束标记
    yield "data: [DONE]\n\n"


@router.get('/stream/counter')
def stream_counter(request):
    """简单计数器流式响应"""
    return create_sse_response(simple_counter_stream)


@router.get('/stream/text')
def stream_text(request, text: str = "这是一个流式文本生成的示例，展示了如何逐字输出内容。"):
    """流式文本生成"""
    return create_sse_response(llm_text_stream, text)


@router.get('/stream/chat')
def stream_chat(request, message: str = "请帮我解决一个技术问题"):
    """模拟聊天对话流式响应"""
    return create_sse_response(chat_simulation_stream, message)


@router.get('/stream/realtime')
def stream_realtime(request):
    """实时数据流"""
    return create_sse_response(real_time_data_stream)


@router.get('/stream/llm-polish')
def stream_llm_polish(request, text: str):
    """使用真实 LLM 服务的流式文本润色（模拟）"""
    def llm_polish_stream():
        try:
            # 发送开始事件
            start_data = {
                'type': 'start',
                'message': '开始文本润色...',
                'original_text': text,
                'timestamp': time.time()
            }
            yield f"data: {json.dumps(start_data, ensure_ascii=False)}\n\n"
            
            # 模拟处理过程
            processing_steps = [
                '分析文本结构...',
                '检查语法和用词...',
                '优化表达方式...',
                '生成润色结果...'
            ]
            
            for step in processing_steps:
                step_data = {
                    'type': 'processing',
                    'message': step,
                    'timestamp': time.time()
                }
                yield f"data: {json.dumps(step_data, ensure_ascii=False)}\n\n"
                time.sleep(0.8)
            
            # 调用实际的 LLM 服务
            polished_text = llm_service.polish_text(text)
            
            # 模拟逐步输出润色结果
            words = polished_text.split()
            generated_text = ""
            
            for i, word in enumerate(words):
                generated_text += word + " "
                
                data = {
                    'type': 'result_chunk',
                    'chunk': word + " ",
                    'polished_text': generated_text.strip(),
                    'progress': (i + 1) / len(words),
                    'timestamp': time.time()
                }
                yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
                time.sleep(0.1)
            
            # 发送完成事件
            final_data = {
                'type': 'complete',
                'original_text': text,
                'polished_text': generated_text.strip(),
                'message': '文本润色完成！',
                'timestamp': time.time()
            }
            yield f"data: {json.dumps(final_data, ensure_ascii=False)}\n\n"
            
            # 发送流结束标记
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            error_data = {
                'type': 'error',
                'message': f'处理过程中出现错误: {str(e)}',
                'timestamp': time.time()
            }
            yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"
            
            # 即使出错也要发送流结束标记
            yield "data: [DONE]\n\n"
    
    return create_sse_response(llm_polish_stream)