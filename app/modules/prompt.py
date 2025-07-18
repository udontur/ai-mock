def init_prompt():
    """
    Initialize the prompt module.
    This function is called to set up any necessary configurations or
    initial states for the prompt module.
    """
    global prompt_parse_raw_latex
    prompt_parse_raw_latex = """
    You are an expert assistant tasked with accurately extracting exam questions from the provided exam written in latex. Follow these instructions precisely:
    Extract only the full latex of each question, including any problem descriptions, context, and the question itself, exactly as it appears in the input.
    Do not include any additional commentary, answers, explanations, scores, or information beyond the extracted questions.
    Separate each extracted question with exactly one blank line, each individual question should be on the same line.
    Each question should not be numbered. 
    All responses must only contain ASCII characters. 
    If the input contains no questions, respond with the exact text: "No questions found.".
    If a question appears incomplete or truncated, respond with the exact text: "Incomplete question: <question>".
    Adhere strictly to these rules to ensure clarity and accuracy.
    The following is the given text:
    """
