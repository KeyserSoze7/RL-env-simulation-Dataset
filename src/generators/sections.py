from utils.random_utils import uuid

SECTIONS = ["To Do", "In Progress", "Done"]

def generate(cursor, project_ids):
    sections = {}

    for pid in project_ids:
        sections[pid] = []
        for idx, name in enumerate(SECTIONS):
            sid = uuid()
            cursor.execute("""
                INSERT INTO section VALUES (?, ?, ?, ?, ?)
            """, (sid, pid, name, idx, 10 if name == "In Progress" else None))
            sections[pid].append(sid)

    return sections
