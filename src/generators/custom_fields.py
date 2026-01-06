from utils.random_utils import uuid
import random

FIELDS = [
    ("Priority", "enum"),
    ("Effort", "number"),
    ("Blocked", "boolean"),
    ("Sprint", "text")
]

def generate(cursor, workspace_id, task_ids):
    field_ids = []

    for name, ftype in FIELDS:
        fid = uuid()
        cursor.execute("""
            INSERT INTO custom_field VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (fid, workspace_id, name, ftype))
        field_ids.append((fid, ftype))

    for tid in task_ids:
        for fid, ftype in field_ids:
            if random.random() < 0.5:
                value = (
                    str(random.randint(1, 8)) if ftype == "number"
                    else random.choice(["true", "false"]) if ftype == "boolean"
                    else random.choice(["Low", "Medium", "High"])
                )
                cursor.execute("""
                    INSERT INTO custom_field_value VALUES (?, ?, ?, ?)
                """, (uuid(), fid, tid, value))
