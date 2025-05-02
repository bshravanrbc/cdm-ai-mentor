import streamlit as st
from question_utils3 import generate_questions, evaluate_answers
import streamlit as st
from PIL import Image
import base64
from io import BytesIO

# Set page config
st.set_page_config(page_title="Asttromani Quiz", layout="centered")

# Convert logo to base64
def get_image_base64(img_path):
    img = Image.open(img_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

logo_base64 = get_image_base64("Asttrolok Logo.png")  # ensure this matches your actual filename

# Inject CSS and logo header
st.markdown(f"""
    <style>
        .block-container {{ padding-top: 1rem; }}
        #MainMenu, footer {{visibility: hidden;}}
        .logo-container {{
            display: flex;
            align-items: center;
            gap: 30px;
            margin-bottom: -10px;
        }}
        .logo-img {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
        }}
        .logo-title {{
            font-size: 1.6rem;
            font-weight: 600;
            margin: 0;
        }}
    </style>

    <div class="logo-container">
        <img src="data:image/png;base64,{logo_base64}" class="logo-img">
        <p class="logo-title">Astromani AI Mentor Quiz</p>
    </div>
""", unsafe_allow_html=True)

#st.title("Astromani AI Mentor Quiz")
num_questions = st.slider("How many questions?", 1, 10)

if st.button("Generate Quiz"):
    questions = generate_questions(num_questions)
    st.session_state['questions'] = questions
    #st.write("DEBUG - Questions returned:", questions)  # ✅ ADD THIS
 
if 'questions' in st.session_state:
    user_answers = []
    for i, q in enumerate(st.session_state['questions']):
        st.markdown(f"**Q{i+1}: {q['question']}**")
        user_answers.append(st.radio("Choose an option", q['options'], key=f"q{i}"))

    if st.button("Submit"):
        results = evaluate_answers(st.session_state['questions'], user_answers)
        st.write(f"**Score: {results['score']} / {results['total']}**")
        st.write(f"✅ Correct: {results['correct']} | ❌ Incorrect: {results['incorrect']}")
        
        for i, res in enumerate(results['details']):
            st.markdown(f"**Q{i+1}: {res['question']}**")
            st.markdown(f"Your answer: {res['user_answer']}")
            st.markdown(f"Correct answer: {res['correct_answer']}")
            st.markdown(f"Explanation: {res['explanation']}")
            st.markdown("---")
