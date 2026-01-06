import sqlite3

from generators import (
    users,
    projects,
    sections,
    tasks,
    subtasks,
    comments,
    custom_fields,
    tags,
    attachments,
)

DB = "output/asana_simulation.sqlite"


def main():
    print(" Connecting to SQLite database...")
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()


    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL;")

  
    workspace_id = "workspace-001"
    print("Creating workspace...")

    cursor.execute(
        """
        INSERT OR IGNORE INTO workspace (
            workspace_id, name, domain, created_at
        )
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """,
        (workspace_id, "Acme Corporation", "acme.com"),
    )
    conn.commit()
    print(" Workspace ready")


    TEAM_DEFS = [
        "Platform",
        "Backend",
        "Frontend",
        "Data",
        "ML",
        "DevOps",
        "Security",
        "Product",
        "Design",
        "QA",
        "Mobile",
        "Infra",
    ]

    team_ids = []

    print(" Creating teams...")
    for name in TEAM_DEFS:
        team_id = f"team-{name.lower()}"
        cursor.execute(
            """
            INSERT OR IGNORE INTO team (
                team_id, workspace_id, name, type
            )
            VALUES (?, ?, ?, ?)
            """,
            (team_id, workspace_id, name, "engineering"),
        )
        team_ids.append(team_id)

    conn.commit()
    print(f" Created {len(team_ids)} teams")

   
    USERS_PER_TEAM = 400  # 12 × 400 = 4,800 users

    print(" Generating users...")
    user_ids = users.generate(
        cursor,
        workspace_id,
        team_ids,
        users_per_team=USERS_PER_TEAM,
    )
    conn.commit()
    print(f" Users committed: {len(user_ids)}")


    print(" Generating projects...")
    project_ids = projects.generate(cursor, team_ids)
    conn.commit()
    print(f" Projects committed: {len(project_ids)}")

 
    print("Generating sections...")
    section_map = sections.generate(cursor, project_ids)
    conn.commit()
    print(" Sections committed")


    print("Generating tasks (LLM-based, slow but realistic)...")
    task_ids = []

    total_projects = len(project_ids)

    for idx, project_id in enumerate(project_ids, start=1):
        print(f"\n Project {idx}/{total_projects}: {project_id}")

        new_tasks = tasks.generate(
            cursor,
            [project_id],
            section_map,
            user_ids,
        )

        task_ids.extend(new_tasks)

        # Critical: commit after each project
        conn.commit()

        print(f" Committed {len(new_tasks)} tasks")
        print(f"Total tasks so far: {len(task_ids)}")


    print("\nGenerating subtasks...")
    subtasks.generate(cursor, task_ids)
    conn.commit()
    print(" Subtasks committed")


    print(" Generating comments...")
    comments.generate(cursor, task_ids, user_ids)
    conn.commit()
    print(" Comments committed")

  
    print("Generating custom fields...")
    custom_fields.generate(cursor, workspace_id, task_ids)
    conn.commit()
    print(" Custom fields committed")

  
    print("Generating tags...")
    tags.generate(cursor, workspace_id, task_ids)
    conn.commit()
    print(" Tags committed")


    print("Generating attachments...")
    attachments.generate(cursor, task_ids)
    conn.commit()
    print(" Attachments committed")

  
    conn.close()
    print("\nDONE — enterprise-scale dataset generated successfully!")


if __name__ == "__main__":
    main()
