from langchain_text_splitters import RecursiveCharacterTextSplitter

import fitz  # PyMuPDF

def read_pdf(file_path):
    # Open the PDF file
    pdf_document = fitz.open(file_path)
    
    # Initialize an empty string to store the text
    pdf_text = ""
    
    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)  # Load the page
        pdf_text += page.get_text()  # Extract text from the page

    return pdf_text


def chunk_docs(doc_file_path, chunk_size=512):
    text_piece=read_pdf(doc_file_path)
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=int(chunk_size),
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
    )
    chunk_list=text_splitter.split_text(text_piece) # this will output a list of text pieces

    return chunk_list

