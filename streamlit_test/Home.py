import streamlit as st
from openai import OpenAI
import re
import streamlit as st
#from streamlit.components.v1 import container as st_container
from openai import OpenAI
import base64

colors = {
    "tan": "#FFEFD5",
    "grey": "#808080",
}

side_bg = "sample.jpg"
side_bg_ext = "jpg"
st.markdown(f"""
    <style>
        body {{
            background-color: {colors['grey']};
            color: {colors['grey']};
        }}
        .sidebar .sidebar-content {{
                background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()})
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
OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)

# initializing the session_state vars
if 'name' not in st.session_state:
    st.session_state.name = 'Readey McReadFace'

if 'age' not in st.session_state:
    st.session_state.age = '25'

if 'genres' not in st.session_state:
    st.session_state.genres = []

if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []

if 'liked_recommendation' not in st.session_state:
    st.session_state.liked_recommendation = None
    st.session_state.feedback_text = ""

if 'pastbooks' not in st.session_state:
    st.session_state.pastbooks = []

if 'dislikes' not in st.session_state:
    st.session_state.dislikes = []
if 'goal' not in st.session_state:
    st.session_state.goal = 'Just my Level'

st.write("""
    # Bookify! - Your Reading Assistant

    Welcome to Bookify! Let us find the perfect books for you!

    Please fill out your profile with your age, past books read, favorite genres, and reading goals!
""")

# Updated Profile Info
container1_home = st.container(border=True)


def refreshInfo():
    container1_home.write('Your name: ' + st.session_state.name)
    container1_home.write('Your age: ' + st.session_state.age)
    container1_home.write('Favorite Genres: ' + str(st.session_state.genres))
    container1_home.write('Your current goal: ' + str(st.session_state.goal))
    container1_home.write('Books you have previously read: ' + str(st.session_state.pastbooks))

container1_home.button('Refresh User Info', on_click=refreshInfo)

# Get Book Recommendation Titles
container2_home = st.container(border=True)
container2_home.header('Book Recommendations')

# Container for feedback input
feedback_container = st.empty()

def getRecommendations():
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    # question = "hi"
    question = f"I like to read a lot and am interested in books that are \n{st.session_state.goal}. Sometimes I have a hard time figuring out the next book I should be reading, but have an idea for the genres I'm interested in. Since I generally have liked books I've read in the past, I'd like to use those books as a model for the books I should read next. Please use my \n{st.session_state.pastbooks} list and recommend 3 books from the following genres: {st.session_state.genres}. If you don't have any recommendations, please say 'I don't know'. Don't make recommendations from those I've read in the past."

    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": "system", "content": "You are a helpful assistant that recommends 3 books to read based on how challenging the books are"},
            {"role": "user", "content": "Please look at all of the books that I have previously read here: \n{st.session_state.pastbooks}"},
            {"role": "assistant", "content": "I see all of the books that you have read here: \n{st.session_state.pastbooks} and will use them to base my recommendation off of when you ask. Please do not recommend any books you have recommended in the past"},
            {"role": "user", "content": "Now, please look at my age here: \n{st.session_state.age} and use that as a basis reading comprehension and look for books that are \n{st.session_state.goal} based on that age. "},
            {"role": "assistant", "content": "I see your age here: \n{st.session_state.age} and will make my recommendation based on your goal of \n{st.session_state.goal}. I will also use your selections in the {st.session_state.genres} genres when I make the recommendation."},
            {"role": "user", "content": "Do not suggest any of the books in the list here: \n{st.session_state.pastbooks} These are books that either have already been recommended or read."},
            {"role": "user", "content": question},
            #{"role": "user", "content": 'Please recommend the 3 books in the layout "Book 1, Book 2, Book 3"'},
            {"role": "user", "content": 'Please describe using 3 bullet points, one sentence each, why you are recommending these books. You should not make up details about the book that are not true.'},
            {"role": "assistant", "content": 'I will make your recommendations!'},
            {"role": "user", "content": 'Give me a book recommendations that are \n{st.session_state.goal}'},
        ],
        temperature=0.2
    )

    book_titles = re.findall(r'"([^"]+)"', response.choices[0].message.content)
    # Joining book titles into a single string separated by commas
    book_titles_string = ', '.join(book_titles)

    st.session_state.recommendations = response.choices[0].message.content
    container2_home.write(st.session_state.recommendations)
    st.session_state.pastbooks.extend([book_titles_string])

    # Add buttons for liking and disliking the recommendation
    liked_button = container2_home.button('Did you like the recommendation?', on_click=toggleLikedRecommendation)
    disliked_button = container2_home.button('Did you dislike the recommendation?', on_click=toggleDislikedRecommendation)

    # If user disliked the recommendation, provide a text input for feedback
    if st.session_state.liked_recommendation is False:
        st.session_state.feedback_text = feedback_container.text_input(
            "Provide feedback on why you didn't like the recommendation:")
        st.session_state.feedback_text = st.session_state.feedback_text.strip()
        if st.session_state.feedback_text:
            feedback_container.write(f"Feedback received: {st.session_state.feedback_text}")
    else:
        # Clear the feedback text if the user liked the recommendation
        st.session_state.feedback_text = ""

def toggleLikedRecommendation():
    st.session_state.liked_recommendation = True
    st.session_state.past_recommendations.extend(st.session_state.recommendations[-3:])
    st.success('Thank you for your positive feedback! 😊')

def toggleDislikedRecommendation():
    st.session_state.liked_recommendation = False
    st.session_state.dislikes.extend(st.session_state.recommendations[-3:])
    st.success('Thank you for your feedback. We will not suggest this book again')

container2_home.button('Get Recommendations', on_click=getRecommendations)

# Get Summaries of Recommendations
container3_home = st.container(border=True)


def getSummaries():
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    summary_prompt = f"""You are a helpful assistant that provides summaries of books from a list. 
                Provide summaries for the following books, without major spoilers: {st.session_state.recommendations}. 
                Do not make up details or hallucinate.
                After each summary provide a difficulty rating for each book on a scale of 1-10."""

    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[{"role": 'assistant', "content": summary_prompt}]
    )

    container3_home.write(response.choices[0].message.content)


container3_home.button('Get Summaries', on_click=getSummaries)

