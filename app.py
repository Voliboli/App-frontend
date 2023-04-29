import st_pages as stp
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

# st_pages conflict with the streamlit_authenticator library, causing the initial popup error saying something like: 
# "The requested page does not exist. Loading default app's page"
# As a workaround, there's an app.py page, that doesn't use streamlit_authenticator app, which hides the login prompt on the sidebar
# But if the user clicks on the Main Page icon on the sidebar, this appears because the Main_Page.py is called and not the app.py
# app.py only ran at the beginning 

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
    |Player| **Select & Analyze** individual player statistics throughout the season|
    |Comparison| **Compare & Evaluate** players statistics against one another|
    |Game| **Upload & Visualize** game statistics using visually appealing graphs.|
    """
)
st.text("")
st.markdown(
    """
        ### 💪 Challenge:
        ##### Here's why you might find this platform useful:
        - You can how a certain individual perfomance was changing througout the season
        - You can interact with graphs instead of the usual static statistics on the PDF
        - You can compare different players and how they performed against the same opponent
        - etc.
    """
)