#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Chaos
# Date： 2024-12-31


from langchain_openai import ChatOpenAI
from bili_server.rag_tools.document_loader import DocumentLoader
from bili_server.edges import EdgeGraph
from bili_server.generate_chain import create_generate_chain
from bili_server.graph import GraphState
from bili_server.utils.grader import GraderUtils
from bili_server.nodes import GraphNodes

from bili_server.qa_tools.prompt_template import GENERATE_KEYWORDS_TEMPLATE

from langgraph.graph import END, StateGraph

import os


def initialize_parser_components():
    """
    初始化解析器组件和评分器实例。

    Returns:
    dict: 包含所有创建的组件实例的字典。
    """

    # 创建 retriever 实例，用于文档检索
    retriever = DocumentLoader()

    # 创建 LLM model 实例，配置为使用 glm-4-flash 模型
    llm = ChatOpenAI(
        base_url=os.getenv('GLM_API_BASE'),
        api_key=os.getenv("GLM_API_KEY"),
        model='glm-4-flash',
        temperature=0
    )

    # 创建生成链，用于基于语言模型的生成任务
    generate_chain = create_generate_chain(llm)

    # 初始化评分器实例，用于创建和管理多种评分工具
    grader = GraderUtils()

    # 创建评估检索文档与用户问题相关性的评分器
    retrieval_grader = grader.create_retrieval_grader()

    # 创建评估模型的回答是否出现幻觉的评分器
    hallucination_grader = grader.create_hallucination_grader()

    # 创建代码评估器，用于评估代码执行结果的正确性
    code_evaluator = grader.create_code_evaluator()

    # 创建问题重写器，用于优化用户问题，使其更适合模型理解和回答
    question_rewriter = grader.create_question_rewriter()

    # 返回包含所有组件的字典，以便在其他部分的代码中使用
    return {
        "llm": llm,
        "retriever": retriever,
        "generate_chain": generate_chain,
        "retrieval_grader": retrieval_grader,
        "hallucination_grader": hallucination_grader,
        "code_evaluator": code_evaluator,
        "question_rewriter": question_rewriter
    }


def create_workflow():
    """
    本函数创建工作流

    Returns:
    StateGraph: 完全初始化和编译好的工作流对象。
    """

    # 调用函数并直接解构字典以获取所有实例
    (llm, retriever, generate_chain,
     retrieval_grader, hallucination_grader,
     code_evaluator, question_rewriter) = initialize_parser_components().values()


    # 初始化图结构
    workflow = StateGraph(GraphState)

    # 创建图节点的实例
    graph_nodes = GraphNodes(llm, retriever, retrieval_grader,
                             hallucination_grader, code_evaluator, question_rewriter)

    # 创建边节点的实例
    edge_graph = EdgeGraph(hallucination_grader, code_evaluator)

    # 定义节点

    # init state
    workflow.add_node("init_state", graph_nodes.parse_question)
    # RAG 中检索关键词实体是否存在
    workflow.add_node("retrieve_keywords_in_RAG", graph_nodes.retrieve_keywords_in_RAG)
    # 向RAG中添加缺少的语料，无需检索文本
    workflow.add_node("retrieve_and_store_keywords_via_bili",graph_nodes.retrieve_and_store_keywords_via_Bili)
    
    # 检索 RAG，输出回答
    workflow.add_node("generate_answer", graph_nodes.generate_answer)

    # grade documents
    workflow.add_node("grade_documents", graph_nodes.grade_documents)
    # transform query
    workflow.add_node("transform_query", graph_nodes.transform_query)

    # TODO 需要修改，添加功能后删除注释
    # workflow.add_node("split_text_by_semantics", graph_nodes.split_text_by_semantics)

    # 创建图
    workflow.set_entry_point("init_state")
    workflow.add_edge("init_state", "retrieve_keywords_in_RAG")
    workflow.add_conditional_edges(
        "retrieve_keywords_in_RAG",
        edge_graph.decide_to_retrieve_keywords,
        {
            "retrieve_and_store_keywords_via_bili": "retrieve_and_store_keywords_via_bili",
            "generate_answer": "generate_answer",
        }
    )
    workflow.add_edge("generate_answer", "grade_documents")
    # workflow.add_edge("retrieve_and_store_keywords_via_bili", "retrieve")
    # workflow.add_conditional_edges(
    #     "generate_answer",
    #     edge_graph.grade_generation_v_documents_and_question,
    #     {
    #         "not supported": "generate_answer",
    #         "useful": END,
    #         "not useful": "transform_query",
    #     }
    # )

    # 编译图
    chain = workflow.compile()
    return chain


if __name__ == '__main__':
    # from langgraph.visualization import display_graph

    try:
        chain = create_workflow()
        print(chain.get_graph().draw_mermaid_png())
        # display_graph(chain)
    except Exception:
        pass
