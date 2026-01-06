import random
from utils.random_utils import uuid, random_date

FILES = ["spec.pdf", "mockup.fig", "logs.txt", "design.png"]

def generate(cursor, task_ids):
    for tid in task_ids:
        if random.random() < 0.25:
            cursor.execute("""
                INSERT INTO attachment VALUES (?, ?, ?, ?, ?, ?)
            """, (
                uuid(),
                tid,
                random.choice(FILES),
                "file",
                random.randint(100, 5000),
                random_date(30)
            ))
