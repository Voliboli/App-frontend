import yaml
import streamlit as st
import st_pages as stp
import streamlit_authenticator as stauth
import requests
from voliboli_sgqlc_types.main import Mutation, Query
from sgqlc.operation import Operation

stp.show_pages(
    [
        stp.Page("Main_Page.py", "Main Page", "🏠"),
        stp.Page("pages/1_Upload_&_Visualize.py", "Upload & Visualize", "📄"),
        stp.Page("pages/2_Select_&_Analyze.py", "Select & Analyze", "🏆"),
        stp.Page("pages/3_Register.py", "Register", "🔒"),
        stp.Page("pages/4_About.py", "About", "💡")
    ]
)
st.sidebar.image("assets/Voliboli.jpg", use_column_width=True)

session = requests.Session()
BASE = "http://172.35.1.3:5000"
query = Operation(Query)

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

print("here")
query.getTeams()
print("+++++++++++++++++")
resp = session.post(BASE + "/teams", json={'query': str(query)})
print("----------------")
print(resp.json())
print("----------------")
st.write(resp.json())
#resp.json()["data"]["getTeams"]["success"])
print("xxxxxxxxxxxxxxxxxxxxxxx")

st.header("Select & Analyze 🏆")
if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar')
    st.write("Welcome to the Statistics Database page!")
    st.write("Here, you can search through our extensive database of player statistics, compare players against each other, and evaluate their performance throughout the season. \
              To get started, use the search bar to find the players you're interested in or select multiple players to compare their statistics side-by-side.")


    '''
    status = st.radio("Select Team: ", (ateam1, ateam2))
    if ("selection1_" + uploaded_file.name) not in st.session_state:
        st.session_state["selection1_" + uploaded_file.name] = []
    if ("selection2_" + uploaded_file.name) not in st.session_state:
        st.session_state["selection2_" + uploaded_file.name] = []

    # NOTE: Weird way of achieving for the multi-select widget to updateX
    # ############################################ DO NOT MODIFY #############################
    def update_selection(key, selection):
        st.session_state[key] = selection

    selection1 = st.session_state["selection1_" + uploaded_file.name]
    selection2 = st.session_state["selection2_" + uploaded_file.name]
    last_selection = st.session_state["selection1_" + uploaded_file.name] + st.session_state["selection2_" + uploaded_file.name]
    if status == ateam1:
        selection1 = st.multiselect(f"{ateam1} - Players: ", names1, default=st.session_state["selection1_" + uploaded_file.name], on_change=update_selection, args=("selection1_" + uploaded_file.name, selection1))
        st.session_state["selection1_" + uploaded_file.name] = selection1
    else:
        selection2 = st.multiselect(f"{ateam2} - Players: ", names2, default=st.session_state["selection2_" + uploaded_file.name], on_change=update_selection, args=("selection2_" + uploaded_file.name, selection2))
        st.session_state["selection2_" + uploaded_file.name] = selection2
    ###########################################################################################

    query.getPlayer(name='Mark')
    resp = requests.post(BASE + "/players", json={'query': str(query)})
    print(resp.json())
    self.assertTrue(resp.json()["data"]["getPlayer"]["success"])
    '''

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
