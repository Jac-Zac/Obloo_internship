# PyPDF2!/usr/bin/env python

import os
import warnings

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (DirectoryLoader, PyPDFLoader,
                                                  UnstructuredExcelLoader)
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Look into caching
# https://python.langchain.com/docs/modules/data_connection/text_embedding/caching_embeddings

warnings.simplefilter("ignore")

# Database directory
ABS_PATH: str = os.path.dirname(os.path.abspath(__file__))
DB_DIR: str = os.path.join(ABS_PATH, "db")

# Data directory
DATA_DIR: str = os.path.join(ABS_PATH, "data")


# Create vector database
def create_vector_database():
    """
    Creates a vector database using document loaders and embeddings.

    This function loads data from PDF, markdown and text files in the 'data/' directory,
    splits the loaded documents into chunks, transforms them into embeddings using OllamaEmbeddings,
    and finally persists the embeddings into a Chroma vector database.

    """

    # Initialize loaders for different file types
    pdf_loader = DirectoryLoader(DATA_DIR, glob="**/*.pdf", loader_cls=PyPDFLoader)
    excel_loader = DirectoryLoader(
        DATA_DIR, glob="**/*.xlsx", loader_cls=UnstructuredExcelLoader
    )

    loaded_documents = pdf_loader.load()
    loaded_documents += excel_loader.load()

    # Split loaded documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=100)
    chunked_documents = text_splitter.split_documents(loaded_documents)

    # Initialize Ollama Embeddings
    ollama_embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # Create and persist a Chroma vector database from the chunked documents
    vector_database = Chroma.from_documents(
        documents=chunked_documents,
        embedding=ollama_embeddings,
        persist_directory=DB_DIR,
    )

    vector_database.persist()


def create_vector_database():
    """
    Creates a vector database using document loaders and embeddings.

    This function loads data from PDF, markdown and text files in the 'data/' directory,
    splits the loaded documents into chunks, transforms them into embeddings using OllamaEmbeddings,
    and finally persists the embeddings into a Chroma vector database.

    """

    # Check if the vector database already exists
    if os.path.exists(DB_DIR):
        # Update only the necessary files
        pass
    else:
        # Initialize loaders for different file types
        pdf_loader = DirectoryLoader(DATA_DIR, glob="**/*.pdf", loader_cls=PyPDFLoader)
        excel_loader = DirectoryLoader(
            DATA_DIR, glob="**/*.xlsx", loader_cls=UnstructuredExcelLoader
        )

        loaded_documents = pdf_loader.load()
        loaded_documents += excel_loader.load()

        # Split loaded documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200, chunk_overlap=100
        )
        chunked_documents = text_splitter.split_documents(loaded_documents)

        # Initialize Ollama Embeddings
        ollama_embeddings = OllamaEmbeddings(model="nomic-embed-text")

        # Create and persist a Chroma vector database from the chunked documents
        vector_database = Chroma.from_documents(
            documents=chunked_documents,
            embedding=ollama_embeddings,
            persist_directory=DB_DIR,
        )

        vector_database.persist()


if __name__ == "__main__":
    create_vector_database()
