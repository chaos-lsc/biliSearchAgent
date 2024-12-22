#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: MuyuCheney
# Date: 2024-10-15

import os

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from pydantic import BaseModel
from utils import create_workflow

from dotenv import load_dotenv, find_dotenv

# 从 .env 文件加载环境变量
load_dotenv(find_dotenv())

# Get the API key and model to use, falling back to alternatives if necessary

# api_key = os.getenv('OPENAI_API_KEY')
# model = os.getenv('openai_model')
api_key = os.getenv('GLM_API_KEY')
model = os.getenv('glm_model')

# print(f"{api_key},{model}")

# 初始化图节点的工作流
chain = create_workflow(os.getenv('OPENAI_API_BASE'), api_key, model)


class Input(BaseModel):
    """定义输入(pydantic模型)"""
    input: str


class Output(BaseModel):
    """定义输出(pydantic模型)"""
    output: dict


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


# 添加路由，定义工作流和输入输出类型
add_routes(
    app,
    chain.with_types(input_type=Input, output_type=Output),
    path="/biliagent_chat",
)

# 运行代码时，使用 Uvicorn 运行 app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
