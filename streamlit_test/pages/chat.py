import streamlit as st
from openai import OpenAI

OPENAI_API_KEY = 'YOUR API KEY'
st.title("BookTalk")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=OPENAI_API_KEY)

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

col1, col2, col3 = st.columns(3)

def reset_conversation():
    st.session_state.messages=[]

with col2:
    st.button('Reset Chat', on_click=reset_conversation)
with col3: 
    st.button('Button2')

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

# if st.button("Refresh"):
#     st.session_state.messages = []
