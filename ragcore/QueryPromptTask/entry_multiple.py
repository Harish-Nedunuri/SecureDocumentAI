from ragcore.QueryPromptTask.args import MultiDocuPromptArgs
from ragcore.SupportUtils.audit.logging import logger
from ragcore.SupportUtils.secret_utils.config import get_settings
# from langchain.chains import RunnableSequence    
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import uuid
from langchain_community.vectorstores import Chroma
from langchain.utils.openai_functions import (
    convert_pydantic_to_openai_function,
)
import os
from typing import List
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from ragcore.SupportUtils.llm_utils.get_embedding_function import get_embedding_function
from ragcore.SupportUtils.llm_utils.query_vectorstore_data import get_embedding_chunks
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from ragcore.QueryPromptTask.src.input_prompt_template import get_prompt
from pydantic import BaseModel,Field
from ragcore.SupportUtils.package_utils.arguments_utils import ArgumentsUnpacker

class ResponseDocument(BaseModel):
    content : str = Field(description="Text Output")
    page_number: int = Field(description= "Page number based on the source title")   
    

class MultiDocPromptResponse:
    def __init__(self, arguments):
        self.arguments = arguments
        self.settings = get_settings()

    def read_code(self):     
        response = {}
        # Prepare the DB.
        embedding_function = get_embedding_function(self.arguments.embedding_source,self.settings.OPENAI_API_KEY)
        # k_value, source_list,page_list= get_embedding_chunks(self.arguments.query,self.arguments.vectorstore_path) 
        
        db = Chroma(persist_directory="vectorstore" ,embedding_function=embedding_function)
        
        # Search the DB.
        results = db.similarity_search_with_score(self.arguments.query, k=2)
        print(results)
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        document_metadata = [doc.metadata["source"] for doc, _score in results]
        document_pages= [doc.metadata["page"] for doc, _score in results]

        prompt_template = get_prompt()        
        model = ChatOpenAI(model=self.arguments.modelid, \
                            temperature=self.arguments.llm_temperature,\
                                api_key = self.settings.OPENAI_API_KEY)
        
        # openai_functions = [convert_pydantic_to_openai_function(ResponseDocument)]
        parser = PydanticOutputParser(pydantic_object=ResponseDocument)
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["query","context"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        
        chain = prompt | model | parser
        # llm_output = model.invoke(prompt)
        llm_output = chain.invoke({"query":self.arguments.query,"context":context_text})
        response["content"] = llm_output.content       
        response["source_document"] = document_metadata
        response["page_number"] = llm_output.page_number   
        return response

def parse_arguments() -> MultiDocuPromptArgs:
    parser = ArgumentsUnpacker(MultiDocuPromptArgs)
    return parser.run()

def main():
    args = parse_arguments()
    # args = {     
    #  "query":"What is the behaviour history of Patches"    
    # }
    # args = MultiDocuPromptArgs(**args)
    mapper = MultiDocPromptResponse(args)
    response = mapper.read_code()
    print(response)
    logger.info(" Multi Document Prompt Task is now complete")

if __name__ == "__main__":
    main()


    