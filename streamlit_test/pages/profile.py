import streamlit as st
import itertools
import streamlit as st
#from streamlit.components.v1 import container as st_container
from openai import OpenAI


colors = {
    "tan": "#FFEFD5",
    "grey": "#808080",
}

st.markdown(f"""
    <style>
        body {{
            background-color: {colors['tan']};
            color: {colors['tan']};
        }}
        .sidebar .sidebar-content {{
            background-color: {colors['tan']};
        }}
        .stButton > button {{
            background-color: {colors['grey']};
            color: {colors['tan']};
            border-color: {colors['grey']};
        }}
        .stTextInput > div > div > input[type="text"] {{
            background-color: {colors['tan']};
            color: {colors['tan']};
        }}
        .stTextInput > div > div > input[type="text"]:focus {{
            border-color: {colors['tan']};
            box-shadow: 0 0 0 0.2rem {colors['tan']};
        }}
        .css-1vllfu2 {{
            color: {colors['tan']};
        }}
    </style>
""", unsafe_allow_html=True)
# initializing the session_state vars 
if 'name' not in st.session_state:
    st.session_state.name = 'Bob'

if 'age' not in st.session_state:
    st.session_state.age = '34'

if 'genres' not in st.session_state:
    st.session_state.genres = []

if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []

if 'liked_recommendation' not in st.session_state:
    st.session_state.liked_recommendation = None
    st.session_state.feedback_text = ""

if 'pastbooks' not in st.session_state:
    st.session_state.pastbooks = []

if 'goal' not in st.session_state:
    st.session_state.goal = 'Just my Level'
st.title("Bookify!")



# Name
container1 = st.container(border=True)
name = container1.text_input(label='Your Name', placeholder="What's your name?")
def changeName():
    st.session_state.name = name
    container1.write('Hi ' + st.session_state.name + '!')
container1.button('Change Name', on_click=changeName)

# Age
container2 = st.container(border=True)
age = container2.text_input(label='Your Age', placeholder="What's your age?")
def changeAge():
    st.session_state.age = age
    container2.write(st.session_state.age + ' years young!')
container2.button('Change Age', on_click=changeAge)

# Favorite Genres
container3 = st.container(border=True)
genre_options = ["Children's", 'Christian', 'Classics', 'Comics', 'Fantasy', 'Historical Fiction', 'Horror', 'Humor and Comedy',
                'Mystery', 'Romance', 'Science Fiction', 'Thriller', 'Travel', 'Young Adult', 'Philosophy']

# Update favorite genres list 
def updateGenres():
    st.session_state.genres.append(genre_selection)
    st.session_state.genres = list(itertools.chain.from_iterable(itertools.repeat(x,1) if isinstance(x,str) else x for x in st.session_state.genres))
    st.session_state.genres = list(set(st.session_state.genres))
    container3.write('You like: ' + str(st.session_state.genres))

genre_selection = container3.multiselect(label="Select a genre", options=genre_options)
container3.button('Update Favorite Genres', on_click=updateGenres)

# Add past books read
container4 = st.container(border=True)
past_books = container4.text_area(label='Past Books Read (comma-separated):', value=', '.join(st.session_state.pastbooks))
def addPastBooks():
    new_books = [book.strip() for book in past_books.split(',')]
    st.session_state.pastbooks.extend(new_books)
    st.session_state.pastbooks = list(set(st.session_state.pastbooks))
    container4.write('Past Books Read: ' + ', '.join(st.session_state.pastbooks))
container4.button('Add Past Books Read', on_click=addPastBooks)

container5 = st.container(border=True)
goal_options = ["Hard to Read", 'Just my Level', 'Easy to Read']

def updateGoals():
    st.session_state.goal = goal_selection
    container5.write(st.session_state.goal)

goal_selection = container5.selectbox(label="Select a Reading Goals", options=goal_options)# , on_change=addFavoriteGenre)
container5.button('Update Reading Goals', on_click=updateGoals)