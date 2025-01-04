#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Chaos
# Date: 2025-01-01

import os

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from pydantic import BaseModel
# from utils import create_workflow
from bili_server.qa_tools.question_type_classify import classify_question_type
from bili_server.qa_tools.function_tools import map_question_to_function
from dotenv import load_dotenv, find_dotenv

# 从 .env 文件加载环境变量
load_dotenv(find_dotenv())

# Create a FastAPI app with specified metadata
app = FastAPI(
    title="BiliAgent Server",
    version="1.0",
    description="An API named bili_server designed specifically for real-time retrieval of live data from BiliBili."
)


# 定义根路径(/)重定向到docs(/docs)
@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

@app.get("/stream")
async def qa_workflow(question: str):
    print(question)
    question_type = classify_question_type(question)
    print(question_type)
    function = map_question_to_function(question_type)

    result = function(question)
    print(result)


# 运行代码时，使用 Uvicorn 运行 app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
