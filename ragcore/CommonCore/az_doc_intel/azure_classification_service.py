import json
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient,AnalysisFeature
from ragcore.CommonCore.secret_utils.config import get_settings
from ragcore.CommonCore.audit.logging import logger
import uuid
from azure.core.exceptions import HttpResponseError
from dotenv import find_dotenv, load_dotenv

from azure.core.credentials import AzureKeyCredential
# from azure.ai.documentintelligence import DocumentIntelligenceAdministrationClient
# from azure.ai.documentintelligence.models import (
#     AzureBlobContentSource,
#     ClassifierDocumentTypeDetails,
#     BuildDocumentClassifierRequest,
# )
# [START classify_document]
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from ragcore.CommonCore.secret_utils.config import get_settings
import os
from urllib.parse import urlparse,unquote
settings = get_settings()

def az_doc_int_classify_document(file_local, classifier_id): 
    document_analysis_client = DocumentAnalysisClient(
        endpoint=settings.AFR_ENDPOINT, credential=AzureKeyCredential(settings.AFR_KEY)
    )
    
    with open(file_local, "rb") as f:
        poller = document_analysis_client.begin_classify_document(
            classifier_id, document=f
        )
        result = poller.result()

    page_wise_list = []
    for doc in result.documents:
        for region in doc.bounding_regions:
            page_wise_list.append({
                "page_type": doc.doc_type or None,
                "classifier_confidence": doc.confidence,
                "pages": region.page_number
            })
    
    return page_wise_list

   

