import sqlite3

from src.database import database


def setup_function():
    database.initialize_database()
    conn = sqlite3.connect(database.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM saved_universities")
    cursor.execute("DELETE FROM searches")
    conn.commit()
    conn.close()


def test_duplicate_universities_are_blocked():
    first_save = database.save_university("MIT", "United States", "mit.edu", "https://mit.edu")
    second_save = database.save_university("mit", "United States", "mit.edu", "https://mit.edu")

    assert first_save is True
    assert second_save is False

    saved_universities = database.get_saved_universities()
    assert len(saved_universities) == 1


def test_saved_university_can_be_deleted():
    database.save_university("Oxford", "United Kingdom", "ox.ac.uk", "https://www.ox.ac.uk")

    deleted = database.delete_university("Oxford")
    saved_universities = database.get_saved_universities()

    assert deleted is True
    assert saved_universities == []


def test_search_history_is_returned_in_reverse_order():
    database.save_search("MIT", "United States")
    database.save_search("Cambridge", "United Kingdom")

    history = database.get_search_history(limit=5)

    assert len(history) == 2
    assert history[0]["university"] == "Cambridge"
    assert history[1]["university"] == "MIT"
