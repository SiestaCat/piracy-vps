#!/bin/sh

docker run --rm -it \
  --env-file .env \
  -e PIP_ROOT_USER_ACTION=ignore \
  --entrypoint "/bin/sh" \
  -v "$(pwd)/auto_create_sftp_volume_dirs.py:/script.py" \
  python:3.13.1-alpine3.21 \
  -c "pip install paramiko && python3 /script.py"

docker compose up --wait --remove-orphans --renew-anon-volumes --force-recreate --y