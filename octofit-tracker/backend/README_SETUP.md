Setup and run populate_db (backend)

Quick steps to create a virtual environment, install project dependencies, run migrations and populate the database.

Run these from the workspace root (do not change directories):

```bash
python3 -m venv octofit-tracker/backend/venv
source octofit-tracker/backend/venv/bin/activate
pip install -r octofit-tracker/backend/requirements.txt
python octofit-tracker/backend/manage.py migrate --noinput
python octofit-tracker/backend/manage.py populate_db
```

Or run the helper script:

```bash
bash octofit-tracker/backend/scripts/setup_and_run_populate.sh
```
