import openai
import os
from dotenv import load_dotenv
import time
import re
import json

load_dotenv()

ASSISTANT_ID = "asst_RE6z2OZAc0bIeD0cvUOwfeVS"
OPENAI_API_KEY = "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"

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_mcqs_from_pdf(prompt, num_questions=5):
    """Generate MCQs using the Assistant"""
    
    # Create thread
    thread = client.beta.threads.create()

    # Add user message
   # user_message = f"Generate {num_questions} multiple choice questions based on this prompt:\n\n{prompt}"

    user_message = f"""
    Generate {num_questions} multiple choice questions based on this topic: "{prompt}".

    Return only a JSON array of dictionaries, no extra text. Each item must include:
    - "question": string
    - "options": list of 4 options
    - "correct": correct option
    - "explanation": brief explanation

    Respond ONLY with the JSON array. No introduction, no markdown, no formatting.
    """

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )

    # Run Assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )

    # Wait for completion
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Get response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    latest_message = messages.data[0]
    return parse_json_from_message(latest_message.content[0].text.value)


def evaluate_mcq_answers(questions, user_answers):
    """Send answers for evaluation and get feedback"""
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    thread = client.beta.threads.create()

    message = "Evaluate the following answers for a quiz:\n\n"
    for i, (q, ans) in enumerate(zip(questions, user_answers), 1):
        message += f"Question {i}: {q['question']}\n"
        message += f"User Answer = \"{ans}\"\n\n"

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )

    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return messages.data[0].content[0].text.value


def parse_json_from_message(text):
    import json, re
    #print("\n🪵 RAW ASSISTANT RESPONSE:\n", text)  # ✅ Add this

    try:
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception as e:
        print("❌ JSON parsing error:", e)
    return []


