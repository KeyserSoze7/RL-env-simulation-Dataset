CREATE TABLE workspace (
    workspace_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
);


CREATE TABLE team (
    team_id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    name TEXT NOT NULL,
    type TEXT CHECK (type IN ('engineering', 'marketing', 'operations')),
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (workspace_id) REFERENCES workspace(workspace_id)
);


CREATE TABLE user (
    user_id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    role TEXT CHECK (role IN ('IC', 'Lead', 'Manager', 'Director')),
    capacity INTEGER,              -- tasks per sprint/day
    efficiency REAL,               -- behavioral parameter (RL)
    burnout REAL,                  -- behavioral parameter (RL)
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (workspace_id) REFERENCES workspace(workspace_id)
);


CREATE TABLE team_membership (
    team_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    joined_at TIMESTAMP NOT NULL,
    PRIMARY KEY (team_id, user_id),
    FOREIGN KEY (team_id) REFERENCES team(team_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);


CREATE TABLE project (
    project_id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    name TEXT NOT NULL,
    type TEXT CHECK (type IN ('feature', 'bugfix', 'campaign', 'operations')),
    priority INTEGER CHECK (priority BETWEEN 1 AND 5),
    start_date DATE,
    due_date DATE,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (team_id) REFERENCES team(team_id)
);


CREATE TABLE section (
    section_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    position INTEGER,
    wip_limit INTEGER,
    FOREIGN KEY (project_id) REFERENCES project(project_id)
);


CREATE TABLE task (
    task_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    section_id TEXT NOT NULL,
    assignee_id TEXT,
    name TEXT NOT NULL,
    description TEXT,
    priority INTEGER CHECK (priority BETWEEN 1 AND 5),
    complexity INTEGER CHECK (complexity BETWEEN 1 AND 10),
    status TEXT CHECK (status IN ('todo', 'in_progress', 'done')),
    due_date DATE,
    created_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES project(project_id),
    FOREIGN KEY (section_id) REFERENCES section(section_id),
    FOREIGN KEY (assignee_id) REFERENCES user(user_id)
);


CREATE TABLE subtask (
    subtask_id TEXT PRIMARY KEY,
    parent_task_id TEXT NOT NULL,
    name TEXT NOT NULL,
    complexity INTEGER CHECK (complexity BETWEEN 1 AND 10),
    status TEXT CHECK (status IN ('todo', 'in_progress', 'done')),
    created_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    FOREIGN KEY (parent_task_id) REFERENCES task(task_id)
);


CREATE TABLE comment (
    comment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    body TEXT NOT NULL,
    sentiment TEXT CHECK (sentiment IN ('neutral', 'positive', 'blocking')),
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES task(task_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);


CREATE TABLE custom_field (
    custom_field_id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    name TEXT NOT NULL,
    field_type TEXT CHECK (
        field_type IN ('text', 'number', 'enum', 'boolean')
    ),
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (workspace_id) REFERENCES workspace(workspace_id)
);


CREATE TABLE custom_field_value (
    custom_field_value_id TEXT PRIMARY KEY,
    custom_field_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    value TEXT,
    FOREIGN KEY (custom_field_id) REFERENCES custom_field(custom_field_id),
    FOREIGN KEY (task_id) REFERENCES task(task_id)
);


CREATE TABLE tag (
    tag_id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (workspace_id) REFERENCES workspace(workspace_id)
);


CREATE TABLE task_tag (
    task_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    PRIMARY KEY (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES task(task_id),
    FOREIGN KEY (tag_id) REFERENCES tag(tag_id)
);


CREATE TABLE attachment (
    attachment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    filename TEXT NOT NULL,
    file_type TEXT,
    size_kb INTEGER,
    uploaded_at TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES task(task_id)
);
