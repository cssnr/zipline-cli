import os
import sys
import time

import psycopg2
import requests


pg_data = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "postgres",
}
zip_data = {
    "username": "administrator",
    "password": "password",
    "code": None,
}
query = 'SELECT "token" FROM public."User";'

# set zipline url
zip_uri = os.environ.get("ZIPLINE_URL", "http://localhost:3000").rstrip("/")
# setup
r = requests.post(f"{zip_uri}/api/setup", json=zip_data)
r.raise_for_status()
time.sleep(3)
# login
r = requests.post(f"{zip_uri}/api/auth/login", json=zip_data)
r.raise_for_status()

# get token from postgres
with psycopg2.connect(**pg_data) as conn:  # type: ignore
    with conn.cursor() as cur:
        cur.execute(query)
        result = cur.fetchone()

# exit with error if no results
if not result:
    print(f"No result from postgres query: {query}")
    sys.exit(1)

# print environment variable for export
print(f"{result[0]}")
