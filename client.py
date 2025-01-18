import streamlit as st
from langserve import RemoteRunnable

# 使用 Markdown 和样式增强标题，包括图标和渐变色
st.markdown("""
<h1 style='text-align: center; color: blue; background: linear-gradient(to right, red, purple); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
      📊 BiliBili 实时数据分析
</h1>
""", unsafe_allow_html=True)

# 设置自定义样式以控制布局
st.markdown("""
<style>
    .search-container {
        position: relative;
        width: 100%;
        max-width: 800px; /* 设置最大宽度 */
        margin: 0 auto; /* 水平居中 */
    }
    div[data-baseweb="input"] {
        height: 70px; /* 设置输入框的高度 */
        width: 100%; /* 输入框全宽 */
        box-sizing: border-box; /* 确保内边距和边框包含在元素的总宽高之内 */
    }
    .buttons-container {
        display: flex;
        justify-content: flex-end; /* 按钮右对齐 */
        gap: 5px; /* 按钮之间的间距 */
        margin-top: 20px; /* 按钮距离输入框底部的距离 */
    }
    div[data-baseweb="button"] {
        height: 35px; /* 设置按钮的高度 */
    }
</style>
""", unsafe_allow_html=True)

# 创建一个外部容器用于整体布局，并设置最大宽度和水平居中
with st.container():
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # 创建搜索框
    input_text = st.text_input("", placeholder="请输入问题:", key="input")

    # 创建按钮容器，并确保它位于输入框的下方
    st.markdown('<div class="buttons-container">', unsafe_allow_html=True)
    col_search, col_clear = st.columns([1, 1])  # 创建两列以放置按钮
    
    with col_search:
        search_button = st.button("搜索", key="search")
    
    with col_clear:
        clear_button = st.button("清空", key="clear")
    
    st.markdown('</div>', unsafe_allow_html=True)  # 关闭按钮容器
    st.markdown('</div>', unsafe_allow_html=True)  # 关闭搜索框容器

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
                st.markdown(last_response["generate"]["generation"])

                # 收缩显示 documents 的内容
                with st.expander("查看详细推荐视频信息"):
                    for idx, doc in enumerate(last_response.get("documents", [])):
                        st.write(f"### 视频 {idx + 1}")
                        st.json(doc)  # 展示每个文档的详细内容
            else:
                st.info("没有返回结果。")
        except Exception as e:
            st.error(f"处理时出现错误: {str(e)}")

# 如果点击了清空按钮，则清空输入框中的文本
if clear_button:
    st.session_state.input = ""  # 清除文本输入框的内容