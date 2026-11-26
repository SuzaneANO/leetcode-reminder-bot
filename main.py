from datetime import datetime, timedelta, timezone
import json
import os
from cryptography.fernet import Fernet
from notify import notify_by_email
from scrap import scrap_user

TWELVE_HOURS_MINUTES = 12 * 60

with open('users.token', 'rb') as f:
    data = f.read()

users = json.loads(Fernet(os.environ['FERNET_KEY']).decrypt(data))['users']

for user in users:
    ret = scrap_user(user['user'])
    if ret is None:
        continue

    has_recent_accepted = any(
        entry[1] == 'Accepted' and entry[2] < TWELVE_HOURS_MINUTES for entry in ret
    )

    if not has_recent_accepted:
        if ret:
            last_problem, _, last_minutes_ago = ret[0]
            last_dt = datetime.now(timezone.utc) - timedelta(minutes=last_minutes_ago)
            last_submission_str = f"{last_dt.strftime('%Y-%m-%d %H:%M UTC')} ({last_problem})"
        else:
            last_submission_str = "none found"

        print(f"Last submission for {user['user']}: {last_submission_str}")
        notify_by_email(user['user'], user['email'], last_submission_str)