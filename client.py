import os
import streamlit as st
from langserve import RemoteRunnable
import networkx as nx
import plotly.graph_objs as go
import logging
from bili_server.rag_tools.document_loader import DocumentLoader
import xxhash
# 设置日志记录器
logger = logging.getLogger(__name__)
@st.dialog("Knowledge Graph Stats", width="large")
def show_kg_stats_dialog():
    """Dialog showing detailed knowledge graph statistics and visualization."""
    try:
        # Use the correct filename in dickens directory
        graph_path = "./dickens/graph_chunk_entity_relation.graphml"
        
        if not os.path.exists(graph_path):
            st.markdown("> [!graph] ⚠ **Knowledge Graph file not found.** Please insert some documents first.")
            return
            
        graph = nx.read_graphml(graph_path)
            
        # Basic stats
        stats = {
            "Nodes": graph.number_of_nodes(),
            "Edges": graph.number_of_edges(),
            "Average Degree": round(sum(dict(graph.degree()).values()) / graph.number_of_nodes(), 2) if graph.number_of_nodes() > 0 else 0
        }
        
        # Display stats with more detail
        st.markdown("## Knowledge Graph Statistics")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Nodes", stats["Nodes"])
        with col2:
            st.metric("Total Edges", stats["Edges"])
        with col3:
            st.metric("Average Degree", stats["Average Degree"])
        
        # Add detailed analysis
        st.markdown("## Graph Analysis")
        
        # Calculate additional metrics
        if stats["Nodes"] > 0:
            density = nx.density(graph)
            components = nx.number_connected_components(graph.to_undirected())
            
            st.markdown(f"""
            - **Graph Density:** {density:.4f}
            - **Connected Components:** {components}
            - **Most Connected Nodes:**
            """)
                        
            # Create table headers
            table_lines = [
                "| Node ID | SHA-12 | Connections |",
                "|---------|--------|-------------|"
            ]
            
            # Add rows for top nodes
            degrees = dict(graph.degree())
            top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:5]
            for node, degree in top_nodes:
                # Get first 12 chars of SHA hash
                sha_hash = xxhash.xxh64(node.encode()).hexdigest()[:12]
                table_lines.append(f"| `{node}` | `{sha_hash}` | {degree} |")
            
            # Display the table
            st.markdown("\n".join(table_lines))
        
        # Generate visualization if there are nodes
        if stats["Nodes"] > 0:
            st.markdown("## Knowledge Graph Visualization")
            
            try:
                from pyvis.network import Network
                import random
                
                st.markdown("*Generating interactive network visualization...*")
                
                net = Network(height="600px", width="100%", notebook=True)
                net.from_nx(graph)
                
                # Apply visual styling
                for node in net.nodes:
                    node["color"] = "#{:06x}".format(random.randint(0, 0xFFFFFF))
                
                # Save and display using the same filename pattern
                html_path = "./dickens/graph_chunk_entity_relation.html"
                net.save_graph(html_path)
                
                # Display the saved HTML
                with open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                st.components.v1.html(html_content, height=600)
                    
            except ImportError:
                st.markdown("⚠️ Please install pyvis to enable graph visualization: `pip install pyvis`")
            except Exception as e:
                st.markdown(f"❌ **Error generating visualization:** {str(e)}")
        
    except Exception as e:
        logger.error(f"Error getting graph stats: {str(e)}")
        st.markdown(f"❌ **Error getting graph stats:** {str(e)}")


def show_kg_stats():
    """Show knowledge graph statistics."""
    try:
        rag=DocumentLoader.get_instance().rag
        status_message = ""
        if rag is None:
            status_message = "Knowledge Graph not initialized yet"
            return
            
        graph = rag.chunk_entity_relation_graph._graph
        if graph is None:
            status_message = "Knowledge Graph is empty"
            return
            
        # Calculate stats
        nodes = graph.number_of_nodes()
        edges = graph.number_of_edges()
        avg_degree = round(sum(dict(graph.degree()).values()) / nodes, 2) if nodes > 0 else 0
        
        # Create degree distribution for plotting
        degrees = dict(graph.degree())
        degree_dist = {}
        for d in degrees.values():
            degree_dist[d] = degree_dist.get(d, 0) + 1
            
        # Create plot
        fig = go.Figure(data=[
            go.Bar(x=list(degree_dist.keys()), y=list(degree_dist.values()))
        ])
        fig.update_layout(
            title="Node Degree Distribution",
            xaxis_title="Degree",
            yaxis_title="Count"
        )
        
    #     # Update state with stats and plot
    #     state.kg_stats = {
    #         "nodes": nodes,
    #         "edges": edges,
    #         "avg_degree": avg_degree,
    #         "plot": fig
    #     }
    #     state.show_kg_stats = True
        
    except Exception as e:
        logger.error(f"Error getting graph stats: {str(e)}")
        status_message = f"Error getting graph stats: {str(e)}"

