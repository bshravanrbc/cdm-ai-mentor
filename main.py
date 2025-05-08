
import streamlit as st
from question_utils import list_mcq_files, load_questions_by_topic, evaluate_answers

st.set_page_config(page_title="Astromani Quiz", layout="centered")

# UI Tweaks
st.markdown("""
    <style>
        .block-container { padding-top: 1rem; }
        #MainMenu, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("🧠 Astromani AI Mentor Quiz (एस्ट्रोमणि एआई मेंटर प्रश्नोत्तरी)")

# Define your custom order manually
TOPIC_ORDER = [
    "भावेशों की स्थिति",
    "Introduction to Rashis (Signs)",
    "Introduction to Houses (Bhav)",
    "Planetary Friendships",
    "Career Analysis Basics",
    "House Karakas and Maran Karakas",
    "Good and Bad Health Indicators",
    "Intro to Planets - Sun",
    "Intro to Planets - Moon",
    "Intro to Planets - Mercury",
    "Intro to Planets - Venus",
    "Intro to Planets - Mars",
    "Intro to Planets - Jupiter",
    "Intro to Planets - Saturn",
    "Intro to Planets - Rahu",
    "Intro to Planets - Ketu",
    "Ascendant Lord in Different Houses",
    "Sun in Houses",
    "Moon in Houses",
    "Mercury in Houses",
    "Venus in Houses",
    "Mars in Houses",
    "Jupiter in Houses",
    "Saturn in Houses",
    "Rahu in Houses",
    "Ketu in Houses",
    "2nd Lord in Different Houses",
    "3rd Lord in Different Houses",
    "4th Lord in Different Houses",
    "5th Lord in Different Houses",
    "6th Lord in Different Houses",
    "7th Lord in Different Houses",
    "8th Lord in Different Houses",
    "9th Lord in Different Houses",
    "10th Lord in Different Houses",
    "11th Lord in Different Houses",
    "12th Lord in Different Houses",
]

# Load topics from your topic folder and order them
import os

available_files = os.listdir("mcqs/")
topics = [file.replace(".json", "") for file in available_files if file.endswith(".json")]
topics = [t for t in TOPIC_ORDER if t in topics]

topic = st.selectbox("Choose a topic (एक विषय चुनें)", topics)

num_questions = st.slider("How many questions? (कितने प्रश्न?)", 1, 20, 5)

if st.button("Generate Quiz", key="generate_quiz (प्रश्नोत्तरी शुरू करें)"):
    questions = load_questions_by_topic(topic, num_questions)
    st.session_state["questions"] = questions

if "questions" in st.session_state:
    questions = st.session_state["questions"]
    user_answers = []

    for i, q in enumerate(questions):
        st.markdown(f"**Q{i+1}: {q['question']}**")
        user_choice = st.radio(f"Choose your answer: (अपना उत्तर चुनें:)", q['options'], key=f"q{i}")
        user_answers.append(user_choice)

    if st.button("Submit", key="submit_quiz (प्रश्नोत्तरी सबमिट करें)"):
        results = evaluate_answers(questions, user_answers)
        st.write(f"### ✅ Score: {results['correct']} / {results['total']}")
        st.write(f"🟩 Correct: {results['correct']} | 🟥 Incorrect: {results['incorrect']}")
        for i, res in enumerate(results['details']):
            st.markdown(f"### Q{i+1}: {res['question']}")
            if res['user_answer'] == res['correct_answer']:
                st.success(f"✅ Correct: {res['correct_answer']}")
                st.markdown(f"🧠 Your Answer: {res['user_answer']}")
            else:
                st.error("❌ Incorrect Answer")
                st.markdown(f"✅ Correct: {res['correct_answer']}")
                st.markdown(f"🧠 Your Answer: ~~{res['user_answer']}~~")
            st.markdown(f"💡 Explanation: {res['explanation']}")
            st.markdown("---")
