
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

st.title("🧠 Astromani AI Mentor Quiz")

# Topic list from files
topics = list_mcq_files()
if not topics:
    st.error("No quiz topics found. Please add MCQ JSON files to the 'mcqs/' folder.")
else:
    topic = st.selectbox("Choose Topic", topics)
    num_questions = st.slider("How many questions?", 1, 20, 5)

    if st.button("Generate Quiz", key="generate_quiz"):
        questions = load_questions_by_topic(topic, num_questions)
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
