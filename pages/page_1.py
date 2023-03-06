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
import streamlit_authenticator as stauth

stp.show_pages(
    [
        stp.Page("app.py", "Home", "🏠"),
        stp.Page("pages/page_1.py", "Upload & Visualize", "📄"),
        stp.Page("pages/page_2.py", "Select & Analyze", "🏆"),
        stp.Page("pages/page_3.py", "About", "💡")
    ]
)

@st.cache_data
def processing_statistics(file, debug):
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

            result, date, location, ateam1, ateam2, players1, players2, names1, names2 = processing_statistics(file, debug=False)
            fplayers1 = []
            for p1 in players1:
                fp1 = []
                for e in p1:
                    if e == '.':
                        e = '0'
                    out1 = e.replace('%', '').replace('(', '').replace(')', '').strip()
                    fp1.append(out1)
                fplayers1.append(fp1)

            fplayers2 = []
            for p2 in players2:
                fp2 = []
                for e in p2:
                    if e == '.':
                        e = '0'
                    out2 = e.replace('%', '').replace('(', '').replace(')', '').strip()
                    fp2.append(out2)
                fplayers2.append(fp2)

            status = st.radio("Select Team: ", (ateam1, ateam2))
            if ("selection1_" + tmp_file.name) not in st.session_state:
                st.session_state["selection1_" + tmp_file.name] = []
            if ("selection2_" + tmp_file.name) not in st.session_state:
                st.session_state["selection2_" + tmp_file.name] = []

            # NOTE: Weird way of achieving for the multi-select widget to updateX
            # ############################################ DO NOT MODIFY #############################
            def update_selection(key, selection):
                st.session_state[key] = selection

            selection1 = st.session_state["selection1_" + tmp_file.name]
            selection2 = st.session_state["selection2_" + tmp_file.name]
            last_selection = st.session_state["selection1_" + tmp_file.name] + st.session_state["selection2_" + tmp_file.name]
            if status == ateam1:
                selection1 = st.multiselect(f"{ateam1} - Players: ", names1, default=st.session_state["selection1_" + tmp_file.name], on_change=update_selection, args=("selection1_" + tmp_file.name, selection1))
                st.session_state["selection1_" + tmp_file.name] = selection1
            else:
                selection2 = st.multiselect(f"{ateam2} - Players: ", names2, default=st.session_state["selection2_" + tmp_file.name], on_change=update_selection, args=("selection2_" + tmp_file.name, selection2))
                st.session_state["selection2_" + tmp_file.name] = selection2
            ###########################################################################################
            
            selection = selection1 + selection2
            num_players = len(selection)

            votes = []
            total_points = []
            break_points = []
            wl_points = []
            total_serves = []
            serve_errors = []
            serve_points = []
            total_receptions = []
            error_receptions = []
            pos_receptions = []
            exc_receptions = []
            total_attacks = []
            error_attacks = []
            block_attacks = []
            pts_attacks = []
            perc_attacks = []
            blocks = []

            fplayers = fplayers1 + fplayers2
            for sel in selection:
                for player in fplayers:
                    if sel == player[0]:
                        votes.append(player[1])
                        total_points.append(player[2])
                        break_points.append(player[3])
                        wl_points.append(player[4])
                        total_serves.append(player[5])
                        serve_errors.append(player[6])
                        serve_points.append(player[7])
                        total_receptions.append(player[8])
                        error_receptions.append(player[9])
                        pos_receptions.append(str(int(player[10])/100))
                        exc_receptions.append(str(int(player[11])/100))
                        total_attacks.append(player[12])
                        error_attacks.append(player[13])
                        block_attacks.append(player[14])
                        pts_attacks.append(player[15])
                        perc_attacks.append(str(int(player[16])/100))
                        blocks.append(player[17])
            
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
                       "Block Points"]
            
            categories1 = []
            for col in columns1:
                for _ in range(num_players):
                    categories1.append(col)
            players_seq1 = selection * len(columns1)
            values1 = total_points + break_points + total_serves + serve_errors + \
                        serve_points + total_receptions + error_receptions + total_attacks + \
                        error_attacks + block_attacks + pts_attacks + block_attacks
            source1 = pd.DataFrame({"Category":list(categories1),
                                "Group":list(players_seq1),
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
                for _ in range(num_players):
                    categories2.append(col)
            values2 = pos_receptions + exc_receptions + perc_attacks
            players_seq2 = selection * len(columns2)
            source2 = pd.DataFrame({"Category":list(categories2),
                                "Group":list(players_seq2),
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
                for _ in range(num_players):
                    categories3.append(col)
            values3 = wl_points
            players_seq3 = selection * len(columns3)
            source3 = pd.DataFrame({"Category":list(categories3),
                                "Group":list(players_seq3),
                                "Value":values3})

            chart3 = alt.Chart(source3).mark_bar().encode(
                x="Category:N",
                y="Value:Q",
                color="Group:N",
                xOffset="Group:N",
            )

            st.altair_chart(chart3, use_container_width=True, theme="streamlit")