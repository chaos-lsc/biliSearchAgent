#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Chaos
# Date: 2024-12-31

from enum import Enum

class QuestionType(Enum):
    """
    问题类型
    """
    UNKNOWN = 0  # 未知问题类型
    WIDE_TOPIC = 1  # 广泛主题问题
    RECOMMENDATION = 2  # 推荐问题
    EXPLANATION = 3  # 解释问题
    STRATEGY = 4  # 策略问题
    COMPARISON = 5  # 比较问题

QUESTION_MAP = {
    "未知问题": QuestionType.UNKNOWN,
    "广泛主题问题": QuestionType.WIDE_TOPIC,
    "推荐问题": QuestionType.RECOMMENDATION,
    "解释问题": QuestionType.EXPLANATION,
    "策略问题": QuestionType.STRATEGY,
    "比较问题": QuestionType.COMPARISON,
    }
