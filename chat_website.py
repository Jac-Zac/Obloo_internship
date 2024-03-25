# import required dependencies
# https://docs.chainlit.io/integrations/langchain
import os

import chainlit as cl
from langchain import hub
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma

# Look into function calling
# https://python.langchain.com/docs/modules/model_io/chat/function_calling

ABS_PATH: str = os.path.dirname(os.path.abspath(__file__))
DB_DIR: str = os.path.join(ABS_PATH, "db_website")


def load_model():
    llm = Ollama(
        model="mistral",
        verbose=True,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )
    return llm


def web_retrival(url):
    # Load data from the specified URL
    loader = WebBaseLoader(url)
    data = loader.load()

    # Split the loaded data
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=40
    )

    docs = text_splitter.split_documents(data)

    # Create Ollama embeddings
    ollama_embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # Create a Chroma vector database from the documents
    vectordb = Chroma.from_documents(
        documents=docs, embedding=ollama_embeddings, persist_directory=DB_DIR
    )

    vectordb.persist()

    # Create a retriever from the Chroma vector database
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    return retriever


def retrieval_qa_chain(llm, retriever):
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
    )
    return qa_chain


def qa_bot():
    llm = load_model()
    # Pass the site
    retriever = web_retrival("https://en.wikipedia.org/wiki/Rubik's_Cube")

    qa = retrieval_qa_chain(llm, retriever)
    return qa


@cl.on_chat_start
async def start():
    """
    Initializes the bot when a new chat starts.

    This asynchronous function creates a new instance of the retrieval QA bot,
    sends a welcome message, and stores the bot instance in the user's session.
    """
    chain = qa_bot()
    welcome_message = cl.Message(content="Starting the bot...")
    await welcome_message.send()
    welcome_message.content = "Ask a question to a website"
    await welcome_message.update()
    cl.user_session.set("chain", chain)


@cl.on_message
async def main(message):
    """
    Processes incoming chat messages.

    This asynchronous function retrieves the QA bot instance from the user's session,
    sets up a callback handler for the bot's response, and executes the bot's
    call method with the given message and callback. The bot's answer and source
    documents are then extracted from the response.
    """
    chain = cl.user_session.get("chain")

    cb = cl.AsyncLangchainCallbackHandler(stream_final_answer=True)
    cb.answer_reached = True

    res = await chain.acall(message.content, callbacks=[cb])  # deprecated

    # print(f"response: {res}")
    answer = res["result"]
    # answer = answer.replace(".", ".\n")
    source_documents = res["source_documents"]

    text_elements = []  # type: List[cl.Text]

    if source_documents:
        for source_idx, source_doc in enumerate(source_documents):
            source_name = f"source_{source_idx}"
            # Create the text element referenced in the message
            text_elements.append(
                cl.Text(content=source_doc.page_content, name=source_name)
            )
        source_names = [text_el.name for text_el in text_elements]

        if source_names:
            answer += f"\nSources: {', '.join(source_names)}"
        else:
            answer += "\nNo sources found"

    # await cl.Message(content=answer, elements=text_elements).send()
