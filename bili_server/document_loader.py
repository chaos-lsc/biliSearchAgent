#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Chaos
# Date: 2024-12-27

import os
# from langchain_core.documents import Document
import get_bilibi
from typing import List, Optional
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from lightrag import LightRAG, QueryParam
from lightrag.llm import openai_complete_if_cache, openai_embedding
from lightrag.utils import EmbeddingFunc
import numpy as np
import asyncio

import nest_asyncio
nest_asyncio.apply()

WORKING_DIR = "./dickens"


if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

# LLM model function


async def llm_model_func(
    prompt, system_prompt=None, history_messages=[], keyword_extraction=False, **kwargs
) -> str:
    return await openai_complete_if_cache(
        "glm4-flash",
        prompt,
        system_prompt=system_prompt,
        history_messages=history_messages,
        api_key=os.getenv("GLM_API_KEY"),
        base_url="https://api.upstage.ai/v1/solar",
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

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=llm_model_func,
    embedding_func=EmbeddingFunc(
        embedding_dim=1024,  # BAAI/bge-m3 支持 1024 dim
        max_token_size=8192,
        func=embedding_func
    )
)


class DocumentLoader:
    """
    This class uses the get_docs function to take a Keyword as input, and outputs a list of documents (including metadata).
    """

    async def get_docs(self, keywords: List[str], page: int) -> List[str]:
        """
        根据BiliBili API中的特定关键字异步检索文档

        Args:
        keywords (List[str]): 用于查询BiliBili API的关键字列表
        page (int): API请求中的页码，用于分页

        Returns:
            List[str]: 包含检索到的内容的列表

        """

        raw_docs = await get_bilibi.bilibili_detail_pipiline(keywords=keywords, page=page)

        docs = [doc["real_data"] for doc in raw_docs]

        return docs

    async def create_graph_store(self, docs):
        """
        从文档列表创建图存储

        Args:
            docs (List[str]): 包含要存储的内容的列表

        """
        print(type(docs))
        rag.insert(docs)

        # Perform naive search
        print(rag.query("What are the top themes in this story?",
                        param=QueryParam(mode="naive")))

        # Perform local search
        print(rag.query("What are the top themes in this story?",
                        param=QueryParam(mode="local")))

        # Perform global search
        print(rag.query("What are the top themes in this story?",
                        param=QueryParam(mode="global")))

        # Perform hybrid search
        print(rag.query("What are the top themes in this story?",
                        param=QueryParam(mode="hybrid")))

        # Perform mix search (Knowledge Graph + Vector Retrieval)
        # Mix mode combines knowledge graph and vector search:
        # - Uses both structured (KG) and unstructured (vector) information
        # - Provides comprehensive answers by analyzing relationships and context
        # - Supports image content through HTML img tags
        # - Allows control over retrieval depth via top_k parameter
        print(rag.query("What are the top themes in this story?", param=QueryParam(
            mode="mix")))

    async def get_retriever(self, keywords: List[str], page: int):
        """
            Retrieves documents and returns a retriever based on the documents.

            Args:
                keywords (List[str]): Keywords to search documents.
                page (int): Page number for pagination of results.

            Returns:

            """
        print(f"开始实时查询BiliBiliAPI获取数据")
        docs = await self.get_docs(keywords, page)
        # print(f"接收到的BiliBili数据为：{docs}")
        print("-------------------------")
        print(f"开始进行图数据库存储")
        await self.create_graph_store(docs)
        print(f"成功完成图数据库的存储")
        print("-------------------------")
        print(f"开始进行文本检索")
        retriever_result = rag.query(keywords, param=QueryParam(mode="mix"))
        print(f"检索到的数据为：{retriever_result}")
        return retriever_result


if __name__ == '__main__':
    async def main():
        loop = asyncio.get_running_loop()
        if loop.is_running():
            print("Event loop is already running")
        else:
            print("Event loop is not running")
        loader = DocumentLoader()
        await loader.get_retriever(keywords=["ChatGLM3-6b"], page=3)

    asyncio.run(main())
