from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

llm=Ollama(model="llama3",temperature=0.6)

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

        