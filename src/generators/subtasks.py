import random
from utils.random_utils import uuid, random_date

def generate(cursor, task_ids):
    for tid in task_ids:
        if random.random() < 0.4:
            n = random.randint(2, 5)
            for _ in range(n):
                cursor.execute("""
                    INSERT INTO subtask VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    uuid(),
                    tid,
                    "Subtask",
                    random.randint(1, 4),
                    "todo",
                    random_date(100),
                    None
                ))
