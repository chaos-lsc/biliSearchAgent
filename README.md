
## 项目介绍
Bilibili视频平台上涵盖了从科技、教育到文化、艺术等广泛领域的高质量内容，吸引了大量追求知识和自我提升的年轻用户。随着数字技术和人工智能的迅猛发展，知识检索的形式正在经历深刻的创新与变革。尽管Bilibili作为领先的在线视频平台，在多媒体内容分发和用户互动方面取得了显著成就，但在智能化检索方面仍有提升空间。为了应对这一挑战并进一步增强用户体验，我们推出了“Bilibili知识检索增强工具”。
本项目的核心目标是构建一个智能的知识检索系统，旨在通过以下方式加强Bilibili的知识发现能力：
1. 知识图谱的构建：利用先进的知识图谱技术，我们将Bilibili丰富的知识区视频信息结构化为语义网络。这种表示模型不仅能够将分散的知识点连接起来，还能揭示不同概念之间的潜在关系，从而提供更加深入和全面的理解。
2. 专业AI智能体的训练：基于大规模语言模型（LLM），我们训练了一个专门针对Bilibili内容的专业AI智能体。这个智能体能够以生成式对话应用的形式，提供自然流畅的人机交互体验，帮助用户更高效地获取所需信息。
3. 问答系统的开发：结合知识图谱与AI智能体，我们开发了一套强大的问答系统。该系统不仅能根据用户的问题快速定位到相关的视频内容，还能通过深度分析问题背后的意图，给出精准且富有洞察力的回答。
4. 可视化探索：为了让用户更好地理解知识图谱的结构和内容，我们提供了直观的可视化工具。这些工具允许用户以图形化的方式浏览和探索知识间的联系，极大地增强了学习和研究的乐趣。
5. RAG检索增强：为了确保系统的灵活性和可扩展性，我们还在系统中增加了基于Retrieval-Augmented Generation (RAG) 的检索增强机制。

![workflow_intro](/pic/workflow.PNG)

## 技术架构
![architecture_intro](/pic/architecture.png)

## 使用方法
```bash
# 安装依赖
pip install -r requirements.txt 
# 根目录下创建.env文件
# 在.env文件中填写下面内容
#GLM_API_BASE='https://open.bigmodel.cn/api/paas/v4'
#GLM_API_KEY='<your_api_key>'
#SF_API_BASE='https://api.siliconflow.cn/v1'
#SF_API_KEY='<your_api_key>'

# 申请API_KEY：
# 申请GLM_API_KEY地址：https://open.bigmodel.cn/usercenter/proj-mgmt/apikeys
# 申请SF_API_KEY地址：https://cloud.siliconflow.cn/account/ak

# 启动服务端
python server.py
# 启动客户端
streamlit run client.py
```



