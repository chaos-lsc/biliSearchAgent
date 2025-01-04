import os
from openai import OpenAI


def chat_with_ai(question_with_prompt: str) -> str:
    """
    与AI进行对话，返回AI的回复。

    Args:
        question_with_prompt (str): 包含问题和提示的字符串。

    Returns:
        str: AI的回复内容。
    """
    client = OpenAI(api_key=os.getenv("GLM_API_KEY"),
                  base_url=os.getenv("GLM_API_BASE"),
                  )
    
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[{"role": "user", "content": question_with_prompt}],
        top_p=0.7,
        temperature=0.95,
        max_tokens=1024,
    )
    return response.choices[0].message.content