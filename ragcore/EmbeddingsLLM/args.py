from pydantic import BaseModel, Field
from ragcore.CommonCore.package_utils.arguments_utils import ArgumentsUnpacker


class FineTuneLLMArgs(BaseModel):
    document_path: str = Field(description = "document_path")
    embedding_source: str = Field(default="openai",description="embedding_source: aws, openai, local")    
    vectorstore_path: str  =  Field(default="vectorstore",description="vectorstore_path")
    reset_vectorstore: bool = Field(default=False,description = "reset_vectorstore")

     
def parse_arguments() -> FineTuneLLMArgs:
    parser = ArgumentsUnpacker(FineTuneLLMArgs)
    return parser.run()
