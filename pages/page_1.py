import os
import tabula as tb
import streamlit as st
from io import StringIO
from pdf2image import convert_from_path
from pathlib import Path
import tempfile
import base64
import st_pages as stp
from voliboli_pdf_scraper.main import process_pdf
import voliboli_pdf_scraper.constants as constants
import altair as alt
import pandas as pd

stp.show_pages(
    [
        stp.Page("app.py", "Home", "🏠"),
        stp.Page("pages/page_1.py", "Upload & Visualize", "📄"),
        stp.Page("pages/page_2.py", "Select & Analyze", "🏆")
    ]
)

# metadata
STAT_DIRECTORY = 'stats'
DEBUG = False

# boundaries
TEAM1_UB = 180
TEAM1_LB = 340
TEAM2_UB = 425
TEAM2_LB = 580

@st.cache_data
def process_statistic(file, debug):
    return process_pdf(file, debug)

def show_pdf(file_path:str):
    """Show the PDF in Streamlit - That returns as html component"""
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)

st.set_page_config(page_title="Upload & Visualize", page_icon="🏐")
uploaded_files = st.file_uploader(label="Choose a PDF file", type=['pdf'], accept_multiple_files=True)
if uploaded_files is not None:
    for uploaded_file in uploaded_files:
        # Make temp file path from uploaded file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.name = uploaded_file.name
            #st.markdown("## Original PDF file")

            fp = Path(tmp_file.name)
            fp.write_bytes(uploaded_file.getvalue())
            #st.write(show_pdf(tmp_file.name)) # DISPLAYS PDF

            #if st.checkbox("Show/Hide PDF"):
            #    imgs = convert_from_path(tmp_file.name)
            #    st.image(imgs)

            file = tmp_file.name

            result, date, location, ateam1, ateam2, players1, players2 = process_statistic(file, debug=False)

            names1 = []
            for player in players1:
                names1.append(player[0])

            names2 = []
            for player in players2:
                names2.append(player[0])

            status = st.radio("Select Team: ", (ateam1, ateam2))
            if (status == ateam1):
                st.write(ateam1)
                selection = st.multiselect(f"{ateam1} - Players: ",
                                      names1)
                for sel in selection:
                    for player in players1:
                        if sel == player[0]:
                            #print(player)
                            barchart_vals = player[2:4] + player[5:10] + player[12:16] + player[17:]
                            #print(barchart_vals)
                            vote = player[1]
                            #print(vote)
                            wl = player[4]
                            #print(wl)
                            pos_rec = player[10]
                            #print(pos_rec)
                            exc_rec = player[11]
                            #print(exc_rec)
                            att_pts = player[16]
                            #print(att_pts)
                            data = pd.DataFrame(barchart_vals).T
                            data.columns = ["Total Points",
                                            "Break Points",
                                            "Total Serves",
                                            "Serve Errors",
                                            "Serve Points",
                                            "Total Receptions",
                                            "Reception Errors",
                                            "Total Attacks",
                                            "Attack Errors",
                                            "Attack Blocks",
                                            "Attack Points",
                                            "Block Points"]
                            '''
                            altair_chart = alt.Chart(data).mark_bar().encode(
                                x='Total Points'
                            )
                            st.altair_chart(altair_chart, use_container_width=True, theme="streamlit")
                            '''
            else:
                st.write(ateam2)
                selection = st.multiselect(f"{ateam2} - Players: ",
                                      names2)
                for sel in selection:
                    for player in players2:
                        if sel == player[0]:
                            st.write(player)