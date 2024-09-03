from operator import itemgetter
from pydantic import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate,PromptTemplate
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from ragcore.SupportUtils.secret_utils.config import get_settings
from langchain.output_parsers import PydanticOutputParser,StructuredOutputParser,ResponseSchema
from ragcore.SupportUtils.llm_utils.get_embedding_function import get_embedding_function
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS, Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.data_anonymizer import PresidioReversibleAnonymizer
from langchain_community.document_loaders import Docx2txtLoader,TextLoader,PyPDFDirectoryLoader
  
    
# 1. Initialize anonymizer
anonymizer = PresidioReversibleAnonymizer()
# 2. Load the data: In our case data's already loaded
# 3. Anonymize the data before indexing
documents = PyPDFDirectoryLoader(path="training_data/pdf_files").load()
for doc in documents:
    doc.page_content = anonymizer.anonymize(doc.page_content)

# 4. Split the documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_documents(documents)
# print(chunks)
# 5. Index the chunks (using OpenAI embeddings, because the data is already anonymized)

# Create embeddings and index the chunks
embeddings = get_embedding_function(embedding_source="openai", open_ai_key=get_settings().OPENAI_API_KEY)

docsearch = Chroma.from_documents(chunks, embeddings,persist_directory = "vectorstore").as_retriever()
docsearch_filter = docsearch.get_relevant_documents(query=anonymizer.anonymize("Who is McLeran?"))
print("doc searcgtype: \n",type(docsearch))
print("docfiltertype: \n",type(docsearch_filter))

retriever  = Chroma.from_documents(docsearch_filter, embeddings).as_retriever()

model = ChatOpenAI(temperature=0.3)


_inputs = RunnableParallel(
    question=RunnablePassthrough(),
    # It is important to remember about question anonymization
    anonymized_question=RunnableLambda(anonymizer.anonymize),
)
response_schemas = [
    ResponseSchema(name="content", description="answer to the user's question"),
    ResponseSchema(
        name="page_number",
        description="Page number based on the source title",
    ),
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
# 6. Create anonymizer chain
template = """Answer the question based only on the following context:
{context}

Question: {anonymized_question}
Use the following format: {format_instructions}
"""
format_instructions = output_parser.get_format_instructions()

prompt = PromptTemplate(
    template=template,
    input_variables=["question"],
    partial_variables={"format_instructions": format_instructions},
)
anonymizer_chain = (
    _inputs
    | {
        "context": itemgetter("anonymized_question") | retriever,
        "anonymized_question": itemgetter("anonymized_question"),
    }
    | prompt
    | model
    | output_parser
)
response = anonymizer_chain.invoke(
    "Who is McLeran?"
)
response["content"] = anonymizer.deanonymize(response["content"])
print(response)
