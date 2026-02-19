# Entry Log — Input Form + Store & Display

A small Flask web application that accepts user input (name, email, notes), validates it, persists entries to a SQLite database, and displays them in a clean interface with the ability to edit and delete individual records.

---

## What it does

- **Submit entries** via a form (name, email, optional notes)
- **Validates** all input server-side with clear error messages:
  - Name is required, 100 characters or fewer
  - Email is required and must be a valid email format
  - Notes are required and capped at 1000 characters
- **Persists** entries in a SQLite database
- **Displays** all entries in reverse-chronological order
- **Edit** existing entries inline without leaving the page
- **Delete** individual entries with a confirmation prompt

---

## Project structure

```
project/
├── app.py                  # Flask routes and validation logic
├── database.py             # SQLite helpers (init, insert, read, update, delete)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── tests.py
├── README.md
├── static/
│   ├── style.css           # All styling
│   └── main.js             # All JavaScript
└── templates/
    └── index.html          # Jinja2 HTML template
```

---

## How to run

### Option 1 — Docker (recommended)

Ensure Docker Desktop is installed and running, then:

```bash
docker-compose up --build
```

Then open [http://localhost:5000](http://localhost:5000).

To stop the app:

```bash
docker-compose down
```

### Option 2 — Local Python

**Requirements**: Python 3.10+

```bash
pip install -r requirements.txt
python app.py
```

Then open [http://localhost:5000](http://localhost:5000).

---

## Running the tests

```bash
pip install pytest
pytest tests.py -v
```

The tests cover:
- Valid form submission and persistence
- Validation errors (missing name, missing/invalid email, letters-only name, oversized fields)
- Edit/update existing entries
- Delete (existing and non-existent entries)
- Database ordering (newest first)

---

## Key design choices

**Separation** —  `database.py` is a data-access module with no Flask imports. `app.py` handles HTTP and validation only. Styling lives in `static/style.css` and JavaScript in `static/main.js`, keeping `index.html` clean and readable.

**Server-side validation** — all validation happens in `app.py` before any database write. The form preserves user input on error so the user does not have to retype everything.

---

## AI usage

This project was built with assistance from Claude. Claude was used to:
- Write the CSS 
- Write tests for API requests
- Assist with Docker configuration and troubleshooting
- Formatting the README documentation in case I forgot anything
