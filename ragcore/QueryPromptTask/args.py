from pydantic import BaseModel, Field
from ragcore.SupportUtils.package_utils.arguments_utils import ArgumentsUnpacker


from pydantic import BaseModel, Field

# Base class to hold the common fields
class BaseDocuPromptArgs(BaseModel):
    query: str = Field(description="query")
    llm_temperature: float = Field(default=0, description="llm_temperature")
    embedding_source: str = Field(default="openai", description="embedding_source")
    modelid: str = Field(default="gpt-4o-mini", description="modelid")
    vectorstore_path: str = Field(default="vectorstore/chroma.sqlite3", description="vectorstore_path")

# Inherited class for single document prompts
class DocuPromptArgs(BaseDocuPromptArgs):
    file_name: str = Field(description="filename")

# Inherited class for multiple document prompts
class MultiDocuPromptArgs(BaseDocuPromptArgs):
    pass  # No additional fields required

class PDFdirectoryPromptArgs(BaseDocuPromptArgs):
    input_directory: str = Field(description="input_directory")
