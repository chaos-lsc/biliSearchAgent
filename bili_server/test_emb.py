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

from dotenv import load_dotenv, find_dotenv

# 从 .env 文件加载环境变量
load_dotenv(find_dotenv())

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


with open("book.txt", "r", encoding="utf-8") as f:
    rag.insert(f.read())

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

