import openai
from pinecone import Pinecone
from utils.config import *

openai.api_key = OPENAI_API_KEY

def get_text_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    embedding = response["data"][0]["embedding"]
    return embedding


def index_text_chunks(chunk_list, doc_name):    
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index("basic-rag-chatbot") # index name, you can add your index, through the pinecone website

    chunk_text_n_vectors_list=[]
    for i, chunk_text in enumerate(chunk_list):
        text_vector_dict={}
        chunk_vector=get_text_embedding(chunk_text)
        text_vector_dict["id"]=str(i)
        text_vector_dict["metadata"]={"text":chunk_text}
        text_vector_dict["values"]=chunk_vector
        chunk_text_n_vectors_list.append(text_vector_dict)
    
    # Upsert vectors and metadata to the index
    index.upsert(vectors=chunk_text_n_vectors_list, namespace=doc_name)
    return f"Document has been uploaded successfully under the name {doc_name}"


