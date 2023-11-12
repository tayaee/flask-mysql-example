if not exist venv (
    python -m venv venv
    if exist requirements.txt venv\scripts\pip install -r requirements.txt
)
venv\scripts\python migrate_db.py
venv\scripts\python web.py