import streamlit as st
from pdf2image import convert_from_path
from pathlib import Path
import tempfile
import base64
import st_pages as stp
from voliboli_pdf_scraper.main import process_pdf
import voliboli_pdf_scraper.constants as constants
import altair as alt
import pandas as pd
from streamlit.runtime.scriptrunner import RerunData,RerunException

stp.show_pages(
    [
        stp.Page("app.py", "Home", "🏠"),
        stp.Page("pages/page_1.py", "Upload & Visualize", "📄"),
        stp.Page("pages/page_2.py", "Select & Analyze", "🏆")
    ]
)

@st.cache_data
def process_statistic(file, debug):
    result, date, location, ateam1, ateam2, players1, players2 = process_pdf(file, debug)
    names1 = []
    for player in players1:
        names1.append(player[0])

    names2 = []
    for player in players2:
        names2.append(player[0])

    return result, date, location, ateam1, ateam2, players1, players2, names1, names2

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

            result, date, location, ateam1, ateam2, players1, players2, names1, names2 = process_statistic(file, debug=False)

            status = st.radio("Select Team: ", (ateam1, ateam2))
            if "selection1" not in st.session_state:
                st.session_state["selection1"] = []
            if "selection2" not in st.session_state:
                st.session_state["selection2"] = []

            # NOTE: Weird way of achieving for the multi-select widget to updateX
            # ############################################ DO NOT MODIFY #############################
            def update_selection(key, selection):
                st.session_state[key] = selection

            selection1 = st.session_state["selection1"]
            selection2 = st.session_state["selection2"]
            last_selection = st.session_state["selection1"] + st.session_state["selection2"]
            if status == ateam1:
                selection1 = st.multiselect(f"{ateam1} - Players: ", names1, default=st.session_state["selection1"], on_change=update_selection, args=("selection1", selection1))
                st.session_state["selection1"] = selection1
            else:
                selection2 = st.multiselect(f"{ateam2} - Players: ", names2, default=st.session_state["selection2"], on_change=update_selection, args=("selection2", selection2))
                st.session_state["selection2"] = selection2
            ###########################################################################################
            
            selection = selection1 + selection2

            for sel in selection:
                for player in players1:
                    if sel == player[0]:
                        barchart_vals = player[:1] + player[2:4] + player[5:10] + player[12:16] + player[17:]
                        vote = player[1]
                        wl = player[4]
                        pos_rec = player[10]
                        exc_rec = player[11]
                        att_pts = player[16]
                        data = pd.DataFrame(barchart_vals).T
                        data.columns = ["Player",
                                        "Total Points",
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
                        source = pd.DataFrame({"Category":list("AAABBBCCC"),
                                            "Group":list("xyzxyzxyz"),
                                            "Value":[0.1, 0.6, 0.9, 0.7, 0.2, 1.1, 0.6, 0.1, 0.2]})

                        chart = alt.Chart(source).mark_bar().encode(
                            x="Category:N",
                            y="Value:Q",
                            xOffset="Group:N",
                            color="Group:N"
                        )

                        st.altair_chart(chart, use_container_width=True, theme="streamlit")