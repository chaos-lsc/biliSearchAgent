import streamlit as st
from langserve import RemoteRunnable

# 使用 Markdown 和样式增强标题，包括图标和渐变色
st.markdown("""
<h1 style='text-align: center; color: blue; background: linear-gradient(to right, red, purple); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
      📊 BiliBili 实时数据分析
</h1>
""", unsafe_allow_html=True)


# 创建两个列，一个用于搜索文本框，一个用于搜索按钮
col1, col2 = st.columns([4, 1])  # 调整比例以适应您的布局需求

# 在第一列中放置搜索文本框
with col1:
    input_text = st.text_input("", placeholder="请输入问题:", key="2")

# 在第二列中放置搜索按钮
with col2:
    search_button = st.button("搜索")

# 添加一个新的按钮用于清空问题
with col2:
    clear_button = st.button("清空")

# 使用自定义CSS样式来设置搜索框和按钮的高度
st.markdown("""
<style>
div[data-baseweb="input"] {
    height: 70px; /* 设置输入框的高度 */
}
div[data-baseweb="button"] {
    height: 40px; /* 设置按钮的高度 */
}
</style>
""", unsafe_allow_html=True)

if search_button:
    with st.spinner("正在处理..."):
        # try:
        app = RemoteRunnable("http://localhost:8000/biliagent_chat")
        responses = []
        for output in app.stream(input={"input": input_text},config={"recursion_limit":100}):
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
        # except Exception as e:
        #     st.error(f"处理时出现错误: {str(e)}")

# 如果点击了清空按钮，则清空输入框中的文本
if clear_button:
    input_text = ""