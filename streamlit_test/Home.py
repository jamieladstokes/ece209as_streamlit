import streamlit as st
from openai import OpenAI

OPENAI_API_KEY = "YOUR API KEY"
client = OpenAI(api_key=OPENAI_API_KEY)


# initializing the session_state vars 
if 'name' not in st.session_state: 
    st.session_state.name = 'Bob'

if 'age' not in st.session_state: 
    st.session_state.age = '34'
    
if 'genres' not in st.session_state: 
    st.session_state.genres = []

if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []
    

st.title("Bookify!")


# Updated Profile Info 
container1_home = st.container(border=True)

def refreshInfo():
    container1_home.write(st.session_state.name)
    container1_home.write(st.session_state.age)
    container1_home.write('Favorite Genres: ')
    container1_home.write(st.session_state.genres)

container1_home.button('Refresh User Info', on_click=refreshInfo)


# Get Book Recommendation Titles 
container2_home = st.container(border=True)
container2_home.header('Book Recommendations')

def getRecommendations():
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    
    rec_prompt = f"""You are a helpful assistant that recommends books to read based on lists. 
                   Your user client likes the following genres: {st.session_state.genres}. 
                   Recommend 3 books for them. Output only the book titles (e.g. 'Dune, Star Wars, Harry Potter')."""
    
    response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages= [{"role": 'assistant', "content": rec_prompt}]
            )
    
    st.session_state.recommendations = response.choices[0].message.content
    container2_home.write(st.session_state.recommendations)

container2_home.button('Get Recommendations', on_click=getRecommendations)


# Get Summaries of Recommendations 
container3_home = st.container(border=True)

def getSummaries():
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    summary_prompt = f"""You are a helpful assistant that provides summaries of books from a list. 
                Provide summaries for the following books, without major spoilers: {st.session_state.recommendations}. 
                Do not make up details or hallucinate.
                After each summary, provide a difficulty rating for each book."""
    
    response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages= [{"role": 'assistant', "content": summary_prompt}]
            )
    
    container3_home.write(response.choices[0].message.content)

container3_home.button('Get Summaries', on_click=getSummaries)

    
