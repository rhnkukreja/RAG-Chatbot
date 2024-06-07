from utils import (chunking_docs,
                   indexing_chunks,
                   retrieve_chunks,
                   generate_answer
                   )
import os
import streamlit as st

def upload_doc(doc_file_path):
    doc_name = os.path.basename(doc_file_path)
    chunk_list=chunking_docs.chunk_docs(doc_file_path)
    answer_message=indexing_chunks.index_text_chunks(chunk_list, doc_name)
    return answer_message



def query_doc(query, doc_name):
    context=retrieve_chunks.get_the_context(query, doc_name)
    answer_to_query=generate_answer.get_answer_from_llm(query, context)    
    return answer_to_query


st.title("RAG Chatbot for Beginners")


uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    temp_dir = "tempDir"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    # Save the uploaded file to a temporary location
    doc_file_path = os.path.join("tempDir", uploaded_file.name)
    with open(doc_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File {uploaded_file.name} uploaded successfully")

    # Process the uploaded document
    answer_message = upload_doc(doc_file_path)
    st.write(answer_message)

    # Dropdown to select the document name (assuming we can have multiple documents)
    doc_name = st.selectbox("Select Document", [uploaded_file.name])

    # Input box for the query
    query = st.text_input("Enter your question")

    if st.button("Get Answer"):
        if query:
            answer_to_query = query_doc(query, doc_name)
            st.write(answer_to_query)
        else:
            st.error("Please enter a question")

