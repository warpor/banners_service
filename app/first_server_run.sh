alembic upgrade head


python create_initial_users.py
uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8000