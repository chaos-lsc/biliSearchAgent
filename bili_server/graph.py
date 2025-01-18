from typing import TypedDict,List
from bili_server.qa_tools.question_type_classify import QuestionType

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Args:
        input(str): question
        input_keywords(List[str]): 输入的关键字
        keywords_in_rag(List[str]): 在RAG中找到的关键字
        keywords_not_in_rag(List[str]): 在RAG中未找到的关键字
        generation(str): LLM generation
        documents(str): 检索到的文档
    """

    input: str
    question_type: QuestionType
    input_keywords: List[str]
    keywords_in_rag: List[str]
    keywords_not_in_rag: List[str]
    generation: str
    documents: str

    def __init__(self, input: str, question_type: QuestionType, input_keywords: List[str] = None, 
                 keywords_in_rag: List[str] = None, keywords_not_in_rag: List[str] = None, 
                 generation: str = "", documents: str = ""):
        self.input = input
        self.question_type = question_type
        self.input_keywords = input_keywords if input_keywords is not None else []
        self.keywords_in_rag = keywords_in_rag if keywords_in_rag is not None else []
        self.keywords_not_in_rag = keywords_not_in_rag if keywords_not_in_rag is not None else []
        self.generation = generation
        self.documents = documents