#!/bin/bash
set -euxo pipefail

python3 -m pip install -r requirements.txt
python3 manage.py collectstatic --noinput -v 3

# List a few files to prove they exist in the build env
python3 - << 'PY'
import os
root="staticfiles"
hits=0
for path,_,files in os.walk(root):
    for f in files:
        if f.endswith(".css") and ("style" in f or "bootstrap" in f):
            print("STATIC:", os.path.join(path, f))
            hits += 1
print("TOTAL_STATIC_MATCHES:", hits)
PY

# Optional: show top-level structure
ls -la staticfiles || true
