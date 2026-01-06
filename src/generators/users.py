import random
from faker import Faker

from utils.random_utils import (
    uuid,
    truncated_normal,
    poisson,
    random_date,
)

fake = Faker()

ROLE_DIST = [
    ("IC", 0.72),
    ("Lead", 0.15),
    ("Manager", 0.10),
    ("Director", 0.03),
]


TEAM_SIZE_MULTIPLIER = {
    "platform": 1.4,
    "backend": 1.3,
    "frontend": 1.2,
    "data": 1.1,
    "ml": 0.9,
    "devops": 0.8,
    "infra": 0.8,
    "product": 0.6,
    "design": 0.5,
    "qa": 0.7,
    "mobile": 0.6,
    "security": 0.4,
}


def generate(cursor, workspace_id, team_ids, users_per_team=400):
    """
    Generate enterprise-scale users with realistic team-size imbalance.

    Returns:
        List[str]: user_ids
    """

    user_ids = []

    print(" Generating users with team-size imbalance...")

    for team_id in team_ids:
        team_key = team_id.replace("team-", "")
        multiplier = TEAM_SIZE_MULTIPLIER.get(team_key, 1.0)

        # Gaussian variation + hard minimum
        base_size = int(users_per_team * multiplier)
        team_size = int(random.gauss(base_size, base_size * 0.15))
        team_size = max(50, team_size)

        print(f" Team {team_key}: {team_size} users")

        for _ in range(team_size):
            name = fake.name()
            email = (
                name.lower()
                .replace(" ", ".")
                .replace("'", "")
                + "@acme.com"
            )

            # Role sampling
            role = random.choices(
                [r for r, _ in ROLE_DIST],
                [w for _, w in ROLE_DIST],
            )[0]

            # Capacity logic
            capacity = poisson(6)
            if role in {"Manager", "Director"}:
                capacity = max(1, capacity // 2)

            # Efficiency & burnout
            efficiency = round(truncated_normal(), 2)
            burnout = round(random.uniform(0.0, 0.4), 2)

            created_at = random_date(540)

            user_id = uuid()

            # ----------------------------------------------------
            # Insert user
            # ----------------------------------------------------
            cursor.execute(
                """
                INSERT INTO user (
                    user_id,
                    workspace_id,
                    name,
                    email,
                    role,
                    capacity,
                    efficiency,
                    burnout,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    workspace_id,
                    name,
                    email,
                    role,
                    capacity,
                    efficiency,
                    burnout,
                    created_at,
                ),
            )

            # ----------------------------------------------------
            # Team membership
            # ----------------------------------------------------
            cursor.execute(
                """
                INSERT INTO team_membership (
                    team_id,
                    user_id,
                    joined_at
                )
                VALUES (?, ?, ?)
                """,
                (
                    team_id,
                    user_id,
                    created_at,
                ),
            )

            user_ids.append(user_id)

    print(f"Total users generated: {len(user_ids)}")
    return user_ids
