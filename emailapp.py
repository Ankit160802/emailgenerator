import streamlit as st

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
import json
import torch
from langchain.llms import HuggingFacePipeline
from transformers import (AutoTokenizer,
                          AutoModelForCausalLM,
                          BitsAndBytesConfig,
                          pipeline)



HF_TOKEN="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"

# Quantisation
# bnb_config=BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_use_double_quant=True,
#     bnb_4bit_quant_type="nf4",
#     bnb_4bit_compute_dtype=torch.bfloat16
# )


model_name="meta-llama/Llama-2-7b-chat-hf"

tokenizer=AutoTokenizer.from_pretrained(model_name,token=HF_TOKEN)
tokenizer.pad_token=tokenizer.eos_token



model=AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    load_in_4bit=True,
    # quantization_config=bnb_config,
    token=HF_TOKEN
)

# PIPELINE
text_generator=pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=128
)



llm=HuggingFacePipeline(pipeline=text_generator)


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
subject=st.text_input("enter subject")



if subject:
    response=langchainforEmail.generate_email(subject)
    st.header(response['email_subject'])
    st.write(response['email_body'])


     
