import os
import time

import requests


zip_data = {
    "username": "administrator",
    "password": "password",
    "code": None,
}

zip_uri = os.environ.get("ZIPLINE_URL", "http://localhost:3000").rstrip("/")

s = requests.Session()

# setup
r = s.post(f"{zip_uri}/api/setup", json=zip_data)
r.raise_for_status()
time.sleep(1)

# login
r = s.post(f"{zip_uri}/api/auth/login", json=zip_data)
r.raise_for_status()

# token
r = s.get(f"{zip_uri}/api/user/token")
r.raise_for_status()
data = r.json()

print(data["token"])
