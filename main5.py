import streamlit as st
import os
from question_utils import load_questions_by_topic, evaluate_answers

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari&family=Hind&family=Karma&display=swap');

    .block-container {
        font-family: 'Noto Sans Devanagari', 'Hind', 'Karma', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        .block-container {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Language selector
LANGUAGES = ["English", "Hindi"]
language = st.selectbox("Language (भाषा चुनें)", LANGUAGES)

# Labels for both languages
LABELS = {
    "English": {
        "title": "🧠 Astromani AI Mentor Quiz",
        "choose_topic": "Choose a topic",
        "num_questions": "How many questions?",
        "generate": "Generate Quiz",
        "submit": "Submit Quiz",
        "choose_answer": "Choose your answer:",
        "score": "Score",
        "correct": "Correct",
        "incorrect": "Incorrect",
        "your_answer": "Your Answer",
        "explanation": "Explanation",
        "question_number": "Question",
        "concept_notes": "Concept Notes",
        "audio_explanation": "Audio Explanation"
    },
    "Hindi": {
        "title": "🧠 एस्ट्रोमणि एआई मेंटर प्रश्नोत्तरी",
        "choose_topic": "एक विषय चुनें",
        "num_questions": "कितने प्रश्न?",
        "generate": "प्रश्नोत्तरी शुरू करें",
        "submit": "प्रश्नोत्तरी प्रस्तुत करें",
        "choose_answer": "अपना उत्तर चुनें:",
        "score": "अंक",
        "correct": "सही",
        "incorrect": "गलत",
        "your_answer": "आपका उत्तर",
        "explanation": "व्याख्या",
        "question_number": "प्रश्न क्रमांक",
        "concept_notes": "ज़रूरी बातें",
        "audio_explanation": "ऑडियो व्याख्या"
    }
}

lbl = LABELS[language]
folder = "mcqs" if language == "English" else "mcqs-hindi"

TOPIC_ORDER_ENGLISH = [
    "Introduction to Rashis (Signs)", "Introduction to Houses (Bhav)",
    "Ascendant Lord in Different Houses", "Sun in Houses", "Moon in Houses",
    "Mercury in Houses", "Venus in Houses", "Mars in Houses", "Jupiter in Houses",
    "Saturn in Houses", "Rahu in Houses", "Ketu in Houses",
    "2nd Lord in Different Houses", "3rd Lord in Different Houses", "4th Lord in Different Houses",
    "5th Lord in Different Houses", "6th Lord in Different Houses", "7th Lord in Different Houses",
    "8th Lord in Different Houses", "9th Lord in Different Houses", "10th Lord in Different Houses",
    "11th Lord in Different Houses", "12th Lord in Different Houses", "Career Analysis"
]

TOPIC_ORDER_HINDI = [
    "भावों का परिचय", "राशियों का परिचय", "भावेशों की स्थिति", 
    "लग्नेश विभिन्न भावों में", "सूर्य विभिन्न भावों में", "चंद्रमा विभिन्न भावों में",
    "बुध विभिन्न भावों में", "शुक्र विभिन्न भावों में", "मंगल विभिन्न भावों में", "बृहस्पति विभिन्न भावों में",
    "शनि विभिन्न भावों में", "राहु विभिन्न भावों में", "केतु विभिन्न भावों में",
    "द्वितीय भावेश", "तृतीय भावेश", "चतुर्थ भावेश", "पंचम भावेश", "षष्ठ भावेश",
    "सप्तम भावेश", "अष्टम भावेश", "नवम भावेश", "दशम भावेश", "एकादश भावेश", "द्वादश भावेश",
    "कैरियर विश्लेषण"
]

TOPIC_ORDER = TOPIC_ORDER_ENGLISH if language == "English" else TOPIC_ORDER_HINDI

st.markdown(f"<h3 style='font-size: 24px;'> {lbl['title']}</h3>", unsafe_allow_html=True)

# Load topic files based on language
available_files = os.listdir(folder)
topics = [f.replace(".json", "") for f in available_files if f.endswith(".json")]
topics = [t for t in TOPIC_ORDER if t in topics]

selected_topic = st.selectbox(lbl["choose_topic"], topics)

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

# Play audio explanations
audio_path = os.path.join("audio", selected_topic + ".wav")
if os.path.exists(audio_path):
    #st.markdown("### 🎧 Audio Explanation:")
    st.markdown(f"<h3 style='font-size: 22px;'> {lbl['audio_explanation']}</h3>", unsafe_allow_html=True)
    with open(audio_path, "rb") as audio_file:
        st.audio(audio_file.read(), format="audio/wav")
else:
    st.info("🎧 No audio available for this topic.")

num_questions = st.slider(lbl["num_questions"], 1, 20, 5)
if st.button(lbl["generate"]):
    st.session_state["questions"] = load_questions_by_topic(selected_topic, num_questions, folder)
    st.text(f"Loading from: {folder}/{selected_topic}.json")
    print(f"Loading from: {folder}/{selected_topic}.json")

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
        for i, res in enumerate(results['details']):
            st.markdown(f"**{lbl['question_number']} {i+1}: {q['question']}**")
            if res['user_answer'] == res['correct_answer']:
                st.success(f"✅ {lbl['correct']}: {res['correct_answer']}")
                st.markdown(f"🧠 {lbl['your_answer']}: {res['user_answer']}")
            else:
                st.error(f"❌ {lbl['incorrect']}")
                st.markdown(f"✅ {lbl['correct']}: {res['correct_answer']}")
                st.markdown(f"🧠 {lbl['your_answer']}: ~~{res['user_answer']}~~")
            st.markdown(f"💡 {lbl['explanation']}: {res['explanation']}")
            st.markdown("---")
