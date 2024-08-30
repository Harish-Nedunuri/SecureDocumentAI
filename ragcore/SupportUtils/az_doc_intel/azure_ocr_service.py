import json
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient,AnalysisFeature
from ragcore.SupportUtils.secret_utils.config import get_settings
from ragcore.SupportUtils.audit.logging import logger

async def extract_data_using_az(file_obj,AFR_ENDPOINT,AFR_KEY,MODEL_ID,high_resolution_on,file_location):
    logger.info(f"Started OCR Extraction with high_resolution as : {high_resolution_on}")
    data = {}
    if AFR_KEY is None:
        return data
    
    if AFR_ENDPOINT is None:
        return data    
    
    document_analysis_client = DocumentAnalysisClient(
    endpoint=AFR_ENDPOINT, credential=AzureKeyCredential(AFR_KEY)
    )   
    if file_location == "LOCAL":
        with open(file_obj, "rb") as f:
            
            features=[AnalysisFeature.OCR_HIGH_RESOLUTION] if high_resolution_on else None            

            poller = document_analysis_client.begin_analyze_document(MODEL_ID, f,features=features)

            data = poller.result()
            # Convert the data to a JSON-serializable format if necessary
            data_dict = data.to_dict() if hasattr(data, 'to_dict') else data
             # Extract the base name of the file and create a JSON file name
            base_name = os.path.splitext(file_obj)[0]
            json_file_name = f"{base_name}.json"
            # Save the data in JSON format
            with open(json_file_name, "w") as json_file:
                json.dump(data_dict, json_file, indent=4)
                logger.info(f"Extraction succeeded for segement {json_file_name}")
      
    return None


