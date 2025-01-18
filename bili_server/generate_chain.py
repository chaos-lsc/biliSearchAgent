#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Chaos
# Date: 2025-01-17

import os
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def create_generate_chain(llm):
    """
    Creates a generate chain for answering bilibili-related questions.

    Args:
        llm (LLM): The language model to use for generating responses.

    Returns:
        A callable function that takes a context and a question as input and returns a string response.
    """
    generate_template = """
    你是一个内容总结专家，我会给你提供一份文字，参考资料会被<context></context>标签包裹，问题会被<question></question>标签包裹，
    你需要结构化输出一份回答，针对问题和参考资料总结出回答，每一条观点需要附上推荐的视频链接，格式如下：

    1. xxx，推荐视频：[视频名字](视频链接)  
    2. xxx，推荐视频：[视频名字](视频链接)  

    如果你找不到答案，请诚实地回答你不知道。不要试图捏造答案。
    如果问题与上下文无关，礼貌地回答你只能回答与提供的上下文相关的问题。

    对于涉及数据分析的问题，请用Python编写代码并提供对结果的详细分析，以提供尽可能全面的答案。

        
    <context>
    {context}
    </context>
    
    <question>
    {input}
    </question>
    """

    generate_prompt = PromptTemplate(
        template=generate_template, input_variables=["context", "input"])

    # 没有StrOutputParser() 输出可能如下所示：
    # {
    #     "content": "This is the response from the LLM.",
    #     "metadata": {
    #         "confidence": 0.8,
    #         "response_time": 0.5
    #     }
    # }

    # 使用StrOutputParser() ，它看起来像这样：
    # This is the response from the LLM.

    # Create the generate chain
    generate_chain = generate_prompt | llm | StrOutputParser()

    return generate_chain


if __name__ == '__main__':
    # https://python.langchain.com/docs/integrations/chat/openai/
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        base_url=os.getenv('OPENAI_API_BASE'),
        api_key=os.getenv("OPENAI_API_KEY"),
        model='gpt-4o',
    )

    # 创建一个生成链
    generate_chain = create_generate_chain(llm)
    final_answer = generate_chain.invoke({
        "context": "这是我查询到的热门视频的描述：ChatGLM3-6B的安装部署、微调、训练智能客服。文档、数据集、微调脚本获取方式：麻烦一键三连，评论后，我会找到评论私发源码，谢谢大家。",
        "input": "请帮我梳理一下热门视频的描述信息"
    })
    print(final_answer)
