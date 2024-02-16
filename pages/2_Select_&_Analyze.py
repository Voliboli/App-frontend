import yaml
import altair as alt
import pandas as pd
import streamlit as st
import st_pages as stp
import streamlit_authenticator as stauth
import requests
from voliboli_sgqlc_types.main import Mutation, Query
from sgqlc.operation import Operation

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

session = requests.Session()
BASE = "http://voliboli-backend.voliboli.svc.cluster.local:80"

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

st.header("Select & Analyze 🏆")
if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar')
    st.write("Welcome to the Statistics Database page!")
    st.write("Here, you can search through our extensive database of player statistics, compare players against each other, and evaluate their performance throughout the season. \
              To get started, use the search bar to find the players you're interested in or select multiple players to compare their statistics side-by-side.")

    q1 = Operation(Query)
    q1.getTeams()
    resp = session.post(BASE + "/teams", json={'query': str(q1)})
    q = resp.json()
    teams = []
    for t in q["data"]["getTeams"]["teams"]:
        teams.append(t['name'])

    team = st.selectbox("Select Team: ", teams)

    if team:
        q2 = Operation(Query)
        q2.getTeam(name=team).__to_graphql__(auto_select_depth=5)
        resp = requests.post(BASE + "/teams", json={'query': str(q2.__to_graphql__(auto_select_depth=3))})
        p = resp.json()
        players = []
        player_names = []
        for player in p["data"]["getTeam"]["team"]["players"]:
            players.append(player)
            player_names.append(player["name"])

        player = st.selectbox(f"Select Player from {team}: ", player_names)

        q3 = Operation(Query)
        q3.getPlayer(name=player)
        resp = requests.post(BASE + "/players", json={'query': str(q3)})
        player_stat = resp.json()["data"]["getPlayer"]["player"]

        def unpack_stats3(stat):
            tmp = stat.split(",")
            out = []
            for e in tmp:
                e = e.replace("[", "").replace("]", "").replace("'", "").strip()
                out.append(e)
            return out  

        def unpack_stats2(stat):
            tmp = stat.split(",")
            out = []
            for e in tmp:
                e = e.replace("(", "").replace(")", "").replace("%", "").strip()
                if e == '.':
                    e = '0'
                out.append(str(int(e)/100))
            return out       

        def unpack_stats(stat):
            tmp = stat.split(",")
            out = []
            for e in tmp:
                if e == '.':
                    e = '0'
                out.append(e)
            return out

        votes = unpack_stats(player_stat["votes"])
        total_points = unpack_stats(player_stat["totalPoints"])
        break_points = unpack_stats(player_stat["breakPoints"])
        wl_points = unpack_stats(player_stat["winloss"])
        total_serves = unpack_stats(player_stat["totalServe"])
        serve_errors = unpack_stats(player_stat["errorServe"])
        serve_points = unpack_stats(player_stat["pointsServe"])
        total_receptions = unpack_stats(player_stat["totalReception"])
        error_receptions = unpack_stats(player_stat["errorReception"])
        pos_receptions = unpack_stats2(player_stat["posReception"])
        exc_receptions = unpack_stats2(player_stat["excReception"])
        total_attacks = unpack_stats(player_stat["totalAttacks"])
        error_attacks = unpack_stats(player_stat["errorAttacks"])
        block_attacks = unpack_stats(player_stat["blockedAttacks"])
        pts_attacks = unpack_stats(player_stat["pointsAttack"])
        perc_attacks = unpack_stats2(player_stat["posAttack"])
        pts_blocks = unpack_stats(player_stat["pointsBlock"])
        opponents = unpack_stats(player_stat["opponent"])
        n_stat = len(votes)
        dates = unpack_stats3(player_stat["date"])

        legend = []
        for opp, date in zip(opponents, dates):
            legend.append(f"{opp} ({date})")
        
        columns1 = ["Total Points",
                    "Break Points",
                    "Total Serves",
                    "Serve Errors",
                    "Serve Points",
                    "Total Receptions",
                    "Reception Errors",
                    "Total Attacks",
                    "Attack Errors",
                    "Blocked Attacks",
                    "Attack Points",
                    "Block points"]
        
        # Number of columns per category
        categories1 = []
        for col in columns1:
            for _ in range(n_stat):
                categories1.append(col)

        groups1 = []
        for _ in range(len(columns1)):
            for l in legend:
                groups1.append(l)
        values1 = total_points + break_points + total_serves + serve_errors + \
                    serve_points + total_receptions + error_receptions + total_attacks + \
                    error_attacks + block_attacks + pts_attacks + pts_blocks
        source1 = pd.DataFrame({"Category":list(categories1),
                                "Group":groups1,
                                "Value":values1})
        chart1 = alt.Chart(source1).mark_bar().encode(
            x="Category:N",
            y="Value:Q",
            xOffset="Group:N",
            color="Group:N"
        )
        st.altair_chart(chart1, use_container_width=True, theme="streamlit")

        columns2 = ["Positive Reception",
                    "Excellent Reception",
                    "Attack Efficiency"]
        categories2 = []
        for col in columns2:
            for _ in range(n_stat):
                categories2.append(col)

        groups2 = []
        for _ in range(len(columns2)):
            for l in legend:
                groups2.append(l)
        values2 = pos_receptions + exc_receptions + perc_attacks
        source2 = pd.DataFrame({"Category":list(categories2),
                                "Group":groups2,
                                "Value":values2})
        chart2 = alt.Chart(source2).mark_bar().encode(
            x=alt.X('Value:Q', axis=alt.Axis(format='%')),
            y="Category:N",
            yOffset="Group:N",
            color="Group:N"
        )
        st.altair_chart(chart2, use_container_width=True, theme="streamlit")

        columns3 = ["W-L Points"]
        categories3 = []
        for col in columns3:
            for _ in range(n_stat):
                categories3.append(col)
        groups3 = []
        for _ in range(len(columns3)):
            for l in legend:
                groups3.append(l)
        values3 = wl_points
        source3 = pd.DataFrame({"Category":list(categories3),
                                "Group":groups3,
                                "Value":values3})

        chart3 = alt.Chart(source3).mark_bar().encode(
            x="Category:N",
            y="Value:Q",
            color="Group:N",
            xOffset="Group:N",
        )

        st.altair_chart(chart3, use_container_width=True, theme="streamlit")

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
