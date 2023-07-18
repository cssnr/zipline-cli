import os
import sys
import psycopg2
import requests

query = 'SELECT "token" FROM public."User" WHERE id=1 ORDER BY id ASC;'
pg_data = {
    'host': 'postgres',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
}
zip_data = {
    'username': 'administrator',
    'password': 'password',
    'code': None,
}

# set zipline url
zip_uri = os.environ.get('ZIPLINE_URL', 'http://zipline:3000').rstrip('/')
zip_url = f'{zip_uri}/api/auth/login'

# log in to create account
r = requests.post(zip_url, json=zip_data)
r.raise_for_status()

# get token from postgres
with psycopg2.connect(**pg_data) as conn:
    with conn.cursor() as cur:
        cur.execute(query)
        result = cur.fetchone()

# exit with error if no results
if not result:
    print(f'No result from postgres query: {query}')
    sys.exit(1)

# print environment variable for export
print(f'{result[0]}')
