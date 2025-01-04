#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Chaos
# Date: 2025-01-01

from typing import Callable
from bili_server.qa_tools.question_type import QuestionType
from bili_server.qa_tools.prompt_template import UNKNOWN_QUESTION_TEMPLATE
from bili_server.qa_tools.prompt_template import GENERATE_KEYWORDS_TEMPLATE
from bili_server.qa_tools.chat_with_ai import chat_with_ai
from bili_server.rag_tools.document_loader import DocumentLoader
from bili_server.utils.grader import GraderUtils

from get_bilibili_data.get_pages import get_pages
import asyncio
import pprint

def common_question_tool(question: str) -> str:
    # answer = asyncio.run(DocumentLoader().get_instance().get_retriever(question,'local'))
    # relative_grader = GraderUtils.get_instance().create_retrieval_grader()
    # score = relative_grader.invoke({"document": answer, "input": question})
    # print(score)
    # if score['score'] == 'yes':
    #     return answer
    
    # 生成关键字
    response = chat_with_ai(f"{GENERATE_KEYWORDS_TEMPLATE}\n{question}")
    keywords = response.split(',')
    print(keywords)
    results = []
    for keyword in keywords:
        # 搜索关键字
        result = get_pages(keyword,1)
        print(result)
        results.append(result)
    print(result)
    pprint(results)


def unknown_question_tool(question: str) -> str:
    return chat_with_ai(f"{UNKNOWN_QUESTION_TEMPLATE}\n{question}")

TOOLS_MAPPING = {
    QuestionType.WIDE_TOPIC: common_question_tool,
    QuestionType.RECOMMENDATION: common_question_tool,
    QuestionType.EXPLANATION: common_question_tool,
    QuestionType.STRATEGY: common_question_tool,
    QuestionType.COMPARISON: common_question_tool,
    QuestionType.UNKNOWN: unknown_question_tool
}


def map_question_to_function(
        question_type: QuestionType,
) -> Callable:
    if question_type in TOOLS_MAPPING:
        return TOOLS_MAPPING[question_type]
    else:
        raise ValueError(f"No tool found for question type: {question_type}")

# 函数参数映射
# 需要根据问题类型和参数数量来确定
# FUNCTION_ARGS_MAPPING = {
#     QuestionType.WIDE_TOPIC: lambda args: args[-1:],
#     QuestionType.RECOMMENDATION: lambda args: args[-1:],
#     QuestionType.EXPLANATION: lambda args: args[-1:],
#     QuestionType.STRATEGY: lambda args: args[-1:],
#     QuestionType.COMPARISON: lambda args: args[-1:],
#     QuestionType.UNKNOWN: lambda args: args[1:3]
# }


# def map_question_to_function_args(
#         question_type: QuestionType,
# ) -> Callable[[List], List]:
#     if question_type in FUNCTION_ARGS_MAPPING:
#         return FUNCTION_ARGS_MAPPING[question_type]
#     else:
#         raise ValueError(f"No tool found for question type: {question_type}")
    