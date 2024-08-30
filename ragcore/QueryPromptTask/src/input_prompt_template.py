
def get_prompt():
    template = """
    You are an assistant for question-answering tasks.
    Answer the question based only on the following context: {context}
    If you don't know the answer, just say that you don't know.
    Answer the question: {query}, and provide source page.
    Use below format instructions:
    \n{format_instructions}\n
    
    """
    return template
