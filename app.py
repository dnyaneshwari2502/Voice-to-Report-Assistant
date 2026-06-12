import whisper
import tempfile
import streamlit as st
import google.generativeai as genai
import imageio_ffmpeg
import os
import re

os.environ["PATH"] += os.pathsep + os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())

from gmail_service import send_email
from dotenv import load_dotenv
from db import save_report, get_reports
from audiorecorder import audiorecorder

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

gemini_model = genai.GenerativeModel("gemini-2.5-flash")

model = whisper.load_model("base")

st.set_page_config(page_title="Voice to Report Assistant", layout="centered")

st.title("Voice to Report Assistant")

st.info(
    """
    This is a personal portfolio project created for learning and demonstration purposes.
    The workflow, data fields, and examples used in this application are fictional and do not represent any employer, client, or proprietary business process.
    """
)

st.write("Record a voice note and enter the recipient email.")

recipient_email = st.text_input("Recipient Email")

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

st.subheader("Record Voice Note")

audio = audiorecorder("Start Recording", "Stop Recording")

if len(audio) > 0:
    st.audio(audio.export().read(), format="audio/wav")
    st.success("Voice note recorded successfully.")

#Transcript Generation Section

if st.button("Generate Transcript"):
    if not recipient_email:
        st.error("Please enter recipient email.")
    elif not is_valid_email(recipient_email):
        st.error("Please enter a valid email address.")
    elif len(audio) == 0:
        st.error("Please record a voice note.")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            audio.export(tmp_file.name, format="wav")
            audio_path = tmp_file.name

        with st.spinner("Transcribing audio..."):
            result = model.transcribe(audio_path)

        st.session_state["transcript"] = result["text"]

if "transcript" in st.session_state:

    edited_text = st.text_area(
        "Review / Edit Transcript",
        value=st.session_state["transcript"],
        height=200
    )

    st.session_state["transcript"] = edited_text

    if st.button("Generate Summary"):

        prompt = f"""
        Convert the following oil field update into a professional field report.

        Format exactly as:

        ## Work Completed
        - item

        ## Issues Identified
        - item

        ## Safety Observations
        - item

        ## Next Steps
        - item

        Use bullet points.
        Do not write any introduction or conclusion.

        Update:
        {edited_text}
        """

        response = gemini_model.generate_content(prompt)

        st.session_state["summary"] = response.text

#Helper Function

def extract_section(summary, section_name):
    lines = summary.splitlines()
    capture = False
    section_lines = []

    for line in lines:
        clean_line = line.strip()

        if clean_line.startswith("##"):
            if section_name.lower() in clean_line.lower():
                capture = True
                continue
            elif capture:
                break

        if capture and clean_line:
            section_lines.append(clean_line.replace("- ", ""))

    return " | ".join(section_lines) if section_lines else "Not Mentioned"

#Summary Section
if "summary" in st.session_state:

    st.subheader("AI Generated Summary")
    
    st.markdown(st.session_state["summary"])

    if st.button("Send Report"):

        send_email(
            recipient_email=recipient_email,
            manager_email="dnyanurakshe123@gmail.com",
            subject="Daily Field Report",
            body=st.session_state["summary"]
        )

        save_report(
            recipient_email,
            st.session_state["transcript"],
            st.session_state["summary"],
            extract_section(st.session_state["summary"], "Work Completed"),
            extract_section(st.session_state["summary"], "Issues Identified"),
            extract_section(st.session_state["summary"], "Safety Observations"),
            extract_section(st.session_state["summary"], "Next Steps")
        )


        st.session_state.pop("transcript", None)
        st.session_state.pop("summary", None)

        st.success("Report sent successfully!")


#History Section

st.divider()

st.subheader("Report History")

if "show_history" not in st.session_state:
    st.session_state["show_history"] = False

col1, col2 = st.columns(2)

with col1:
    if st.button("Load History"):
        st.session_state["show_history"] = True

with col2:
    if st.button("Close History"):
        st.session_state["show_history"] = False

if st.session_state["show_history"]:

    reports = get_reports()

    history_data = []

    for report in reports:
        history_data.append({
            "Report ID": report[0],
            "Recipient": report[1],
            "Created": report[2].date(),
            "Work Completed": report[3],
            "Issues": report[4],
            "Safety Observations": report[5],
            "Next Steps": report[6]
        })

    st.dataframe(history_data, use_container_width=True)


#connect with me section

st.sidebar.markdown("## Connect With Me")

st.sidebar.markdown(
    "[LinkedIn](https://www.linkedin.com/in/dnyaneshwari-rakshe1325)"
)

st.sidebar.markdown(
    "📧 dnyaneshwarirakshe133@gmail.com"
)

st.sidebar.info(
    """
    Email functionality in this demo is currently configured using my personal Gmail API credentials.

    If you are interested in using, extending, or integrating this project for your own workflow or organization, please feel free to reach out.
    """
)