from ragcore.QueryPromptTask.args import DocuPromptArgs,MultiDocuPromptArgs
from ragcore.QueryPromptTask.entry_single import GetPromptResponse
from ragcore.QueryPromptTask.entry_multiple import MultiDocPromptResponse
from fastapi import HTTPException
from fastapi import APIRouter, Depends, status

from ragcore.SupportUtils.security_utils.oauth2_security import oauth2Scheme as get_current_token
router = APIRouter(
    prefix="/single-document-query",
    tags=["Document Query using LLM"],
    responses={404: {"description": "Not found"}},
    dependencies={Depends(get_current_token)}
)
@router.post('', status_code=status.HTTP_201_CREATED, description="Use this API to ask a question to the LLM about the document. This API will return answers only from the documents that  have embedding_status = 1")
async def single_document_query( 
    file_name: str,
    query: str,    
):
    try:        
        args = DocuPromptArgs(
            file_name=file_name,
            query = query                 
        )
        mapper = GetPromptResponse(args)
        response  = mapper.read_code()
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

multi_router = APIRouter(
    prefix="/multiple-document-query", 
    tags=["Document Query using LLM"],
    responses={404: {"description": "Not found"}},
    dependencies={Depends(get_current_token)}
)
@multi_router.post('', status_code=status.HTTP_201_CREATED, description="Use this API to ask a question to the LLM about any document in the embeddings. This API will return answers only from the documents that  have embedding_status = 1")
async def multiple_document_query(     
    query: str       
):
    try:        
        args = MultiDocuPromptArgs(            
            query = query                 
        )        
        mapper = MultiDocPromptResponse(args)
        response = mapper.read_code()
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

