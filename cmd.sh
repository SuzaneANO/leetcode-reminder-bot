python -c '
import json
from cryptography.fernet import Fernet

key = Fernet.generate_key()
payload = {
    "users": [
        {"user": "gSkBA1WgOh", "email": "sanjosebim7@gmail.com"}
    ]
}
token = Fernet(key).encrypt(json.dumps(payload).encode("utf-8"))

with open("users.token", "wb") as f:
    f.write(token)

print("FERNET_KEY:", key.decode("utf-8"))
print("finished")
'