
import json
import random
from assistant_api import get_mcqs_from_pdf

# Load pre-generated questions from local JSON file
with open("full_astrology_mcqs.json", "r") as f:
    LOCAL_QUESTION_BANK = json.load(f)

def generate_questions_local(topic, num):
    """Return MCQs from local file based on topic."""
    if topic not in LOCAL_QUESTION_BANK:
        return []
    return random.sample(LOCAL_QUESTION_BANK[topic], min(num, len(LOCAL_QUESTION_BANK[topic])))

def generate_questions_ai(prompt, num):
    """Fetch MCQs from OpenAI Assistant based on topic."""
    return get_mcqs_from_pdf(prompt, num)

def evaluate_answers(questions, user_answers):
    import re

    def clean_explanation(text):
        return re.sub(r'【.*?†.*?】', '', text).strip()

    correct = 0
    incorrect = 0
    details = []

    for q, ua in zip(questions, user_answers):
        is_correct = ua == q['correct']
        if is_correct:
            correct += 1
        else:
            incorrect += 1

        details.append({
            "question": q['question'],
            "user_answer": ua,
            "correct_answer": q['correct'],
            "explanation": clean_explanation(q['explanation'])
        })

    return {
        "score": correct,
        "total": len(questions),
        "correct": correct,
        "incorrect": incorrect,
        "details": details
    }
