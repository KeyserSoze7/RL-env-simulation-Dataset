import random
import numpy as np
from datetime import datetime, timedelta

def uuid():
    import uuid
    return str(uuid.uuid4())

def truncated_normal(mean=1.0, std=0.2, low=0.3, high=2.0):
    val = random.gauss(mean, std)
    return max(low, min(high, val))

def poisson(lam=5):
    return np.random.poisson(lam)

def weighted_choice(choices):
    items, weights = zip(*choices)
    return random.choices(items, weights=weights)[0]

def random_date(start_days_ago=180):
    return datetime.utcnow() - timedelta(days=random.randint(0, start_days_ago))
