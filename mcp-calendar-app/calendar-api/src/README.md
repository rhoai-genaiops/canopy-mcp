# calendar-api

A simple calendar API powered by FastAPI.

## Architecture

```md
- database
	- build.py
	- database_handler.py
- server
	- method.py
	- server.py
- client
	- client.py
```

## Usage

### With uv (recommended)
```bash
# Install dependencies from requirements.txt
uv pip install -r requirements.txt

# Create SQLite database (first time only)
uv run python build.py

# Start the FastAPI server
uv run uvicorn server:app --reload --host 127.0.0.1 --port 8000 --workers 4 --limit-concurrency 100 --timeout-keep-alive 5

# Test the API (optional)
uv run python client.py
```

### With pip
1. Install dependencies: `pip install -r requirements.txt`
2. Run `python build.py` to create a SQLite database (only run for the first time)
3. Run `uvicorn server:app --reload --host 127.0.0.1 --port 8000 --workers 4 --limit-concurrency 100 --timeout-keep-alive 5`
4. Run test code in `client.py`, or try it out on `http://127.0.0.1:8000/docs`

## Test Data

To populate the database with sample schedules for testing:

```bash
# Add test data
python test_data.py

# Remove test data
python test_data.py clear
```

The test data includes various Redwood Digital University activities (lectures, labs, office hours, assignments, faculty meetings, PhD defenses, workshops, study groups, etc.) across different dates to demonstrate the academic calendar functionality.

## Local Development

```md
python build.py
docker run -d --name calendar-api -p 8000:8000 -v $(pwd)/CalendarDB.db:/app/CalendarDB.db calendar-api:v1
```