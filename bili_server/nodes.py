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

class GraphNodes:
    def __init__(self, llm, retriever, retrieval_grader, hallucination_grader, code_evaluator, question_rewriter):
        self.llm = llm
        self.retriever = retriever
        self.retrieval_grader = retrieval_grader
        self.hallucination_grader = hallucination_grader
        self.code_evaluator = code_evaluator
        self.question_rewriter = question_rewriter
        self.generate_chain = create_generate_chain(llm)

    async def retrieve(self, state):
        """
        根据输入问题检索文档，并将它们添加到图状态中。
        Retrieve documents

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, documents, that contains retrieved documents
        """
        print("---节点：开始检索---")
        question = state["input"]

        # 执行检索
        documents = await self.retriever.get_retriever(keywords=[question], page=1)
        print(f"这是检索到的Docs:{documents}")
        return {"documents": documents, "input": question}
    
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
        input_keywords = response.split(',')

        return {"input_keywords": input_keywords, "input": question,
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
        # TODO: 根据关键词检索RAG
        keywords_in_rag = []
        keywords_not_in_rag = []
        for keyword in keywords:
            if DocumentLoader.get_instance().has_keyword(keyword):
                keywords_in_rag.append(keyword)
            else:
                keywords_not_in_rag.append(keyword)

        return {"input_keywords": keywords, "input": state["input"],
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
        
        for keyword in missing_keywords:
            pass
            #TODO: 执行检索
            #documents =
            #get_docs(missing_keywords, page=1)
            #print(f"检索到的文档为: {documents}")
            #TODO: 向rag中添加
            #await self.rag.create_graph_store(documents)
        
        return state

    def generate_answer(self, state)->dict:
        """
        使用输入问题和检索到的数据生成答案，并将生成添加到状态中

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, generation, that contains LLM generation
        """
        print("---节点：生成响应---")

        question = state["input"]
        documents=DocumentLoader.getinstance().get_retriever(keywords=state["input_keywords"], mode="mix")
        state["documents"]=documents

        generation = self.generate_chain.invoke({"context": documents, "input": question})
        print(f"生成的响应为:{generation}")
        return {"documents": documents, "input": question, "generation": generation}

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
        documents = state["documents"]


        filtered_docs = []

        for d in documents:
            score = self.retrieval_grader.invoke({"input": question, "document": d.page_content})
            grade = score["score"]
            if grade == "yes":
                print("---评估结果: 检索文档与问题相关---")
                filtered_docs.append(d)
            else:
                print("---评估结果: 检索文档与问题不相关---")
                continue

        return {"documents": filtered_docs, "input": question}

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
        # TODO 这里需要检索的文档信息？
        documents = state["documents"]

        # 问题重写
        better_question = self.question_rewriter.invoke({"input": question})
        print(f"这是重写的问题:{better_question}")
        return {"documents": documents, "input": better_question}
