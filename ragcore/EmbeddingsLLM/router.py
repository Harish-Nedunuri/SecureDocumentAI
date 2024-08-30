from fastapi import HTTPException
from ragcore.EmbeddingsLLM.args import EmbeddingsArgs
from ragcore.EmbeddingsLLM.entry import VectorStorePersist
from fastapi import APIRouter, Depends, status
from ragcore.SupportUtils.security_utils.oauth2_security import oauth2Scheme as get_current_token
from fastapi import  File, UploadFile
import os
import shutil

router = APIRouter(
    prefix="/vector-store-embeddings",
    tags=["Store Embeddings"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_token)]
)

# Define the directory where files should be saved
BASE_DIR = "training_data"
PDF_DIR = os.path.join(BASE_DIR, "pdf_files")

@router.post('', status_code=status.HTTP_201_CREATED, description="Use this API to Store the Embeddings to the vector store.")
async def vector_store_embeddings(
    file: UploadFile = File(...)
):
    try:
        # Determine the file extension
        _, file_extension = os.path.splitext(file.filename)

        # Define the destination path based on file extension
        if file_extension.lower() == ".pdf":
            save_path = os.path.join(PDF_DIR, file.filename)
            # Save the uploaded file
            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Only PDFs are allowed.")

        # Create an instance of FineTuneLLMArgs with the saved file path
        args = EmbeddingsArgs(
            document_path=PDF_DIR,
        )        
        # Create an instance of FineTuneLLM and persist embeddings
        mapper = VectorStorePersist(args)
        response = mapper.persist_embeddings()
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
