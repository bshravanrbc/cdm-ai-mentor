import streamlit as st
import os
import json
import random

from question_utils import load_questions_by_topic, evaluate_answers  # You must define these

# Set page config
st.set_page_config(page_title="ISDA CDM Mentor", layout="wide")

# Inject styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans&display=swap');
    .block-container { padding-top: 1rem; font-family: 'Noto Sans', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# Define labels
lbl = {
    "title": "🧠 ISDA CDM AI Mentor",
    "choose_topic": "Choose a CDM Topic",
    "num_questions": "How many questions?",
    "generate": "Generate Quiz",
    "submit": "Submit Quiz",
    "choose_answer": "Choose your answer:",
    "score": "Score",
    "correct": "Correct",
    "incorrect": "Incorrect",
    "your_answer": "Your Answer",
    "explanation": "Explanation",
    "concept_notes": "Concept Notes",
    "audio_explanation": "Audio Explanation",
    "question_number": "Question"
}

# Define topic list
TOPIC_ORDER = [
    "CDM Overview", "CDM Product Model", "CDM Event Model", "Contract Formation",  "PrimitiveEvent", "Trade",
    "WorkflowStep", "CDM Fields", "Regulatory Reporting", "Valuation", "CDM Objects"
]

# Title
st.markdown(f"<h3 style='font-size: 26px; color: #222;'>{lbl['title']}</h3>", unsafe_allow_html=True)

# Topic selector
selected_topic = st.selectbox(lbl["choose_topic"], TOPIC_ORDER)

# Show concept text
text_path = os.path.join("data", selected_topic + ".txt")
if os.path.exists(text_path):
    with open(text_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    lines = raw_text.strip().splitlines()
    styled_lines = []
    for line in lines:
        if line.strip().endswith(":"):
            styled_lines.append(f"<h4>{line.strip()}</h4>")
        elif line.strip().startswith("•"):
            styled_lines.append(f"<li>{line.strip()[1:].strip()}</li>")
        else:
            styled_lines.append(f"<p>{line.strip()}</p>")

    html_content = f"""
    <ul style="line-height: 1.7; font-size: 0.95rem;">{''.join(styled_lines)}</ul>
    """

with st.expander(f"📘 **{lbl['concept_notes'].upper()}**"):
    #st.markdown(f"### **{lbl['concept_notes']}**")
    st.markdown(html_content, unsafe_allow_html=True)

num_questions = st.slider(lbl["num_questions"], 1, 20, 5)

# Show Concept Notes
text_path = os.path.join("cdm-data", selected_topic + ".txt")
if os.path.exists(text_path):
    with open(text_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
    lines = raw_text.strip().splitlines()
    styled_lines = []
    for line in lines:
        if line.strip().endswith(":"):
            styled_lines.append(f"<h4>{line.strip()}</h4>")
        elif line.strip().startswith("•"):
            styled_lines.append(f"<li>{line.strip()[1:].strip()}</li>")
        else:
            styled_lines.append(f"<p>{line.strip()}</p>")
    html_content = f"<ul style='line-height: 1.6; font-size: 0.94rem;'>{''.join(styled_lines)}</ul>"
    with st.expander(f"📘 {lbl['concept_notes']}"):
        st.markdown(html_content, unsafe_allow_html=True)

# Play audio explanations
audio_path = os.path.join("audio", selected_topic + ".wav")
if os.path.exists(audio_path):
    #st.markdown("### 🎧 Audio Explanation:")
    st.markdown(f"<h3 style='font-size: 22px;'> {lbl['audio_explanation']}</h3>", unsafe_allow_html=True)
    with open(audio_path, "rb") as audio_file:
        st.audio(audio_file.read(), format="audio/wav")
else:
    st.info("🎧 No audio available for this topic.")

# Generate quiz
if st.button(lbl["generate"]):
    st.session_state["questions"] = load_questions_by_topic(selected_topic, num_questions, folder="cdm-mcqs")

# Display quiz
if "questions" in st.session_state:
    questions = st.session_state["questions"]
    user_answers = []

    for i, q in enumerate(questions):
        st.markdown(f"**{lbl['question_number']} {i+1}: {q['question']}**")
        user_choice = st.radio(lbl["choose_answer"], q["options"], key=f"q{i}")
        user_answers.append(user_choice)

    if st.button(lbl["submit"]):
        results = evaluate_answers(questions, user_answers)
        st.write(f"### ✅ {lbl['score']}: {results['correct']} / {results['total']}")
        st.write(f"🟩 {lbl['correct']}: {results['correct']} | 🟥 {lbl['incorrect']}: {results['incorrect']}")
        for i, res in enumerate(results["details"]):
            st.markdown(f"### {lbl['question_number']} {i+1}: {res['question']}")
            if res['user_answer'] == res['correct_answer']:
                st.success(f"✅ {lbl['correct']}: {res['correct_answer']}")
                st.markdown(f"🧠 {lbl['your_answer']}: {res['user_answer']}")
            else:
                st.error(f"❌ {lbl['incorrect']}")
                st.markdown(f"✅ {lbl['correct']}: {res['correct_answer']}")
                st.markdown(f"🧠 {lbl['your_answer']}: ~~{res['user_answer']}~~")
            st.markdown(f"💡 {lbl['explanation']}: {res['explanation']}")
            st.markdown("---")
