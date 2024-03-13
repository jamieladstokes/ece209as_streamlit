import streamlit as st
import itertools

# initializing the session_state vars 
if 'name' not in st.session_state: 
    st.session_state.name = 'Bob'

if 'age' not in st.session_state: 
    st.session_state.age = '34'
    
if 'genres' not in st.session_state: 
    st.session_state.genres = []

if 'pastbooks' not in st.session_state:
    st.session_state.pastbooks = []

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
                'Mystery', 'Romance', 'Science Fiction', 'Thriller', 'Travel', 'Young Adult']

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
    st.session_state.pastbooks = [book.strip() for book in past_books.split(',')]
    container4.write('Past Books Read: ' + ', '.join(st.session_state.pastbooks))
container4.button('Add Past Books Read', on_click=addPastBooks)

container5 = st.container(border=True)
goal_options = ["Hard to Read", 'Just my Level', 'Easy to Read']

def updateGoals():
    st.session_state.goals = goal_selection
    container5.write(st.session_state.goal)

goal_selection = container4.multiselect(label="Select a Reading Goals", options=goal_options)# , on_change=addFavoriteGenre)
container5.button('Update Reading Goals', on_click=updateGoals)
st.write(goal_selection)