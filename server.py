#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Chaos
# Date: 2025-01-01

import os

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from pydantic import BaseModel
from utils import create_workflow
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

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

# 初始化图节点的工作流
chain = create_workflow()

class Input(BaseModel):
    input: str


class Output(BaseModel):
    output: dict

# 添加路由
add_routes(
    app,
    chain.with_types(input_type=Input, output_type=Output),
    path="/biliagent_chat",
)

# 运行代码时，使用 Uvicorn 运行 app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
