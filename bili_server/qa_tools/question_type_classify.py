from bili_server.qa_tools.prompt_template import QUESTION_PARSE_TEMPLATE
from bili_server.qa_tools.chat_with_ai import chat_with_ai
from bili_server.qa_tools.question_type import QuestionType, QUESTION_MAP

def classify_question_type(question: str) -> QuestionType:
    """
    解析问题的意图
    Args:
        question(str): 输入的问题
    Returns:
        QuestionType: 问题的意图类型
    """
    
    prompt = f"{QUESTION_PARSE_TEMPLATE}\n{question}"

    response= chat_with_ai(prompt)


    question_type = QUESTION_MAP[response]

    return question_type