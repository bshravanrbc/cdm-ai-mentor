import openai

API_KEY = "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"  # your full key
ASSISTANT_ID = "asst_RE6z2OZAc0bIeD0cvUOwfeVS"

client = openai.OpenAI(api_key=API_KEY)

def test():
    thread = client.beta.threads.create()

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Generate 1 multiple choice question about Sun in astrology houses."
    )

    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)

    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    msg = client.beta.threads.messages.list(thread_id=thread.id)
    print(msg.data[0].content[0].text.value)

test()
