import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


st.set_page_config(page_title="Your stylist", page_icon="👗", layout="wide")
st.title("Your stylist")

#Get response from LLM

def get_response(query,chat_history):
    template = """
    You are a stylist and your goal is to help people look their best. You are a fashion expert and you have a great sense of style. You are always up to date with the latest fashion trends and you know how to make people look good. You are a great listener and you are always ready to help people look their best. You are a fashion expert and you have a great sense of style. 
    Your goal is to answer the question of the user with the history of the conversation.

    chat_history: {chat_history}
    user_question: {user_question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI()
    chain =  prompt | llm | StrOutputParser()
    return chain.invoke({
        "chat_history" : chat_history,
        "user_question" : query
    })


#Conversation
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("Stylist"):
            st.markdown(message.content)

#User input
user_query= st.chat_input("Ask me anything")

if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message('Stylist'):
        ai_response = get_response(user_query, st.session_state.chat_history)
        st.markdown(ai_response)    

    st.session_state.chat_history.append(AIMessage(ai_response))


        