from assistant_api import get_mcqs_from_pdf
import re

def generate_questions(num):
# question_utils.py
    return get_mcqs_from_pdf("", num)

def clean_explanation(text):
    return re.sub(r'【.*?†.*?】', '', text).strip()

def evaluate_answers(questions, user_answers):
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