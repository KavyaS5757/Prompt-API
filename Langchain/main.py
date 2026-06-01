## Integrate our code Groq API
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Get Groq API key from environment
groq_api_key = os.getenv("GROQ_API_KEY")

# streamlit framework

st.title('Langchain Demo With Groq API')
input_text=st.text_input("Search the topic u want")

## Groq LLM
llm=ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.8,
    api_key=groq_api_key
)



if input_text:
    st.write(llm.invoke(input_text).content)