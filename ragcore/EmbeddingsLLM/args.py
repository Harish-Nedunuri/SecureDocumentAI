from pydantic import BaseModel, Field
from ragcore.SupportUtils.package_utils.arguments_utils import ArgumentsUnpacker


class EmbeddingsArgs(BaseModel):
    document_path: str = Field(description = "document_path")
    embedding_source: str = Field(default="openai",description="embedding_source: aws, openai, local")    
    vectorstore_path: str  =  Field(default="vectorstore",description="vectorstore_path")
    reset_vectorstore: bool = Field(default=False,description = "reset_vectorstore")

     
def parse_arguments() -> EmbeddingsArgs:
    parser = ArgumentsUnpacker(EmbeddingsArgs)
    return parser.run()
