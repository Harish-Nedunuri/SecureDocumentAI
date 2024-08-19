# Secure RAG - README

## Overview

Secure RAG is a Python package designed for implementing a secure Retrieval-Augmented Generation (RAG) system using Large Language Models (LLMs). The system is built on top of FastAPI and integrates Azure Document Intelligence OCR models for document processing. The application ensures secure access through OAuth2 authentication, making it suitable for sensitive use cases that require both document understanding and secure user authentication.

## Features

- **LLM Integration:** Utilizes advanced Large Language Models to enhance retrieval and generation tasks.
- **Azure Document Intelligence:** Leverages Azure's Document Intelligence OCR models for accurate document processing and extraction.
- **Secure API Access:** Implements OAuth2 authentication to ensure that only authorized users can access the application.
- **FastAPI Application:** The core of the application is built using FastAPI, known for its high performance and ease of use.

## Installation

To install Secure RAG, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/your-username/secure-rag.git
cd secure-rag
pip install -r requirements.txt
```

## Usage

### Running the Application

To start the FastAPI application, execute the `main.py` file:

```bash
uvicorn main:app --reload
```

This will launch the server, and the API will be available at `http://127.0.0.1:8000`.

### OAuth2 Authentication

Secure RAG uses OAuth2 for securing API endpoints. Users must obtain an access token by authenticating via the OAuth2 provider configured in the application. The access token must be included in the `Authorization` header of each API request.

```bash
Authorization: Bearer <access_token>
```

### API Endpoints

- **/docs:** Access the automatically generated API documentation.
- **/rag:** Main RAG endpoint that processes the input using the LLM and returns the generated output.
- **/ocr:** Endpoint for document processing using Azure Document Intelligence OCR models.

## Configuration

The application configuration, including OAuth2 credentials and Azure API keys, is managed through environment variables. You can set these in a `.env` file in the root of the project:

```env
OAUTH2_CLIENT_ID=your-client-id
OAUTH2_CLIENT_SECRET=your-client-secret
OAUTH2_TOKEN_URL=https://provider.com/oauth2/token
AZURE_OCR_KEY=your-azure-ocr-key
AZURE_OCR_ENDPOINT=https://your-azure-endpoint.com
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Be sure to include tests for any new features or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or support, please contact the project maintainer at [your-email@example.com](mailto:your-email@example.com).
