from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from embeddings import get_embeddings
import tempfile, os

def create_vectorstore(uploaded_files):
    docs = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    for file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name
        loader = PyPDFLoader(tmp_path)
        pages = loader.load()
        docs.extend(splitter.split_documents(pages))
        os.unlink(tmp_path)

    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore

def get_relevant_context(vectorstore, query, k=3):
    if vectorstore is None:
        return ""
    results = vectorstore.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in results])