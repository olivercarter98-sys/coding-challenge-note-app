import pytest
import os
import database
from app import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Create a test client with an isolated temporary database."""
    db_file = str(tmp_path / "test.db")
    monkeypatch.setattr(database, "DB_PATH", db_file)
    database.init_db()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as c:
        yield c


# ── GET / ──────────────────────────────────────────────────────────────────

def test_index_loads(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Note App" in res.data


# ── POST / – valid submission ──────────────────────────────────────────────

def test_valid_submission(client):
    res = client.post("/", data={
        "name": "Alice Smith",
        "email": "alice@example.com",
        "notes": "Hello world"
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Alice Smith" in res.data
    assert b"alice@example.com" in res.data


# ── POST / – validation errors ────────────────────────────────────────────

def test_missing_name(client):
    res = client.post("/", data={"name": "", "email": "x@x.com", "notes": "Some notes"})
    assert b"Name is required" in res.data


def test_missing_email(client):
    res = client.post("/", data={"name": "Bob", "email": "", "notes": "Some notes"})
    assert b"Email is required" in res.data


def test_invalid_email(client):
    res = client.post("/", data={"name": "Bob", "email": "not-an-email", "notes": "Some notes"})
    assert b"valid email" in res.data


def test_name_too_long(client):
    res = client.post("/", data={"name": "A" * 101, "email": "a@b.com", "notes": "Some notes"})
    assert b"100 characters" in res.data


def test_notes_too_long(client):
    res = client.post("/", data={"name": "Jo", "email": "j@j.com", "notes": "x" * 1001})
    assert b"1000 characters" in res.data


def test_missing_notes(client):
    res = client.post("/", data={"name": "Bob", "email": "bob@example.com", "notes": ""})
    assert b"Notes are required" in res.data


# ── DELETE ────────────────────────────────────────────────────────────────

def test_delete_entry(client):
    client.post("/", data={"name": "Delete Me", "email": "del@example.com", "notes": "Some notes"})
    entries = database.get_all_entries()
    assert len(entries) == 1
    entry_id = entries[0]["id"]

    res = client.post(f"/delete/{entry_id}", follow_redirects=True)
    assert res.status_code == 200
    assert len(database.get_all_entries()) == 0


def test_delete_nonexistent(client):
    res = client.post("/delete/9999", follow_redirects=True)
    assert b"not found" in res.data


# ── DATABASE helpers ──────────────────────────────────────────────────────

def test_multiple_entries_ordered_by_date(client):
    import time
    database.insert_entry("First", "first@test.com", "Some notes")
    time.sleep(1)
    database.insert_entry("Second", "second@test.com", "Some notes")
    entries = database.get_all_entries()
    assert entries[0]["name"] == "Second"
    assert entries[1]["name"] == "First"