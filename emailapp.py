import streamlit as st
import langchainforEmail

st.title("email generator")

# subject=st.sidebar.selectbox("pick your task",("request item for 20 piece cheffing dish","declining_request"))
subject=st.text_input("enter subject")



if subject:
    response=langchainforEmail.generate_email(subject)
    st.header(response['email_subject'])
    st.write(response['email_body'])


     
