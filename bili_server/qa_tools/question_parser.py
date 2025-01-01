#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Chaos
# Date: 2024-12-31

import os
from bili_server.qa_tools.question_type import QuestionType, QUESTION_MAP
from bili_server.qa_tools.prompt_template import get_question_parser_prompt
from openai import OpenAI

def parse_question(question: str) -> QuestionType:
    """
    解析问题的意图
    Args:
        question(str): 输入的问题
    Returns:
        QuestionType: 问题的意图类型
    """
    client = OpenAI(api_key=os.getenv("GLM_API_KEY"),
                  base_url=os.getenv("GLM_API_BASE"),
                  )
    
    prompt = get_question_parser_prompt(question)
    parse_result = client.chat.completions.create(
            model="glm-4-flash",
            messages=[
                {"role": "user", "content": prompt},
            ],
            top_p=0.7,
            temperature=0.95,
            max_tokens=1024,
        )
    question_type = QUESTION_MAP[parse_result]

    return question_type
