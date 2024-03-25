from io import BytesIO
from typing import List

import chainlit as cl
import PyPDF2
from langchain.chains import ConversationalRetrievalChain
from langchain.docstore.document import Document
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma

# Small splitting for documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)


@cl.on_chat_start
async def on_chat_start():
    files = None

    # Wait for the user to upload a file
    while files is None:
        files = await cl.AskFileMessage(
            content="Please upload a pdf file to begin!",
            accept=["application/pdf"],
            max_size_mb=100,
            timeout=180,
        ).send()

    file = files[0]
    print(file)

    msg = cl.Message(content=f"Processing `{file.name}`...")
    await msg.send()

    # Read the PDF file

    # pdf_stream = BytesIO(content)
    pdf = PyPDF2.PdfReader(file.path)
    pdf_text = ""
    for page in pdf.pages:
        pdf_text += page.extract_text()

    # Split the text into chunks
    texts = text_splitter.split_text(pdf_text)

    # Create a metadata for each chunk
    metadatas = [{"source": f"{i}-pl"} for i in range(len(texts))]

    # Create a Chroma vector store
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    docsearch = await cl.make_async(Chroma.from_texts)(
        texts, embeddings, metadatas=metadatas
    )

    message_history = ChatMessageHistory()

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        chat_memory=message_history,
        return_messages=True,
    )

    # Create a chain that uses the Chroma vector store
    chain = ConversationalRetrievalChain.from_llm(
        ChatOllama(model="mistral"),
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        memory=memory,
        return_source_documents=True,
    )

    # Let the user know that the system is ready
    msg.content = f"Processing `{file.name}` done. You can now ask questions!"
    await msg.update()

    cl.user_session.set("chain", chain)


@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain")

    cb = cl.AsyncLangchainCallbackHandler(stream_final_answer=True)
    cb.answer_reached = True

    res = await chain.acall(message.content, callbacks=[cb])  # deprecated

    # print(f"response: {res}")
    answer = res["answer"]
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
        context = ", ".join(source_names)

        # if source_names:
        #     answer += f"\nSources: {', '.join(source_names)}"
        # else:
        #     answer += "\nNo sources found"

    await cl.Message(content=context, elements=text_elements).send()
