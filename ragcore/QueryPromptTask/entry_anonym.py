from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS, Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.data_anonymizer import PresidioReversibleAnonymizer
from langchain_community.document_loaders import Docx2txtLoader,TextLoader,PyPDFDirectoryLoader
# 1. Initialize anonymizer
anonymizer = PresidioReversibleAnonymizer(
    # Faker seed is used here to make sure the same fake data is generated for the test purposes
    # In production, it is recommended to remove the faker_seed parameter (it will default to None)
    faker_seed=42,
)
# 2. Load the data: In our case data's already loaded
# 3. Anonymize the data before indexing
documents = PyPDFDirectoryLoader(path="training_data/pdf_files").load()
for doc in documents:
    doc.page_content = anonymizer.anonymize(doc.page_content)

# 4. Split the documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_documents(documents)
print(chunks)
# 5. Index the chunks (using OpenAI embeddings, because the data is already anonymized)
embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(chunks, embeddings)
retriever = docsearch.as_retriever()



# 6. Create anonymizer chain
template = """Answer the question based only on the following context:
{context}

Question: {anonymized_question}
"""
prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI(temperature=0.3)


_inputs = RunnableParallel(
    question=RunnablePassthrough(),
    # It is important to remember about question anonymization
    anonymized_question=RunnableLambda(anonymizer.anonymize),
)

anonymizer_chain = (
    _inputs
    | {
        "context": itemgetter("anonymized_question") | retriever,
        "anonymized_question": itemgetter("anonymized_question"),
    }
    | prompt
    | model
    | StrOutputParser()
)
chain_with_deanonymization = anonymizer_chain | RunnableLambda(anonymizer.deanonymize)
response = chain_with_deanonymization.invoke(
    "Who is McLeran?"
)
print(response)