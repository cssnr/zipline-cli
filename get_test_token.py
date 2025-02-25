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
# print(r.status_code)
# print(r.json())
time.sleep(2)


# login
r = s.post(f"{zip_uri}/api/auth/login", json=zip_data)
r.raise_for_status()
# print(r.status_code)
# print(r.json())


# token
r = s.get(f"{zip_uri}/api/user/token")
r.raise_for_status()
# print(r.status_code)
data = r.json()
# print(data)

print(data["token"])
