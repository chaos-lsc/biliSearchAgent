#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Chaos
# Date: 2024-12-31

from typing import Callable, List
from bili_server.qa_tools.question_type import QuestionType

def wide_topic_tool(args: List) -> List:
    return args

def recommendation_tool(args: List) -> List:
    return args

def explanation_tool(args: List) -> List:
    return args

def strategy_tool(args: List) -> List:
    return args

def comparison_tool(args: List) -> List:
    return args

def process_unknown_question_tool(args: List) -> List:
    return args

TOOLS_MAPPING = {
    QuestionType.WIDE_TOPIC: wide_topic_tool,
    QuestionType.RECOMMENDATION: recommendation_tool,
    QuestionType.EXPLANATION: explanation_tool,
    QuestionType.STRATEGY: strategy_tool,
    QuestionType.COMPARISON: comparison_tool,
    QuestionType.UNKNOWN: process_unknown_question_tool
}


def map_question_to_function(
        question_type: QuestionType,
) -> Callable:
    if question_type in TOOLS_MAPPING:
        return TOOLS_MAPPING[question_type]
    else:
        raise ValueError(f"No tool found for question type: {question_type}")

FUNCTION_ARGS_MAPPING = {
    QuestionType.WIDE_TOPIC: lambda args: args[-1:],
    QuestionType.RECOMMENDATION: lambda args: args[-1:],
    QuestionType.EXPLANATION: lambda args: args[-1:],
    QuestionType.STRATEGY: lambda args: args[-1:],
    QuestionType.COMPARISON: lambda args: args[-1:],
    QuestionType.UNKNOWN: lambda args: args[1:3]
}


def map_question_to_function_args(
        question_type: QuestionType,
) -> Callable[[List], List]:
    if question_type in FUNCTION_ARGS_MAPPING:
        return FUNCTION_ARGS_MAPPING[question_type]
    else:
        raise ValueError(f"No tool found for question type: {question_type}")
    