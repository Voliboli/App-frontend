import yaml
import st_pages as stp
import streamlit_authenticator as stauth
import streamlit as st

st.set_page_config(page_title="Main Page", page_icon="🏠", layout="wide", initial_sidebar_state="auto")

stp.show_pages(
    [
        stp.Page("pages/Main_Page.py", "Main Page", "🏠"),
        stp.Page("pages/1_Upload_&_Visualize.py", "Upload & Visualize", "📄"),
        stp.Page("pages/2_Select_&_Analyze.py", "Select & Analyze", "🏆"),
        stp.Page("pages/3_Register.py", "Register", "🔒"),
        stp.Page("pages/4_About.py", "About", "💡")
    ]
)

st.sidebar.image("assets/Voliboli.jpg", use_column_width=True)

with open('auth/auth.yaml') as file:
    config = yaml.load(file, Loader=yaml.loader.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
authenticator._check_cookie() # NOTE: bug in the imported library (need to call it manually)

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar')
else:
    name, authentication_status, username = authenticator.login('Login', 'sidebar')

st.title("Main Page 🏠")
st.write("Welcome to our Web application for volleyball enthusiasts! \
        Our platform offers a unique opportunity to analyze and compare volleyball statistics using visually appealing graphs. \
        Whether you're a coach, player, or just a fan of the game, our platform provides valuable insights into player performance and team strategy. \
        With the ability to upload your own match statistics in PDF format or search our database, you can easily access the information. \
        Our user-friendly interface allows for easy navigation of the data, so you can focus on what's important - improving your game. \
        Join our community today and take your volleyball analysis to the next level!")
st.markdown(
   """
    ### ⚡ Use Cases:
    **Feature**|**Description**
    -----|-----
    |Player| **Select & Analyze**: Explore individual player statistics throughout the season.|
    |Comparison| **Compare & Evaluate**:  Evaluate players' statistics by comparing them against one another.|
    |Game| **Upload & Visualize**: Upload and visualize game statistics using visually appealing graphs.|
    """
)
st.text("")
st.markdown(
   """
        ### 💪 Challenge:
        ##### Here's why you might find this platform useful:
        - Track the dynamic changes in an individual's performance throughout the season, allowing you to witness their progress firsthand.
        - Engage with interactive graphs that bring statistics to life, providing a richer experience compared to traditional static PDF data.
        - Conduct insightful player comparisons, examining how different individuals performed against the same opponent, providing valuable insights into their strengths and weaknesses.
    """
)
