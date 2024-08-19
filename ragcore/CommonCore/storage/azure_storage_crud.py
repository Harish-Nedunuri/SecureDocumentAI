from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import uuid
from urllib.parse import urlparse,unquote
import os
import fitz  # PyMuPDF
from ragcore.CommonCore.secret_utils.config import get_settings
from ragcore.CommonCore.audit.logging import logger
from datetime import datetime



def get_blob_service_client():
    """
    Get a reference to the BlobServiceClient.

    :return: BlobServiceClient object
    """
    settings = get_settings()
    # Replace these with your Azure Storage account details
    STORAGE_ACCOUNT_NAME = settings.STORAGE_ACCOUNT_NAME
    STORAGE_ACCOUNT_KEY = settings.STORAGE_ACCOUNT_KEY
    # Create the connection string
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={STORAGE_ACCOUNT_NAME};AccountKey={STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"

    # Initialize the BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    return blob_service_client

def upload_file_to_az_storage(file_path, blob_name,container):
    """
    Upload a file to the specified container and blob.
    
    :param file_path: Path of the file to be uploaded
    :param blob_name: Name of the blob to be stored in the container
    """
    blob_service_client = get_blob_service_client()
    try:
        # Get a reference to the container
        container_client = blob_service_client.get_container_client(container)
        
        # Get a reference to the blob
        blob_client = container_client.get_blob_client(blob_name)
       
        # Upload the file
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        return blob_client.url
    except Exception as ex:
        logger.info(f"An error occurred: {ex}")


def download_file_from_az_storage(blob_url, download_folder):
    try:
        os.makedirs(download_folder, exist_ok=True)
        # Parse the blob URL to get the container name and blob name
        parsed_url = urlparse(blob_url)
        blob_path = parsed_url.path.lstrip('/')  # Remove leading slash
        container_name, blob_name = blob_path.split('/', 1)
        # Decode percent-encoded characters in the blob name
        blob_name = unquote(blob_name)
        blob_name_local = blob_name.split("\\")[-1]

        # Get the BlobServiceClient
        blob_service_client = get_blob_service_client()
        
        # Create a BlobClient
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
        # Set the local path where the file will be saved
        local_file_path = os.path.join(download_folder, os.path.basename(blob_name_local))
        
        # Download the blob to a local file
        with open(local_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
        
        logger.info(f"File downloaded to {local_file_path}")
        
    except Exception as e:
        logger.info(f"An error occurred: {e}")
        local_file_path = None
    return local_file_path    

def get_num_of_pages(blob_client):
    """
    Get the number of pages in a PDF document.
    
    :param blob_client: BlobClient object
    :return: Number of pages
    """
    try:
        # Download the blob content as a byte stream
        pdf_bytes = blob_client.download_blob().readall()
        
        if not pdf_bytes:
            raise ValueError("Downloaded PDF byte stream is empty.")
        
        # Open the PDF from the byte stream
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        # Get the number of pages
        num_of_pages = pdf_document.page_count
        
        return num_of_pages
    
   
    except ValueError as ve:
        print(f"An error occurred: {ve}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
    
    return 0

def list_blobs_recursive(container_client, prefix):
    """
    List all blobs in a container recursively.
    
    :param container_client: ContainerClient object
    :param prefix: Prefix to search blobs within
    :return: Generator of BlobProperties
    """
    blob_list = container_client.list_blobs(name_starts_with=prefix)
    for blob in blob_list:
        yield blob
        if blob.name.endswith('/'):
            yield from list_blobs_recursive(container_client, blob.name)

def get_folder_content_details(folder_path, container):

    """
    Get details of all PDF blobs in the specified folder and its subdirectories within the container.
    
    :param folder_path: Path of the folder in the container
    :param container: Name of the container
    :return: List of dictionaries containing document details
    """
    blob_service_client = get_blob_service_client()
    try:
        # Get a reference to the container
        container_client = blob_service_client.get_container_client(container)
        
        # List blobs in the specified folder and its subdirectories
        folder_contents = []
        for blob in list_blobs_recursive(container_client, folder_path):
            # Only process PDF files
            if blob.name.lower().endswith('.pdf'):
                blob_client = container_client.get_blob_client(blob)
                blob_properties = blob_client.get_blob_properties()
                
                num_of_pages = get_num_of_pages(blob_client)
                
                if num_of_pages == 0:
                    print(f"Skipping blob {blob.name} due to error in retrieving page count.")
                    continue
                
                document_details = {
                    "document_id": str(uuid.uuid4()),
                    "num_of_pages": num_of_pages,
                    "file_size": blob_properties.size,
                    "file_name": os.path.basename(blob.name),
                    "document_path_uri": blob_client.url,
                    "content_type": blob_properties.content_settings.content_type,
                    "creation_time": blob_properties.creation_time,
                    "last_modified": blob_properties.last_modified,
                    "register_time": datetime.now()            
                }
                folder_contents.append(document_details)
        
        return folder_contents
    except Exception as e:
        logger.info(f"An error occurred: {e}")
        return []
    
def extract_directory_path(doc_uri):
    # Parse the URL
    parsed_url = urlparse(doc_uri)  
    # Extract the path and remove the leading '/'
    path = parsed_url.path.lstrip('/')
    decoded_path = unquote(path)
    path_parts = decoded_path.split('/')[1:]            
    # Split the path to remove the file name and retain the directory structure
    directory_path = '/'.join(path_parts[:-1])
    return directory_path 

def get_blob_uri(filename, container):
    blob_service_client = get_blob_service_client()
    try:
        # Get a reference to the container
        container_client = blob_service_client.get_container_client(container)

        # Get a reference to the blob
        blob_client = container_client.get_blob_client(filename)

        # Get the blob URL
        blob_url = blob_client.url

        return blob_url
    except Exception as e:
        logger.info(f"An error occurred: {e}")
        return None