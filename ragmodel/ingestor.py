import os
import fitz
import regex as re 
from langchain.docstore.document import Document
"""Used for getting the list of texts in a pdf in the form of Document object

path -> name of directory containing the pdfs (default : docs)"""
def refine_docs(doc):
    doc = re.sub(r"\n","",doc)
    doc = re.sub(r".\"?!,@#%^&*()","",doc)
    return doc

def getDocument(path):
    doc_list = []
    # Ensure the provided path exists
    if not os.path.exists(path):
        print(f"The specified path '{path}' does not exist.")
        return

    # Iterate through all files in the specified path
    for file_name in os.listdir(path):
        print("Ingesting " + file_name + "...")
        file_path = os.path.join(path, file_name)

        # Check if the current item in the path is a file
        if os.path.isfile(file_path):
            doc = fitz.open(file_path)
            for i in doc:
                doc_list.append(Document(page_content = refine_docs(i.get_text())))
    return doc_list

            