# 使用 Markdown 和样式增强标题，包括图标和渐变色
st.markdown("""
<h1 style='text-align: center; color: blue; background: linear-gradient(to right, red, purple); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
      📊 BiliBili Search 检索增强助手
</h1>
""", unsafe_allow_html=True)

# 创建一个外部容器用于整体布局
with st.container():
    # 设置自定义样式以控制布局
    st.markdown("""
    <style>
        .search-container {
            display: flex;
            align-items: flex-start; /* 对齐到顶部 */
            gap: 5px; /* 组件之间的间距 */
        }
        div[data-baseweb="input"] {
            height: 50px; /* 设置输入框的高度 */
            flex-grow: 1; /* 让输入框占据剩余空间 */
        }
        div[data-baseweb="button"] {
            height: 50px; /* 使按钮高度与输入框一致 */
        }
        .buttons-column {
            margin-top: 30px; /* 向下移动按钮30px */
        }
    </style>
    """, unsafe_allow_html=True)

    # 创建搜索框容器
    with st.container():
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        
        col_input, col_search, col_clear = st.columns([4, 0.5, 0.5])  # 分配比例给各列
        with col_input:
            # 使用 st.empty() 创建一个可替换的容器
            input_text_container = st.empty()
            # # 在容器中添加文本输入框
            # input_text = input_text_container.text_input("", placeholder="请输入问题:", key="input")
        with col_search:
            st.markdown('<div class="buttons-column">', unsafe_allow_html=True)
            search_button = st.button("搜索", key="search")
            st.markdown('</div>', unsafe_allow_html=True)  # 关闭按钮容器
        with col_clear:
            st.markdown('<div class="buttons-column">', unsafe_allow_html=True)
            clear_button = st.button("清空", key="clear")
            st.markdown('</div>', unsafe_allow_html=True)  # 关闭按钮容器
        
        st.markdown('</div>', unsafe_allow_html=True)  # 关闭搜索框容器

# 如果点击了清空按钮，则清空输入框中的文本
if clear_button:
    # 使用 st.empty() 重新创建一个空的容器，替换原来的文本输入框
    input_text_container.empty()
    # 在新的容器中添加一个新的文本输入框
    input_text = st.text_input("", placeholder="请输入问题:", key="input")
    # 清空输入框中的文本，但保留输入框
    st.session_state.input_text = ""
    # 手动更新 input_text 变量的值
    input_text = ""

    # # 显示知识图谱按钮和 expander
    # show_knowledge_graph = st.button('显示知识图谱')

    # if show_knowledge_graph:
    #     with st.sidebar("知识图谱", expanded=True):
    #         show_kg_stats_dialog()


# 初始化session state中的变量，如果它还不存在的话
if 'show_kg' not in st.session_state:
    st.session_state.show_kg = False

# 显示按钮，当点击时改变session state中的show_kg状态
if st.sidebar.button('显示/隐藏 知识图谱'):
    st.session_state.show_kg = not st.session_state.show_kg  # 切换状态

# 在侧边栏中条件性地显示知识图谱
with st.sidebar:
    if st.session_state.show_kg:
        with st.expander("知识图谱", expanded=st.session_state.show_kg):
            st.write("知识图谱加载中......")
            # 调用显示知识图谱统计对话框或相关内容的函数
            show_kg_stats_dialog()

def show_kg_stats_dialog():
    # 这里放置展示知识图谱统计数据的代码
    st.write("这是知识图谱的统计数据对话框")

# 注意：你需要自己定义show_kg_stats_dialog函数的具体实现。
                

if search_button:
    with st.spinner("正在处理..."):
        try:
            app = RemoteRunnable("http://localhost:8000/biliagent_chat")
            responses = []
            for output in app.stream(input={"input": input_text}, config={"recursion_limit":100}):
                responses.append(output)
                print(output)
            print(responses)
            if responses:
                st.subheader('分析结果')
                last_response = responses[-1]
                print(last_response)
                print("--------------")
                if last_response is not None and "generation" in last_response:
                    print(last_response["generation"])
                    st.markdown(last_response["generation"])
                else:
                    st.markdown("No generation data available.")
        except Exception as e:
            st.error(f"处理时出现错误: {str(e)}")
            print(last_response["generation"])
            st.markdown(last_response["generation"])