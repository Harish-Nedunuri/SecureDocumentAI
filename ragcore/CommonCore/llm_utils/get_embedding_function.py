from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_openai import OpenAIEmbeddings


def get_embedding_function(embedding_source,open_ai_key):
   
    if embedding_source == "aws":
        embeddings = BedrockEmbeddings(
            credentials_profile_name="default", region_name="us-east-1"
        )
    elif embedding_source == "local":
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
    elif embedding_source ==  "openai":
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002",api_key=open_ai_key)
    return embeddings
