from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from os import getenv

def get_response(user_prompt, text):
    """
    Get response from LLM. Falls back to mock response if API keys are not configured.
    """
    # Check if required environment variables are set
    api_key = getenv("OPENROUTER_API_KEY")
    api_base = getenv("OPENROUTER_API_BASE")
    model_name = getenv("OPENROUTER_MODEL_NAME")
    
    if not api_key or not api_base or not model_name:
        # Return mock response for testing/development
        print("Warning: LLM API not configured, using mock response")
        return MockLLMResponse("Mock LLM response - API keys not configured")
    
    try:
        prompt_template = f"""
            {user_prompt}

            {{text}}
        """
        prompt = PromptTemplate(input_variables=["text"], template=prompt_template)
        llm = ChatOpenAI(
            openai_api_key=api_key,
            openai_api_base=api_base,
            model_name=model_name,
        )
        llm_chain = prompt | llm
        response = llm_chain.invoke(input={"text": text})
        return response
    except Exception as e:
        print(f"LLM API error: {e}")
        return MockLLMResponse(f"LLM processing failed: {e}")

class MockLLMResponse:
    """Mock LLM response for testing when API is not available"""
    def __init__(self, content):
        self.content = content
    
    def __str__(self):
        return self.content
