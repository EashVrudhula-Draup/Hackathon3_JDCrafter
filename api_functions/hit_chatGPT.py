import os
import sys
import constants
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
os.environ["OPENAI_API_KEY"] = constants.api_key

def hit_chatGPT(query, textfile):
    loader = TextLoader(textfile)
    index = VectorstoreIndexCreator().from_loaders([loader])
    return index.query(query,llm=ChatOpenAI(temperature=0))