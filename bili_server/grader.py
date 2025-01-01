#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Chaos
# Date: 2024-12-31

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

class GraderUtils:
    def __init__(self, model):
        self.model = model

    def create_retrieval_grader(self):
        """
        创建一个评估检索文档与用户问题相关性的评分器。

        Returns:
            一个可调用函数，接受一个文档和一个问题作为输入，并返回一个JSON对象，指示文档是否与问题相关。
        """

        # 使用特殊标记来指定不同部分的开始和结束，以及明确不同类型的文本块。
        # 这些标记有助于大模型更好地理解和区分输入数据的不同部分，从而更精确地执行特定任务。
        # 您是一名评分员，负责评估检索到的文档与用户问题的相关性。如果文档包含与用户问题相关的关键词，请将其评为相关。这不需要非常严格的测试。目标是过滤掉错误的检索结果。
        grade_prompt = PromptTemplate(
            template="""
            <|begin_of_text|><|start_header_id|>system<|end_header_id|>
            您是一名评分员，负责评估检索到的文档与用户问题的相关性。如果文档包含与用户问题相关的关键词，请将其评为相关。这不需要非常严格的测试。目标是过滤掉错误的检索结果。
            给出一个二元评分 'yes' 或 'no'，表示文档是否与问题相关。
            提供一个只有一个键 'score' 的JSON，不需要前言或解释。
            <|eot_id|>
            <|start_header_id|>user<|end_header_id|>

            这是检索到的文档: \n\n {document} \n\n
            这是用户问题: {input} \n
            <|eot_id|>
            <|start_header_id|>assistant<|end_header_id|>
            """,
            input_variables=["document", "input"],
        )

        # 创建一个 检索 的链
        retriever_grader = grade_prompt | self.model | JsonOutputParser()

        return retriever_grader

    def create_hallucination_grader(self):
        """
        创建一个评估答案是否基于一组事实的支持的评分器。

        Returns:
            一个可调用函数，接受一个生成（答案）和一组文档（事实）作为输入，并返回一个JSON对象，指示答案是否基于一组事实的支持。
        """
        hallucination_prompt = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
            您是一名评分员，负责评估答案是否基于一组事实的支持。给出一个二元评分 'yes' 或 'no'，表示答案是否基于一组事实的支持。提供一个只有一个键 'score' 的JSON，不需要前言或解释。
            <|eot_id|>
            <|start_header_id|>user<|end_header_id|>
            这些是事实：
            \n ------- \n
            {documents}
            \n ------- \n
            这是答案: {generation}
            <|eot_id|>
            <|start_header_id|>assistant<|end_header_id|>""",
            input_variables=["generation", "documents"],
        )

        hallucination_grader = hallucination_prompt | self.model | JsonOutputParser()

        return hallucination_grader

    def create_code_evaluator(self):
        """
        创建一个评估生成代码是否正确和相关的评分器。

        Returns:
            一个可调用函数，接受一个生成（代码）、一个问题和一组文档作为输入，并返回一个JSON对象，指示代码是否正确和相关。
        """
        eval_template = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> 您是一名评分员，负责评估生成代码是否正确和相关的。
            提供一个JSON响应，包含以下键：

            'score': 一个二元评分 'yes' 或 'no'，表示代码是否正确和相关。
            'feedback': 一个简短的评价解释，包括任何问题或改进建议。

            <|eot_id|><|start_header_id|>user<|end_header_id|>
            这是生成的代码:
            \n ------- \n
            {generation}
            \n ------- \n
            这是问题: {input}
            \n ------- \n
            这是一组相关文档: {documents}
            <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
            input_variables=["generation", "input", "documents"],
        )

        code_evaluator = eval_template | self.model | JsonOutputParser()

        return code_evaluator

    def create_question_rewriter(self):
        """
        创建一个问题重写器链，将输入的问题转换成更好的版本，优化以适应图存储检索。

        Returns:
            一个可调用函数，接受一个问题作为输入，并返回重写后的问题作为字符串。
        """
        re_write_prompt = PromptTemplate(
            template="""
            您是一个问题重写器，将输入的问题转换成更好的版本，优化以适应图存储检索。查看输入并尝试理解其潜在的语义意图/含义。

            这是初始问题: {input}

            形成一个改进的问题.""",

            input_variables=["input"],
        )

        question_rewriter = re_write_prompt | self.model | StrOutputParser()

        return question_rewriter


if __name__ == '__main__':
    from langchain_openai import ChatOpenAI
    from dotenv import load_dotenv, find_dotenv
    import os

    load_dotenv(find_dotenv())

    llm = ChatOpenAI(
        base_url=os.getenv('OPENAI_API_BASE'),
        api_key=os.getenv("OPENAI_API_KEY"),
        model='gpt-4o',
    )

    # 创建一个评分器类的实例
    grader = GraderUtils(llm)

    # # 创建一个检索的评估器
    # retrieval_grader = grader.create_retrieval_grader()
    #
    # # 这是不相关的
    # retrieval_grader_results = retrieval_grader.invoke({
    #     "document": "哈哈哈",
    #     "input": "请问关于ChatGLM3-6B热门视频的描述有哪些？"
    # })
    #
    # # 这是相关的
    # # retrieval_grader_results = retrieval_grader.invoke({
    # #     "document": "这是我查询到的热门视频的描述：ChatGLM3-6B的安装部署、微调、训练智能客服。文档、数据集、微调脚本获取方式：麻烦一键三连，评论后，我会找到评论私发源码，谢谢大家。",
    # #     "input": "请问关于ChatGLM3-6B热门视频的描述有哪些？"
    # # })
    #
    # print(f"retrieval_grader_results: {retrieval_grader_results}")

    # # 创建一个检测大模型幻觉的生成器
    # hallucination_grader = grader.create_hallucination_grader()
    #
    # # 这是出现幻觉的回答
    # # hallucination_grader_results = hallucination_grader.invoke({
    # #     "documents": "这是我查询到的热门视频的描述：ChatGLM3-6B的安装部署、微调、训练智能客服。文档、数据集、微调脚本获取方式：麻烦一键三连，评论后，我会找到评论私发源码，谢谢大家。",
    # #     "generation": "你好"
    # # })
    #
    # # 这是基于检索内容生成的回答
    # hallucination_grader_results = hallucination_grader.invoke({
    #     "documents": "这是我查询到的热门视频的描述：ChatGLM3-6B的安装部署、微调、训练智能客服。文档、数据集、微调脚本获取方式：麻烦一键三连，评论后，我会找到评论私发源码，谢谢大家。",
    #     "generation": "一般对于ChatGLM3-6B模型的热门视频，可以从安装部署、微调、训练等方向来思考"
    # })
    #
    # print(f"hallucination_grader_results:{hallucination_grader_results}")
    #
    # # Get the code evaluator
    # code_evaluator = grader.create_code_evaluator()

    # 对输入的问题进行重写
    question_rewriter = grader.create_question_rewriter()
    question_rewriter_results = question_rewriter.invoke({
        "input": "对于ChatGLM3-6B模型，应该如何写热门标题的描述,请你用中文回复"
    })
    print(f"question_rewriter_results: {question_rewriter_results}")
