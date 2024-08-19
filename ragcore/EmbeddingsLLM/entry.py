import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader, JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.vectorstores import Chroma
from ragcore.CommonCore.secret_utils.config import get_settings
from ragcore.CommonCore.llm_utils.get_embedding_function import get_embedding_function
from ragcore.EmbeddingsLLM.args import FineTuneLLMArgs, parse_arguments
from ragcore.CommonCore.audit.logging import logger
from langchain_community.document_loaders import Docx2txtLoader,TextLoader
from ragcore.CommonCore.secret_utils.config import get_settings
import json

class FineTuneLLM:
    def __init__(self, arguments):
        self.arguments = arguments
        self.settings = get_settings()
        

    def clear_database(self):
        if os.path.exists(self.arguments.vectorstore_path):
            shutil.rmtree(self.arguments.vectorstore_path)

    def load_documents(self, input_path):
        # Load documents in a directory. Mixing of not supported PDFs, JSON and DOCX
        docx_files = [f for f in os.listdir(input_path) if f.endswith('.docx')]
        pdf_files = [f for f in os.listdir(input_path) if f.endswith('.pdf')]
        json_files = [f for f in os.listdir(input_path) if f.endswith('.json')]
        print("json_files",json_files)
        if docx_files:
            document_loader = []
            for docx in docx_files:
                docx_path = os.path.join(input_path, docx)
                loader = Docx2txtLoader(docx_path)                
                document_loader.append(loader.load())

        elif pdf_files:
            logger.info("ℹ️ Loading PDF files")
            document_loader = PyPDFDirectoryLoader(
                input_path).load()
        elif json_files:
            logger.info("ℹ️ Loading JSON files")
            document_loader=[]
            for json_file in json_files:
                json_path = os.path.join(input_path, json_file)
                with open(json_path, 'r') as f:
                    data = json.load(f)
                with open(os.path.join(input_path,"temp.txt"), "w") as f:
                    f.write(data.get("content", ""))                    
                loader = TextLoader(os.path.join(input_path,"temp.txt"))   
                data = loader.load()             
                document_loader.append(data)
        else:
            document_loader = None
            raise FileNotFoundError(
                "No DOCX or PDF or JSON files NOT found in the specified directory")
        
        return document_loader

    def split_documents(self, documents: list[Document]):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=0,
            length_function=len,
            is_separator_regex=False,
        )
        return text_splitter.split_documents(documents)

    def add_to_chroma(self, chunks: list[Document]):
        # Load the existing database.
        db = Chroma(
            persist_directory=self.arguments.vectorstore_path,
            embedding_function=get_embedding_function(
                self.arguments.embedding_source, self.settings.OPENAI_API_KEY)
        )
        logger.info(
            f"Selected {self.arguments.embedding_source} 🧠 for embeddings")

        # Calculate Page IDs.
        chunks_with_ids = self.calculate_chunk_ids(chunks)

        # Add or Update the documents.
        # IDs are always included by default
        existing_items = db.get(include=[])
        existing_ids = set(existing_items["ids"])
        logger.info(f" ℹ️ Number of existing documents in DB: {len(existing_ids)}")

        # Only add documents that don't exist in the DB.
        new_chunks = []
        for chunk in chunks_with_ids:
            
            if chunk.metadata["id"] not in existing_ids:
                new_chunks.append(chunk)

        if len(new_chunks):           
            new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
            db.add_documents(new_chunks, ids=new_chunk_ids)
            db.persist()
            response =f"📃 Adding new documents: {len(new_chunks)}"
            logger.info(response)
            return response
        else:
            response = "Document already exists in the DB."
            logger.info(response)
            return response


    def calculate_chunk_ids(self,chunks):

        # This will create IDs like "data/monopoly.pdf:6:2"
        # Page Source : Page Number : Chunk Index

        last_page_id = None
        current_chunk_index = 0

        for chunk in chunks:            
            source = chunk.metadata.get("source")
            page = chunk.metadata.get("page")
            current_page_id = f"{source}:{page}"

            # If the page ID is the same as the last one, increment the index.
            if current_page_id == last_page_id:
                current_chunk_index += 1
            else:
                current_chunk_index = 0

            # Calculate the chunk ID.
            chunk_id = f"{current_page_id}:{current_chunk_index}"
            last_page_id = current_page_id

            # Add it to the page meta-data.
            chunk.metadata["id"] = chunk_id

        return chunks

    def persist_embeddings(self):
        # Vectors are stored in the Chroma DB.
        if self.arguments.reset_vectorstore:
            logger.info(f"ℹ️ Clearing Database: {self.arguments.vectorstore_path}")
            self.clear_database()

        documents = self.load_documents(self.arguments.document_path)
        documents = self.split_documents(documents)
        respone = self.add_to_chroma(documents)
        return respone


def main():
    # args = parse_arguments()
    args = {
        "document_path": "training_data\pdf_files" ,
        "reset_vectorstore"  : True
    }
    args = FineTuneLLMArgs(**args)
    mapper = FineTuneLLM(args)
    mapper.persist_embeddings()
    logger.info("✅ Document Training Task is now complete")


if __name__ == "__main__":
    main()
