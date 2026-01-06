from utils.random_utils import uuid
import random

TAGS = ["bug", "urgent", "frontend", "backend", "tech-debt"]

def generate(cursor, workspace_id, task_ids):
    tag_ids = {}

    for tag in TAGS:
        tid = uuid()
        cursor.execute("""
            INSERT INTO tag VALUES (?, ?, ?)
        """, (tid, workspace_id, tag))
        tag_ids[tag] = tid

    for task_id in task_ids:
        for tag in random.sample(TAGS, random.randint(0, 2)):
            cursor.execute("""
                INSERT INTO task_tag VALUES (?, ?)
            """, (task_id, tag_ids[tag]))
