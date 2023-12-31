import nltk
import urllib
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
nltk.download('stopwords')
import streamlit as st
import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
import requests


def scrap(link):
  link = 'https://ellakkiaa.github.io/kct/'
  source = requests.get(link)
  soup = BeautifulSoup(source.text,'html.parser')

  text = ""
  with open('data.txt', "w", encoding="utf-8") as file:
    for para in soup.find_all('p'):
      paragraph = para.getText()
      file.write(paragraph +'\n')
  print("File Saved!")

from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub

from langchain.document_loaders import TextLoader
loader = TextLoader('/content/notes.txt')
document = loader.load()

from langchain.document_loaders.onedrive_file import CHUNK_SIZE
from langchain.text_splitter import CharacterTextSplitter
text_splitter = CharacterTextSplitter(chunk_size=5,chunk_overlap=0)
docs  = text_splitter.split_documents(document)

from langchain.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings()


from langchain.vectorstores import FAISS
db = FAISS.from_documents(docs,embeddings)
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub

def qbot(query):
  llm = HuggingFaceHub(repo_id="google/flan-t5-base",model_kwargs={"temperature":0.5,"max_length":100})
  chain = load_qa_chain(llm,chain_type="stuff")

  docs = db.similarity_search(query)
  a = chain.run(input_documents = docs,question = query)
  return a

def main():
    st.title('CustomBot - Tailored Conversation')

    query = st.text_input("Enter a query")
    show_output = False

    if query:
        show_output = True
        z = qbot(query)

    if show_output:
        st.write(z)



if __name__ == '__main__':
  main()
