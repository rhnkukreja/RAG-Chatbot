import utils.indexing_chunks as indexing_chunks
from pinecone import Pinecone
import openai
from utils.config import *

openai.api_key = OPENAI_API_KEY

def get_the_context(query, doc_name):
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index("basic-rag-chatbot") # index name

    query_vector=indexing_chunks.get_text_embedding(query)

    results=index.query(
    namespace=doc_name,
    vector=query_vector,
    top_k=2,
    include_values=True,
    include_metadata=True,
    )

    # Extract the metadata for the top 2 items
    top_metadata = [result['metadata'] for result in results['matches']]

    return top_metadata



