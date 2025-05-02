
import streamlit as st
from question_utils3 import generate_questions_local, generate_questions_ai, evaluate_answers

st.set_page_config(page_title="Astromani Quiz", layout="centered")
import os

def list_mcq_files(folder="mcqs"):
    files = [f for f in os.listdir(folder) if f.endswith(".json")]
    return sorted(f.replace(".json", "") for f in files)

import json

def load_questions_by_topic(topic, folder="mcqs", num=5):
    try:
        with open(f"{folder}/{topic}.json", "r") as f:
            questions = json.load(f)
            return random.sample(questions, min(num, len(questions)))
    except Exception as e:
        print("Error loading questions:", e)
        return []

# UI Tweaks
st.markdown("""
    <style>
        .block-container { padding-top: 1rem; }
        #MainMenu, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("🧠 Astromani AI Mentor Quiz")

# Mode and topic selection
mode = st.radio("Select Quiz Mode", ["Local (faster)", "AI (slower)"])
topics = [
    "Sun in Houses", "Moon in Houses", "Mercury in Houses", "Venus in Houses", 
    "Mars in Houses", "Jupiter in Houses", "Saturn in Houses", "Rahu in Houses", "Ketu in Houses"
]
topic = st.selectbox("Choose Topic", topics)
num_questions = st.slider("How many questions?", 1, 5, 3)

if st.button("Generate Quiz", key="generate_quiz"):
    if mode.startswith("Local"):
        questions = generate_questions_local(topic, num_questions)
    else:
        questions = generate_questions_ai(topic, num_questions)
    st.session_state["questions"] = questions

if "questions" in st.session_state:
    questions = st.session_state["questions"]
    user_answers = []

    for i, q in enumerate(questions):
        st.markdown(f"**Q{i+1}: {q['question']}**")
        user_choice = st.radio(f"Choose your answer:", q['options'], key=f"q{i}")
        user_answers.append(user_choice)

    if st.button("Submit", key="submit_quiz"):
        results = evaluate_answers(questions, user_answers)
        st.write(f"### ✅ Score: {results['correct']} / {results['total']}")
        st.write(f"🟩 Correct: {results['correct']} | 🟥 Incorrect: {results['incorrect']}")
        for i, res in enumerate(results['details']):
            st.markdown(f"**Q{i+1}: {res['question']}**")
            st.markdown(f"✅ Correct: {res['correct_answer']}")
            st.markdown(f"🧠 Your Answer: {res['user_answer']}")
            st.markdown(f"💡 Explanation: {res['explanation']}")
            st.markdown("---")
