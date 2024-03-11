import streamlit as st
import itertools

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


def updateGenres():
    st.session_state.genres.append(genre_selection)
    # st.session_state.genres = list(itertools.chain.from_iterable(st.session_state.genres))
    st.session_state.genres = list(itertools.chain.from_iterable(itertools.repeat(x,1) if isinstance(x,str) else x for x in st.session_state.genres))
    st.session_state.genres = list(set(st.session_state.genres))
    container3.write('You like: ' + str(st.session_state.genres))

genre_selection = container3.multiselect(label="Select a genre", options=genre_options)# , on_change=addFavoriteGenre)
container3.button('Update Favorite Genres', on_click=updateGenres)
st.write(genre_selection)
# st.write(st.session_state.genres)