#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Chaos
# Date: 2025-01-12

from bili_server.generate_chain import create_generate_chain
# from bili_server.qa_tools.function_tools import common_question_tool
from bili_server.qa_tools.prompt_template import GENERATE_KEYWORDS_TEMPLATE
from bili_server.qa_tools.question_type_classify import classify_question_type
from bili_server.rag_tools.document_loader import DocumentLoader
from bili_server.qa_tools.chat_with_ai import chat_with_ai
import re

class GraphNodes:
    def __init__(self, llm, retriever, retrieval_grader, hallucination_grader, code_evaluator, question_rewriter):
        self.llm = llm
        self.retriever = retriever
        self.retrieval_grader = retrieval_grader
        self.hallucination_grader = hallucination_grader
        self.code_evaluator = code_evaluator
        self.question_rewriter = question_rewriter
        self.generate_chain = create_generate_chain(llm)

    
    def transform_query(self, state)->dict:
        """
        重写提问
        Transform the query to produce a better question.

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Updates question key with a re-phrased question
        """
        print("---节点：重写用户输入的问题---")

        question = state["input"]
        if "documents" in state:
            documents = state["documents"]
        else:
            documents = "无参考信息"

        # 问题重写
        better_question = self.question_rewriter.invoke({"input": question, 
                                                         "documents": documents})
        print(f"这是重写的问题:{better_question}")
        return {"documents": documents, "input": better_question}

    def parse_question(self,state) -> dict:
        """
        解析输入的问题

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, input_keywords, that contains input keywords
        """
        question = state["input"]
        # # 解析问题类型
        # question_type = classify_question_type(question)
        # state["question_type"] = question_type
        # 生成关键字
        response = chat_with_ai(f"{GENERATE_KEYWORDS_TEMPLATE}\n{question}")
        input_keywords = re.split(r'[,\uFF0C]', response)
        return {"input_keywords": input_keywords, "input": question,
                "documents": state["documents"],
                 "keywords_in_rag": [], "keywords_not_in_rag": []}
    
    def retrieve_keywords_in_RAG(self, state)->dict:
        """
        根据关键词检索RAG，将检索到的关键词添加到图状态中

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state
        """
        keywords = state["input_keywords"]
        keywords_in_rag = []
        keywords_not_in_rag = []
        for keyword in keywords:
            # TODO: has_keyword需要检查文本是否足够重要
            if DocumentLoader.get_instance().has_keyword(keyword):
                keywords_in_rag.append(keyword)
            else:
                keywords_not_in_rag.append(keyword)

        return {"input_keywords": keywords, "input": state["input"],
                "documents": state["documents"],
                 "keywords_in_rag": keywords_in_rag, "keywords_not_in_rag": keywords_not_in_rag}

    async def retrieve_and_store_keywords_via_Bili(self, state)->dict:
        """
        根据关键词检索Bilibili

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state
        """
        keywords = state["input_keywords"]
        missing_keywords = [keyword for keyword in keywords if not state["keywords_in_rag"]]
        

        from get_bilibili_data import get_data
        documents=get_data.get(missing_keywords,page_num=1)
        try:
            print(f"检索到的文档为[前200字符]: {documents[:100]}")
        except:
            print()

        DocumentLoader.get_instance().create_graph_store(documents)
        
        return state


    def grade_documents(self, state)->dict:
        """
        判断检索到的文档是否与问题相关

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Updates documents key with only filtered relevant documents
        """
        print("---节点：检查检索到的文档是否与问题相关---")
        question = state["input"]
        old_documents = state["documents"]

        print(question)
        print(type(question))
        documents=DocumentLoader.get_instance().get_retriever(keywords=question, mode="local")
        
        print(f"这是检索到的Docs:{documents}")

        if documents and old_documents:
            # 比较两份文档哪个更好,赋值给document
            pass
        
        filtered_docs = []


        score = self.retrieval_grader.invoke({"input": question, "document": documents})
        #TODO 正式版删除
        print(documents)
        grade = score["score"]
        if grade == "yes":
            print("---评估结果: 检索文档与问题相关---")
        else:
            print("---评估结果: 检索文档与问题不相关---")

        return {"documents": filtered_docs, "input": question}

    def generate_answer(self, state)->dict:
        """
        使用输入问题和检索到的数据生成答案，并将生成添加到状态中

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, generation, that contains LLM generation
        """
        print("---节点：生成回答---")

        question = state["input"]
        documents = state["documents"]

        generation = self.generate_chain.invoke({"context": documents, "input": question})
        print(f"生成的回答为:{generation}")
        return {"documents": documents, "input": question, "generation": generation}
    
    # def parse_answer(self,state)->dict:
    #     """
    #     对答案结构化输出
    #     Args:
    #         state (dict): The current graph state

    #     Returns:
    #         state (dict): New key added to state, answer, that contains the answer
    #     """
    #     print("---节点：结构化输出---")
    #     generation=state["generation"]
    #     chat_with_ai(f"""
    #         你是一个内容总结专家，我会给你提供一份文字，你需要结构化输出一份回答，
    #         针对提问的问题和参考资料，总结出回答，
    #         每一条观点需要附上推荐的视频链接，格式如下：
    #         1.xxx，推荐视频：[视频名字](视频链接)
    #         2.xxx，推荐视频：[视频名字](视频链接)
    #         问题：{state["input"]},
    #         参考文档：{state["documents"]}
    #     """)

    #     return{"input": state["input"], "generation":None}
