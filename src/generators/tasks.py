import random
from datetime import timedelta
from pathlib import Path

from utils.random_utils import uuid, random_date
from utils.llm_llamacpp import llm_generate


FAST_MODE = True       # SET TO False FOR FULL RUN
COMMIT_EVERY = 5       # commiting every N tasks

PROMPTS_DIR = Path("src/prompts")
TASK_TITLE_PROMPT = PROMPTS_DIR / "task_title.txt"
TASK_DESC_PROMPT = PROMPTS_DIR / "task_description.txt"



def generate_task_text(meta):
    title_prompt = TASK_TITLE_PROMPT.read_text().format(
        team=meta["team"],
        project_type=meta["project_type"],
        component=meta["component"],
        complexity=meta["complexity"],
    )

    title = llm_generate(title_prompt, max_tokens=32)

    verbosity = random.choices(
        ["short", "medium", "long"],
        weights=[0.2, 0.5, 0.3],
    )[0]

    desc_prompt = TASK_DESC_PROMPT.read_text().format(
        title=title,
        verbosity=verbosity,
    )

    description = llm_generate(desc_prompt, max_tokens=128)

    # Allowing empty descriptions sometimes
    if random.random() < 0.2:
        description = None

    return title.strip(), description.strip() if description else None



def generate(cursor, project_ids, section_map, user_ids):
    task_ids = []

    for project_id in project_ids:
        n_tasks = (
            random.randint(3, 5)
            if FAST_MODE
            else random.randint(50, 150)
        )

        print(f"    Generating {n_tasks} tasks for project {project_id}")

        for task_idx in range(1, n_tasks + 1):
            created_at = random_date(180)
            complexity = random.randint(1, 10)
            priority = random.randint(1, 5)

            completed = random.random() < 0.65
            completed_at = (
                created_at + timedelta(days=random.randint(2, 14))
                if completed
                else None
            )

            # Due date logic
            r = random.random()
            if r < 0.10:
                due_date = None
            elif r < 0.35:
                due_date = created_at + timedelta(days=random.randint(1, 7))
            elif r < 0.75:
                due_date = created_at + timedelta(days=random.randint(8, 30))
            else:
                due_date = created_at + timedelta(days=random.randint(31, 90))

            assignee_id = (
                random.choice(user_ids)
                if random.random() > 0.15
                else None
            )

            section_id = random.choice(section_map[project_id])
            status = random.choice(["todo", "in_progress", "done"])

            # LLM call
            title, description = generate_task_text(
                {
                    "team": "engineering",
                    "project_type": "feature",
                    "component": "core",
                    "complexity": complexity,
                }
            )

            task_id = uuid()

            cursor.execute(
                """
                INSERT INTO task (
                    task_id,
                    project_id,
                    section_id,
                    assignee_id,
                    name,
                    description,
                    priority,
                    complexity,
                    status,
                    due_date,
                    created_at,
                    completed_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    task_id,
                    project_id,
                    section_id,
                    assignee_id,
                    title,
                    description,
                    priority,
                    complexity,
                    status,
                    due_date.date() if due_date else None,
                    created_at,
                    completed_at,
                ),
            )

            task_ids.append(task_id)

            #  LIVE progress
            print(f"      Task {task_idx}/{n_tasks}: {title[:60]}")

            # Periodic commit
            if task_idx % COMMIT_EVERY == 0:
                cursor.connection.commit()

    return task_ids
