import random
from utils.random_utils import uuid, random_date
from utils.llm_llamacpp import llm_generate

SENTIMENTS = ["neutral", "positive", "blocking"]

PROMPTS = {
    "neutral": "Write a short neutral task update comment.",
    "positive": "Write a short positive comment indicating progress or completion.",
    "blocking": "Write a short comment describing a blocker or issue.",
}

def generate(cursor, task_ids, user_ids):
    for task_id in task_ids:
        for _ in range(random.randint(0, 3)):
            sentiment = random.choices(
                SENTIMENTS, weights=[0.6, 0.2, 0.2]
            )[0]

            prompt = PROMPTS[sentiment]
            body = llm_generate(prompt, max_tokens=32)

            cursor.execute(
                """
                INSERT INTO comment (
                    comment_id, task_id, user_id, body, sentiment, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    uuid(),
                    task_id,
                    random.choice(user_ids),
                    body.strip(),
                    sentiment,
                    random_date(60),
                ),
            )
