import yaml
import streamlit as st
import st_pages as stp
import streamlit_authenticator as stauth

stp.show_pages(
    [
        stp.Page("app.py", "Home", "🏠"),
        stp.Page("pages/page_1.py", "Upload & Visualize", "📄"),
        stp.Page("pages/page_2.py", "Select & Analyze", "🏆"),
        stp.Page("pages/page_3.py", "About", "💡"),
        stp.Page("pages/page_4.py", "Register", "🔒")
    ]
)
st.sidebar.image("assets/Voliboli.jpg", use_column_width=True)

with open('auth.yaml') as file:
    config = yaml.load(file, Loader=yaml.loader.SafeLoader)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
authenticator._check_cookie() # NOTE: bug in the imported library (need to call it manually)

st.header("Select & Analyze 🏆")
if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar')
    st.write("Welcome to the Statistics Database page!")
    st.write("Here, you can search through our extensive database of player statistics, compare players against each other, and evaluate their performance throughout the season. \
              To get started, use the search bar to find the players you're interested in or select multiple players to compare their statistics side-by-side.")
    st.write("This is still under active development but is planned to come out soon!")
    st.image("assets/coming_soon.jpg", use_column_width=True)
elif st.session_state["authentication_status"] is False:
    name, authentication_status, username = authenticator.login('Login', 'sidebar')
    st.sidebar.error('Username/password is incorrect')
    st.warning("We apologize for the inconvenience, but to access this page, please log in to your account. \
              Your security is our top priority, and this login requirement helps to ensure that your personal information remains protected. \
              Thank you for your understanding.")
elif st.session_state["authentication_status"] is None:
    name, authentication_status, username = authenticator.login('Login', 'sidebar')
    st.warning("We apologize for the inconvenience, but to access this page, please log in to your account. \
              Your security is our top priority, and this login requirement helps to ensure that your personal information remains protected. \
              Thank you for your understanding.")