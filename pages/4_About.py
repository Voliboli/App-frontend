import yaml
import streamlit as st
import st_pages as stp
from streamlit_timeline import timeline
import streamlit_authenticator as stauth

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

st.title("About 💡")
st.write("**Teodor Janez Podobnik**, Creator of Voliboli")
st.write("")
st.write("As the creator of Voliboli, I am passionate about using technology to help people improve their volleyball skills and understanding of the game. \
           With years of experience as a player, I understand the importance of data-driven decision-making in sports. \
           My vision for Voliboli is to **provide volleyball enthusiasts with an easy-to-use platform for analyzing and comparing statistics.** \
           I believe that data visualization is key to unlocking insights and improving performance, and I have worked tirelessly to create a user-friendly interface that makes data analysis accessible to everyone.")
st.write("")
st.write("When I'm not working on Voliboli or playing volleyball, I enjoy working my two part-time jobs as a Cloud Architect or hanging out with friends. \
           I believe that a well-rounded life is essential to success in any endeavor, and I strive to bring that perspective to everything I do. \
           Thank you for choosing Voliboli. I am confident that our platform will help you take your volleyball analysis to the next level, and **I look forward to hearing your feedback and suggestions for how we can continue to improve.**")


# load data
data = None
with open('timeline.json', "r") as f:
    data = f.read()

# render timeline
timeline(data, height=426)
