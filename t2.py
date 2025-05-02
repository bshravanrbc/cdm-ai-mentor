import openai
import time
import json
import re


ASSISTANT_ID = "asst_RE6z2OZAc0bIeD0cvUOwfeVS"
OPENAI_API_KEY = "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"
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_mcqs_from_pdf(prompt, num_questions=5):
    """Generate MCQs using the Assistant."""
    thread = client.beta.threads.create()

    # Send message
    user_message = f"Generate {num_questions} multiple choice questions based on this prompt:\n\n{prompt}"
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )

    # Run assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )

    # Wait for completion (max 30s)
    for _ in range(30):
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run.status == "completed":
            break
        elif run.status in ("failed", "cancelled", "expired"):
            print(f"❌ Run failed: {run.status}")
            return []
        time.sleep(1)
    else:
        print("❌ Timeout waiting for assistant run to complete.")
        return []

    # Get response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    text = messages.data[0].content[0].text.value
    return parse_json_from_message(text)


def evaluate_mcq_answers(questions, user_answers):
    """Send answers for evaluation and get feedback."""
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

    # Wait for evaluation completion
    for _ in range(30):
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run.status == "completed":
            break
        time.sleep(1)
    else:
        print("❌ Evaluation run timed out.")
        return "Evaluation failed."

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return messages.data[0].content[0].text.value


def parse_json_from_message(text):
    """Extract JSON list of MCQs from assistant reply."""
    print("\n🪵 RAW ASSISTANT RESPONSE:\n", text)

    try:
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception as e:
        print("❌ JSON parsing failed:", e)
    return []
