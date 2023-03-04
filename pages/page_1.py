import os
import tabula as tb
import streamlit as st
from io import StringIO
from pdf2image import convert_from_path
from pathlib import Path
import tempfile
import base64
import st_pages as stp

stp.show_pages(
    [
        stp.Page("app.py", "Home", "🏠"),
        stp.Page("pages/page_1.py", "Upload & Visualize", "📄"),
        stp.Page("pages/page_2.py", "Select & Analyze", "🏆")
    ]
)

season = "2022-23"
team_names = ["Calcit Volley",
              "FužinarSijMetalRavne",
              "HišaNaKolesihTriglav",
              "Salonit Anhovo",
              "ACH Volley Ljubljana",
              "Črnuče",
              "Merkur Maribor",
              "Panvita Pomgrad"]
teams = {
    "Calcit Volley" : {"1": "Planinšič Uroš",
                       "2": "Mujanović Nik",
                       "5": "Vinkovič Dino",
                       "6": "Lazar Luka",
                       "8": "Klobučar Jan",
                       "10": "Košenina Alan",
                       "11": "Arsenoski Miloš",
                       "12": "Okroglič Jure",
                       "13": "Sosa Luis",
                       "23": "Aponza Daniel",
                       "77": "Pavlovič Uroš"},
    "FužinarSijMetalRavne": {"1": "Cafuta Miha",
                             "3": "Lednik Nace",
                             "4": "Križanič Bor",
                             "5": "Knuplež Jani",
                             "6": "Ranc David",
                             "7": "Bregar Miha",
                             "9": "Erpič Uroš",
                             "10": "Makaš Emir",
                             "11": "Levar Uroš",
                             "12": "Hribernik Žiga",
                             "14": "Vučetić Luka",
                             "23": "Ranc Vid"},
    "HišaNaKolesihTriglav": {"1": "Ibrišimovič Gal",
                             "3": "Nanut Maj",
                             "6": "Tučen Uroš",
                             "7": "Adžović Adi",
                             "9": "Rotar Bor Jese",
                             "11": "Snedec Amadej",
                             "12": "Jovović Đorđe",
                             "13": "Mali Miha",
                             "15": "Šikanič Aljoša",
                             "16": "Glamočanin Jure",
                             "17": "Fajfar Matic"},
    "Salonit Anhovo": {"1": "Kodrič Erik",
                       "2": "Stojanovič Aleksander",
                       "3": "Šarić Danijel",
                       "5": "Hesselholt Joachim",
                       "6": "Karnel Irenej",
                       "7": "Jeklin Primož",
                       "8": "Godnič Jani",
                       "9": "Kavčič Jakob",
                       "10": "Maretič Lian Svit",
                       "11": "Bojić Slobodan",
                       "12": "Okroglič Grega",
                       "13": "Kovačič Aleks",
                       "15": "Vrtovec Matic",
                       "17": "Maksimović Marko"},
    "ACH Volley Ljubljana": {"1": "Mejal Primož",
                             "5": "Šket Alen",
                             "8": "Mašulović Nemanja",
                             "9": "Todorović Vuk",
                             "10": "Bošnjak Črtomir",
                             "11": "Koncilja Danijel",
                             "12": "Šestan Filip",
                             "13": "Kovačič Jani",
                             "14": "Gjorgiev Nikola",
                             "17": "Videčnik Matic",
                             "18": "Kök Matej",
                             "19": "Šen Klemen"},
    "Črnuče": {"2": "Mihelčič Gregor",
               "6": "Karadža Pevc Matevž",
               "8": "Verdinek Jožef",
               "9": "Rojnik Matic",
               "10": "Oman Jurij",
               "11": "Sešek Jaka",
               "13": "Marovt Luka",
               "15": "Jančič Jan Karl",
               "16": "Valenčič Martin",
               "19": "Ramšak Vid",
               "33": "Česnovar Matic"},
    "Merkur Maribor": {"2": "Jevšnik Jaka",
                       "3": "Vodušek Timotej",
                       "4": "Pernuš Gregor",
                       "5": "Adžović Sani",
                       "6": "McConnell Connor",
                       "8": "Bračko Rok",
                       "9": "Kumer Žiga",
                       "10": "Kržič Janž Janez",
                       "11": "Donik Žiga",
                       "12": "Leva Filip",
                       "13": "Fink Miha",
                       "14": "Najdič Nejc",
                       "16": "Iršič Jaka",
                       "42": "Peruničić Nemanja"},
    "Panvita Pomgrad": {"1": "Rajnar Urban",
                        "5": "Šormaz Nenad",
                        "6": "Avšič Tine",
                        "7": "Drvarič Urban",
                        "8": "Vrabl Tin",
                        "10": "Rojnik Jakob",
                        "11": "Kovačič Tit",
                        "12": "Legen Nik",
                        "13": "Milovanović Marko",
                        "14": "Bedrač Žan",
                        "15": "Fužir Urban",
                        "16": "Novak David"},
}

