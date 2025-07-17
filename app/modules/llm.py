from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from os import getenv


def get_response(user_prompt, text):
    prompt = """
        {{user_prompt}}

        {text}
    """
    prompt = PromptTemplate(input_variables=["text"], template=prompt)
    llm = ChatOpenAI(
        openai_api_key=getenv("OPENROUTER_API_KEY"),
        openai_api_base=getenv("OPENROUTER_API_BASE"),
        model_name=getenv("OPENROUTER_MODEL_NAME"),
    )
    llm_chain = prompt | llm
    response = llm_chain.invoke(input={"text": text})
    return response
