import subprocess
from urllib.parse import urlparse
import gzip
import shutil
import os
import time
from dotenv import load_dotenv
load_dotenv()

import subprocess
import urllib.parse


def parse_db_uri(uri):
    result = urllib.parse.urlparse(uri)
    return {
        'dbname': result.path[1:],
        'user': result.username,
        'password': result.password,
        'host': result.hostname,
        'port': 5432,
    }

def dump_db(db):
    # Execute pg_dump
    dump_command = (
        f'PGPASSWORD={db["password"]} pg_dump -U {db["user"]} -h {db["host"]} -p {db["port"]} '
        f'-d {db["dbname"]} -F c -b -v -f "/tmp/db_backup"'
    )
    print(f"Running: {dump_command}")
    subprocess.run(dump_command, shell=True, check=True)

def restore_db(db):
    # Execute pg_restore
    restore_command = (
        f'PGPASSWORD={db["password"]} pg_restore -U {db["user"]} -h {db["host"]} -p {db["port"]} '
        f'-d {db["dbname"]} -v "/tmp/db_backup"'
    )
    print(f"Running: {restore_command}")
    subprocess.run(restore_command, shell=True, check=True)

# Read URIs from environment variables
src_uri = os.environ.get('SRC_URI')
dest_uri = os.environ.get('DEST_URI')

# Ensure the URIs have been provided
if not src_uri or not dest_uri:
    raise ValueError("Both SRC_URI and DEST_URI must be set")

# Parse URIs
src_db = parse_db_uri(src_uri)
dest_db = parse_db_uri(dest_uri)

# Dump source DB and restore to destination DB
dump_db(src_db)
restore_db(dest_db)


if __name__ == "__main__":
    # Parse URIs
    src_db = parse_db_uri(src_uri)
    dest_db = parse_db_uri(dest_uri)

    # Dump source DB and restore to destination DB
    dump_db(src_db)
    restore_db(dest_db)
    print("FINISHED")
    time.sleep(10000)