# metadata
STAT_DIRECTORY = 'stats'
DEBUG = False

# boundaries
TEAM1_UB = 180
TEAM1_LB = 340
TEAM2_UB = 425
TEAM2_LB = 580

def show_pdf(file_path:str):
    """Show the PDF in Streamlit - That returns as html component"""
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)

def unpack_df(df):
    a = []
    for (colName, colData) in df.items():
        a.append(colName)
        for d in colData:
            a.append(d)

    return a

def autocomplete_teamname(name):
    for n in team_names:
        if name in n:
            return n 
    return None

st.set_page_config(page_title="Upload & Visualize", page_icon="🏐")
uploaded_files = st.file_uploader(label="Choose a PDF file", type=['pdf'], accept_multiple_files=True)
if uploaded_files is not None:
    for uploaded_file in uploaded_files:
        # Make temp file path from uploaded file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            #st.markdown("## Original PDF file")
            fp = Path(tmp_file.name)
            fp.write_bytes(uploaded_file.getvalue())
            #st.write(show_pdf(tmp_file.name)) # DISPLAYS PDF

            #if st.checkbox("Show/Hide PDF"):
            #    imgs = convert_from_path(tmp_file.name)
            #    st.image(imgs)

            file = tmp_file.name

            game = tb.read_pdf(file, area = (40, 300, 85, 480), pages = '1')[0]
            game = unpack_df(game)
            team1, team2 = game
            if (ateam1 := autocomplete_teamname(team1)) is None:
                print(f"Failed to resolve team name: {team1}")
                continue
            if (ateam2 := autocomplete_teamname(team2)) is None:
                print(f"Failed to resolve team name: {team2}")
                continue

            result = tb.read_pdf(file, area = (40, 550, 85, 570), pages = '1')[0]
            time = tb.read_pdf(file, area = (105, 70, 115, 150), pages = '1')[0]
            location = tb.read_pdf(file, area = (120, 70, 135, 150), pages = '1')[0]

            team1_numbers = tb.read_pdf(file, area = (TEAM1_UB, 20, TEAM1_LB, 40), pages = '1')[0]
            team1_names = tb.read_pdf(file, area = (TEAM1_UB, 45, TEAM1_LB, 145), pages = '1')[0]
            team1_votes = tb.read_pdf(file, area = (TEAM1_UB, 190, TEAM1_LB, 240), pages = '1')[0]
            team1_points_tot = tb.read_pdf(file, area = (TEAM1_UB, 230, TEAM1_LB, 250), pages = '1')[0]
            team1_points_bp = tb.read_pdf(file, area = (TEAM1_UB, 250, TEAM1_LB, 270), pages = '1')[0]
            team1_points_wl = tb.read_pdf(file, area = (TEAM1_UB, 270, TEAM1_LB, 290), pages = '1')[0]
            team1_serve_tot = tb.read_pdf(file, area = (TEAM1_UB, 290, TEAM1_LB, 310), pages = '1')[0]
            team1_serve_err = tb.read_pdf(file, area = (TEAM1_UB, 310, TEAM1_LB, 330), pages = '1')[0]
            team1_serve_pts = tb.read_pdf(file, area = (TEAM1_UB, 330, TEAM1_LB, 350), pages = '1')[0]
            team1_rec_tot = tb.read_pdf(file, area = (TEAM1_UB, 350, TEAM1_LB, 380), pages = '1')[0]
            team1_rec_err = tb.read_pdf(file, area = (TEAM1_UB, 380, TEAM1_LB, 400), pages = '1')[0]
            team1_rec_pos = tb.read_pdf(file, area = (TEAM1_UB, 400, TEAM1_LB, 420), pages = '1')[0]
            team1_rec_exc = tb.read_pdf(file, area = (TEAM1_UB, 420, TEAM1_LB, 450), pages = '1')[0]
            team1_att_tot = tb.read_pdf(file, area = (TEAM1_UB, 450, TEAM1_LB, 470), pages = '1')[0]
            team1_att_err = tb.read_pdf(file, area = (TEAM1_UB, 470, TEAM1_LB, 490), pages = '1')[0]
            team1_att_blk = tb.read_pdf(file, area = (TEAM1_UB, 490, TEAM1_LB, 510), pages = '1')[0]
            team1_att_pts = tb.read_pdf(file, area = (TEAM1_UB, 510, TEAM1_LB, 530), pages = '1')[0]
            team1_att_exc = tb.read_pdf(file, area = (TEAM1_UB, 530, TEAM1_LB, 560), pages = '1')[0]
            team1_blk = tb.read_pdf(file, area = (TEAM1_UB, 560, TEAM1_LB, 580), pages = '1')[0]
            
            if DEBUG:
                print(time)
                print(location)
                print(game)
                print(result)
                print(team1_numbers)
                print(team1_names)
                print(team1_votes)
                print(team1_points_tot)
                print(team1_points_bp)
                print(team1_points_wl)
                print(team1_serve_tot)
                print(team1_serve_err)
                print(team1_serve_pts)
                print(team1_rec_tot)
                print(team1_rec_err)
                print(team1_rec_pos)
                print(team1_rec_exc)
                print(team1_att_tot)
                print(team1_att_err)
                print(team1_att_blk)
                print(team1_att_pts)
                print(team1_att_exc)
                print(team1_blk)

            team1_numbers = unpack_df(team1_numbers)
            #team1_names = unpack_df(team1_names)
            names1 = []
            for num in team1_numbers:
                names1.append(teams[ateam1][str(num)])

            team1_votes = unpack_df(team1_votes)
            team1_points_tot = unpack_df(team1_points_tot)
            team1_points_bp = unpack_df(team1_points_bp)
            team1_points_wl = unpack_df(team1_points_wl)
            team1_serve_tot = unpack_df(team1_serve_tot)
            team1_serve_err = unpack_df(team1_serve_err)
            team1_serve_pts = unpack_df(team1_serve_pts)
            team1_rec_tot = unpack_df(team1_rec_tot)
            team1_rec_err = unpack_df(team1_rec_err)
            team1_rec_pos = unpack_df(team1_rec_pos)
            team1_rec_exc = unpack_df(team1_rec_exc)
            team1_att_tot = unpack_df(team1_att_tot)
            team1_att_err = unpack_df(team1_att_err)
            team1_att_blk = unpack_df(team1_att_blk)
            team1_att_pts = unpack_df(team1_att_pts)
            team1_att_exc = unpack_df(team1_att_exc)
            team1_blk = unpack_df(team1_blk)


            players1 = {}
            for (a, b, c, d, e, f, g, h, j, k, l, m, n, o, p, r, s, u) in zip(names1, 
                                                                                team1_votes, 
                                                                                team1_points_tot, 
                                                                                team1_points_bp, 
                                                                                team1_points_wl, 
                                                                                team1_serve_tot, 
                                                                                team1_serve_err, 
                                                                                team1_serve_pts, 
                                                                                team1_rec_tot,
                                                                                team1_rec_err,
                                                                                team1_rec_pos,
                                                                                team1_rec_exc,
                                                                                team1_att_tot,
                                                                                team1_att_err,
                                                                                team1_att_blk,
                                                                                team1_att_pts, 
                                                                                team1_att_exc,
                                                                                team1_blk):
                print(a, b, c, d, e, f, g, h, j, k, l, m, n, o, p, r, s, u)
                print("--------------------")
                players1[a] = [b, c, d, e, f, g, h, j, k, l, m, n, o, p, r, s, u]

            
            team2_numbers = tb.read_pdf(file, area = (TEAM2_UB, 20, TEAM2_LB, 40), pages = '1')[0]
            team2_names = tb.read_pdf(file, area = (TEAM2_UB, 45, TEAM2_LB, 145), pages = '1')[0]
            team2_votes = tb.read_pdf(file, area = (TEAM2_UB, 190, TEAM2_LB, 240), pages = '1')[0]
            team2_points_tot = tb.read_pdf(file, area = (TEAM2_UB, 230, TEAM2_LB, 250), pages = '1')[0]
            team2_points_bp = tb.read_pdf(file, area = (TEAM2_UB, 250, TEAM2_LB, 270), pages = '1')[0]
            team2_points_wl = tb.read_pdf(file, area = (TEAM2_UB, 270, TEAM2_LB, 290), pages = '1')[0]
            team2_serve_tot = tb.read_pdf(file, area = (TEAM2_UB, 290, TEAM2_LB, 310), pages = '1')[0]
            team2_serve_err = tb.read_pdf(file, area = (TEAM2_UB, 310, TEAM2_LB, 330), pages = '1')[0]
            team2_serve_pts = tb.read_pdf(file, area = (TEAM2_UB, 330, TEAM2_LB, 350), pages = '1')[0]
            team2_rec_tot = tb.read_pdf(file, area = (TEAM2_UB, 350, TEAM2_LB, 380), pages = '1')[0]
            team2_rec_err = tb.read_pdf(file, area = (TEAM2_UB, 380, TEAM2_LB, 400), pages = '1')[0]
            team2_rec_pos = tb.read_pdf(file, area = (TEAM2_UB, 400, TEAM2_LB, 420), pages = '1')[0]
            team2_rec_exc = tb.read_pdf(file, area = (TEAM2_UB, 420, TEAM2_LB, 450), pages = '1')[0]
            team2_att_tot = tb.read_pdf(file, area = (TEAM2_UB, 450, TEAM2_LB, 470), pages = '1')[0]
            team2_att_err = tb.read_pdf(file, area = (TEAM2_UB, 470, TEAM2_LB, 490), pages = '1')[0]
            team2_att_blk = tb.read_pdf(file, area = (TEAM2_UB, 490, TEAM2_LB, 510), pages = '1')[0]
            team2_att_pts = tb.read_pdf(file, area = (TEAM2_UB, 510, TEAM2_LB, 530), pages = '1')[0]
            team2_att_exc = tb.read_pdf(file, area = (TEAM2_UB, 530, TEAM2_LB, 560), pages = '1')[0]
            team2_blk = tb.read_pdf(file, area = (TEAM2_UB, 560, TEAM2_LB, 580), pages = '1')[0]
            
            if DEBUG:
                print(team2_names)
                print(team2_votes)
                print(team2_points_tot)
                print(team2_points_bp)
                print(team2_points_wl)
                print(team2_serve_tot)
                print(team2_serve_err)
                print(team2_serve_pts)
                print(team2_rec_tot)
                print(team2_rec_err)
                print(team2_rec_pos)
                print(team2_rec_exc)
                print(team2_att_tot)
                print(team2_att_err)
                print(team2_att_blk)
                print(team2_att_pts)
                print(team2_att_exc)
                print(team2_blk)
            
            team2_numbers = unpack_df(team2_numbers)
            #team2_names = unpack_df(team2_names)
            names2 = []
            for num in team2_numbers:
                names2.append(teams[ateam2][str(num)])

            team2_votes = unpack_df(team2_votes)
            team2_points_tot = unpack_df(team2_points_tot)
            team2_points_bp = unpack_df(team2_points_bp)
            team2_points_wl = unpack_df(team2_points_wl)
            team2_serve_tot = unpack_df(team2_serve_tot)
            team2_serve_err = unpack_df(team2_serve_err)
            team2_serve_pts = unpack_df(team2_serve_pts)
            team2_rec_tot = unpack_df(team2_rec_tot)
            team2_rec_err = unpack_df(team2_rec_err)
            team2_rec_pos = unpack_df(team2_rec_pos)
            team2_rec_exc = unpack_df(team2_rec_exc)
            team2_att_tot = unpack_df(team2_att_tot)
            team2_att_err = unpack_df(team2_att_err)
            team2_att_blk = unpack_df(team2_att_blk)
            team2_att_pts = unpack_df(team2_att_pts)
            team2_att_exc = unpack_df(team2_att_exc)
            team2_blk = unpack_df(team2_blk)


            players2 = {}
            for (a, b, c, d, e, f, g, h, j, k, l, m, n, o, p, r, s, u) in zip(names2, 
                                                                                team2_votes, 
                                                                                team2_points_tot, 
                                                                                team2_points_bp, 
                                                                                team2_points_wl, 
                                                                                team2_serve_tot, 
                                                                                team2_serve_err, 
                                                                                team2_serve_pts, 
                                                                                team2_rec_tot,
                                                                                team2_rec_err,
                                                                                team2_rec_pos,
                                                                                team2_rec_exc,
                                                                                team2_att_tot,
                                                                                team2_att_err,
                                                                                team2_att_blk,
                                                                                team2_att_pts, 
                                                                                team2_att_exc,
                                                                                team2_blk):
                print(a, b, c, d, e, f, g, h, j, k, l, m, n, o, p, r, s, u)
                print("--------------------")
                players2[a] = [b, c, d, e, f, g, h, j, k, l, m, n, o, p, r, s, u]

            status = st.radio("Select Team: ", (team1, team2))
            if (status == team1):
                st.write(team1)
                selection = st.multiselect(f"{team1} - Players: ",
                                      names1)
                for player in selection:
                    st.write(players1[player])
            else:
                st.write(team2)
                selection = st.multiselect(f"{team2} - Players: ",
                                      names2)
                for player in selection:
                    st.write(players2[player])