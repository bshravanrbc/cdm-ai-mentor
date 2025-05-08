
import json
import os
import random

MCQ_FOLDER = "mcqs"

def list_mcq_files():
    """List all available topics based on JSON filenames."""
    try:
        files = [f for f in os.listdir(MCQ_FOLDER) if f.endswith(".json")]
        return sorted(f.replace(".json", "") for f in files)
    except FileNotFoundError:
        return []

def load_questions_by_topic(topic, num, folder="mcqs"):
    """Load MCQs from a specific topic file."""
    try:
        with open(f"{MCQ_FOLDER}/{topic}.json", "r", encoding="utf-8") as f:
            questions = json.load(f)
            print("Loading:", topic)
            print("Folder:", folder)
            print("Path:", os.path.join(folder, topic + ".json"))
            return random.sample(questions, min(num, len(questions)))
    except Exception as e:
        print("Error loading questions:", e)
        return []
    
def load_questions_by_topic1(topic, num_questions=5, folder="mcqs"):
    path = os.path.join(folder, topic + ".json")
    with open(path, "r", encoding="utf-8") as f:  # ✅ Ensure UTF-8 here
        questions = json.load(f)
    return random.sample(questions, min(num_questions, len(questions)))

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
