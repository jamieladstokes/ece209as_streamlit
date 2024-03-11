
  # Bookify - Streamlit Version 

  Note: Please ensure you have installed Streamlit (pip install streamlit). Some users have reported issues when running outside of a virtual environment. I'm running it in a conda virtual 
        environment to be safe.  

  Additional Dependencies: openai library (& associated API key).

  To preview and run the project on your device:
  1) Open project folder (name: stream_test) in <a href="https://code.visualstudio.com/download">Visual Studio Code</a>
  2) In Home.py, and pages/chat.py, replace the OPENAI_API_KEY variable with your API key. 
  3) In the terminal, run `streamlit run Home.py'
  4) View project in browser
  
Structure:
1) Need a Home.py file that serves as the app's homepage.
2) Additional app pages can each be coded in their own .py files. These py files need to be stored in a 'pages' folder that lies in the same directory as the Home.py file.
3) the streamlit.session_state dictionary object can store variables/values across pages.
4) Still have to figure out how to store session_state info across diffferent runtimes (maybe store it in a csv for demo purposes, idk). 
