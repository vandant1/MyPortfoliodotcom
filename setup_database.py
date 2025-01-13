import sqlite3
from datetime import datetime

def initialize_database():
    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()

    # Create the projects table with the 'link' and 'image_url' columns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            link TEXT,
            image_url TEXT,
            date_added TEXT DEFAULT (datetime('now','localtime'))
        )
    ''')

    # Create the achievements table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            date_achieved TEXT DEFAULT (datetime('now','localtime'))
        )
    ''')

    # Create the skills table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT NOT NULL,
            proficiency INTEGER,
            date_added TEXT DEFAULT (datetime('now','localtime'))
        )
    ''')

    # Create the project_updates table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            image_url TEXT,
            update_text TEXT NOT NULL,
            timestamp TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
    ''')

    conn.commit()
    conn.close()

def insert_project(name, description, link, image_url, date_added=None):
    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()

    # Format date_added as a string if it’s not None, or set a default string value
    if date_added is None:
        date_added = datetime.now().strftime("%Y-%m-%d")
    else:
        date_added = date_added.strftime("%Y-%m-%d") if isinstance(date_added, datetime) else date_added

    cursor.execute(
        "INSERT INTO projects (name, description, link, image_url, date_added) VALUES (?, ?, ?, ?, ?)",
        (name, description, link, image_url, date_added)
    )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully!")
