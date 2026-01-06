import random
from utils.random_utils import uuid, random_date
from datetime import timedelta

PROJECT_TYPES = ["feature", "bugfix", "campaign", "operations"]

def generate(cursor, team_ids):
    projects = []

    for team_id in team_ids:
        for _ in range(random.randint(3, 6)):
            created = random_date(180)
            project = (
                uuid(),
                team_id,
                f"Project {random.randint(1000,9999)}",
                random.choice(PROJECT_TYPES),
                random.randint(1, 5),
                created.date(),
                (created + timedelta(days=random.randint(30, 120))).date(),
                created
            )

            cursor.execute("""
                INSERT INTO project VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, project)

            projects.append(project[0])

    return projects
