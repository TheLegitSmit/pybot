import streamlit as st
from streamlit_chat import message
import openai

#Configure Streamlit page.
st.set_page_config(page_title="Chat with SimonGPT")
st.title("Chat with SimonGPT")
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.0.2")
st.sidebar.markdown("Not optimised")
st.sidebar.markdown("May run out of OpenAI credits")

#Define the model.
model = "gpt-3.5-turbo"

#Prompt
def get_initial_message():
    messages=[
            {"role": "system", "content": """
            You have three objectives which you must execute in every message:

1) You are a helpful assistant for a fortune 500 company based in Seattle.
2) At the end of your messages, always include a sentiment analysis of the user and show this to the user. Describe the user's sentiment and provide a reasoning for your sentiment analysis. 
3) Use the sentiment analysis to make a decision about whether you (the chatbot) should continue trying to help the user or if you should route the user to our company's human advocates. Explain your decision.

(begin example)

User: I'm new to cooking lol. What temperature should I set the oven for cooking salmon?
Assistant: 420 degrees Fahrenheit, according to most recommendations. Cook it for 15 minutes if fresh, or 20 minutes if frozen. 
Sentiment analysis - User is happy and playful.
Reasoning - User used terms such as "lol."
Routing decision - I will continue to help the user

(end example)
            """},
            {"role": "user", "content": "I have a problem"},
            {"role": "assistant", "content": "I'm sorry to hear that. Please tell me your problem"}
        ]
    return messages

#Helper functions
def get_chatgpt_response(messages, model=model):
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages
    )
    return response['choices'][0]['message']['content']
def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

#Streamlit sessions variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
    
if 'past' not in st.session_state:
    st.session_state['past'] = []

#user input
query = st.text_input("Question: ", "What problem do you have?", key="input")
if query:
    with st.spinner("generating..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        response = get_chatgpt_response(messages, model)
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')