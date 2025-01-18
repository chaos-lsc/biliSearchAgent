#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Chaos
# Date: 2024-12-27

import os
# from langchain_core.documents import Document
from get_bilibili_data import get_data
from typing import List, Any
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from lightrag import LightRAG, QueryParam
from typing import Literal
from lightrag.llm import openai_complete_if_cache, openai_embedding
from lightrag.utils import EmbeddingFunc
import numpy as np
import asyncio

import nest_asyncio
nest_asyncio.apply()

from dotenv import load_dotenv, find_dotenv
import networkx as nx

WORKING_DIR = "./dickens"

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

# LLM model function


async def llm_model_func(
    prompt, system_prompt=None, history_messages=[], keyword_extraction=False, **kwargs
) -> str:
    return await openai_complete_if_cache(
        "glm-4-flash",
        prompt,
        system_prompt=system_prompt,
        history_messages=history_messages,
        api_key=os.getenv("GLM_API_KEY"),
        base_url=os.getenv("GLM_API_BASE"),
        **kwargs
    )

# Embedding function


async def embedding_func(texts: list[str]) -> np.ndarray:
    return await openai_embedding(
        texts,
        model="BAAI/bge-m3",
        api_key=os.getenv("SF_API_KEY"),
        base_url=os.getenv("SF_API_BASE")
    )


class DocumentLoader:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.rag = LightRAG(
            working_dir=WORKING_DIR,
            llm_model_func=llm_model_func,
            embedding_func=EmbeddingFunc(
                embedding_dim=1024,  # BAAI/bge-m3 支持 1024 dim
                max_token_size=8192,
                func=embedding_func
            ),
            addon_params={
                "entity_types": ["organization", "person", "geo", "event", "category", "videoID",],
                "language": "中文",
            }
        )

    def has_keyword(self, keyword: str) -> bool:
        """
        检查RAG中是否存在特定关键词
        """
        # Get all nodes that have edges
        nodes_with_edges = set()
        graph_file_path = WORKING_DIR + "/graph_chunk_entity_relation.graphml"
        if os.path.exists(graph_file_path):
            G = nx.read_graphml(graph_file_path)
            if G.number_of_nodes() > 0:
                for u, v in G.edges():
                    nodes_with_edges.add(u)
                    nodes_with_edges.add(v)
        else:
            print(f"文件 {graph_file_path} 不存在。")

        # if nodes_with_edges:
        #     # Print all nodes that have edges
        #     for node in nodes_with_edges:
        #         print(f"Node: {node}")
        #         print(f"Node Properties: {G.nodes[node]}")
        #         print("---")
        
        if keyword in nodes_with_edges:
            print(f"关键词 '{keyword}' 存在于节点中。")
            return True
        else:
            print(f"关键词 '{keyword}' 不存在于节点中。")
            return False

    async def get_docs(self, keywords: List[str], page: int) -> List[str]:
        """
        根据BiliBili API中的特定关键字异步检索文档

        Args:
        keywords (List[str]): 用于查询BiliBili API的关键字列表
        page (int): API请求中的页码，用于分页

        Returns:
            List[str]: 包含检索到的内容的列表

        """

        raw_docs = await get_data(keywords=keywords, page=page)

        docs = [doc["real_data"] for doc in raw_docs]

        return docs

    async def create_graph_store(self, docs):
        """
        从文档列表创建图存储

        Args:
            docs (List[str]): 包含要存储的内容的列表

        """
        self.rag.insert(docs)

    async def get_retriever(self, keywords: List[str], mode: Literal['local', 'global', 'hybrid', 'naive', 'mix'] = "mix") -> Any:
        """
        Retrieves documents and returns a retriever based on the documents.

        Args:
            keywords (List[str]): Keywords to search documents.
            mode (Literal['local', 'global', 'hybrid', 'naive', 'mix']): The mode for the retriever. Defaults to "mix".

        Returns:
            Any: The retrieved result.
        """
        print("开始进行文本检索")
        retriever_result = self.rag.query(query=keywords, param=QueryParam(mode=mode))
        # TODO：对比测试一下那种方式检索出来的内容更好
        # rag.query_with_separate_keyword_extraction(
        # "What are the top themes in this story?",
        # "You need to answer me this question in as simple language as you can. Just know that a 5 year old should understand it.",
        # param=QueryParam(mode="hybrid")
        # )
        print(f"检索到的数据为：{retriever_result}")
        return retriever_result


if __name__ == '__main__':
    async def main():
        # 从 .env 文件加载环境变量
        load_dotenv(find_dotenv())

        loader = DocumentLoader()
        await loader.get_retriever(keywords=["如何学习使用ChatGLM3-6b"])

    asyncio.run(main())
