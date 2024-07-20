import streamlit as st

from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
import json
import torch
from langchain.llms import GooglePalm

api_key = st.secrets["api_key"] 
from langchain_google_genai import GoogleGenerativeAI

llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key, temperature=0.1)

def generate_email(subject1):

    email_subject_prompt=PromptTemplate(
        input_variables=['subject'],
        template=""" give only one subject for email for {subject} in simple words """
    )

    subject=LLMChain(llm=llm,prompt=email_subject_prompt,output_key="email_subject")

    # email body chain

    email_body_prompt=PromptTemplate(
        input_variables=['email_subject'],
        template=""" write only one email for given subject {email_subject}."""
    )
    body=LLMChain(llm=llm,prompt=email_body_prompt,output_key="email_body")

    # chain finalizing

    email_chain=SequentialChain(
        chains=[subject,body],
        input_variables=['subject'],
        output_variables=['email_subject','email_body']
    )

    response=email_chain.invoke(subject1)

    return response

st.title("email generator")

# subject=st.sidebar.selectbox("pick your task",("request item for 20 piece cheffing dish","declining_request"))
subject1=st.text_input("enter subject")



if subject1:
    response=generate_email(subject1)
    st.header(response['email_subject'])
    st.write(response['email_body'])


     
