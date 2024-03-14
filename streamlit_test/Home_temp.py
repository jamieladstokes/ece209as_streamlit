import streamlit as st
from openai import OpenAI

OPENAI_API_KEY = "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"
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

st.session_state.goal = 'Just my Level'

st.title("Bookify!")


# Updated Profile Info 
container1_home = st.container(border=True)

def refreshInfo():
    container1_home.write(st.session_state.name)
    container1_home.write(st.session_state.age)
    container1_home.write('Favorite Genres: ')
    container1_home.write(st.session_state.genres)
    container1_home.write(st.session_state.goal)

container1_home.button('Refresh User Info', on_click=refreshInfo)


# Get Book Recommendation Titles 
container2_home = st.container(border=True)
container2_home.header('Book Recommendations')

def getRecommendations():
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    question = f"I like to read a lot and am interested in books that are \n{st.session_state.goal}. Sometimes I have a hard time figuring out the next book I should be reading, but have an idea for the genres I'm interested in. Since I generally have liked books I've read in the past, I'd like to use those books as a model for the books I should read next. Please use my \n{books_read} list and recommend 3 books from the following genres: {st.session_state.genres}. If you don't have any recommendations, please say 'I don't know'. Don't make recommendations from those i've read in the past."

    messages=[
                    {"role": "system", "content": "You are a helpful assistant that recommends 3 books to read based on how challenging the books are"},
                    {"role": "user", "content": "Please look at all of the books that I have previously read here: \n{books_read}"},
                    {"role": "assistant", "content": "I see all of the books that you have read here: \n{books_read} and will use them to base my recommendation off of when you ask. "},
                    {"role": "user", "content": "Now, please look at my age here: \n{st.session_state.age} and use that as a basis reading comprehension and look for books that are \n{st.session_state.goal} based on that age. "},
                    {"role": "assistant", "content": "I see your age here: \n{st.session_state.age} and will make my recommendation based on your goal of \n{st.session_state.goal}. I will also use your selections in the {st.session_state.genres} genres when I make the recommendation."},
                    {"role": "user", "content": question},
                    {"role": "user", "content": 'Please describe using 3 bullet points, one sentence each, why you are recommending these books. You should not make up details about the book that are not true.'},
                    {"role": "assistant", "content": 'I will make your recommendations!'},
                    {"role": "user", "content": 'Please make sure these books are in the {st.session_state.genres} genres before making the recommendation. When you make the recommendation, never apologize.'},
            ],
    
    #rec_prompt = f"""You are a helpful assistant that recommends books to read based on lists. 
    #               Your user client likes the following genres: {st.session_state.genres}. 
    #               Recommend 3 books for them. Output only the book titles (e.g. 'Dune, Star Wars, Harry Potter')."""
    
    response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages= messages,
            temperature=0.4
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

    
