
import sqlite3

# Connect to the database
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# Create table with a unique email constraint
cursor.execute("""
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
""")
conn.commit()


def add_record(name, email):
    # Validate the input
    name = name.strip()
    email = email.strip().lower()

    if not name or not email or "@" not in email:
        print("Invalid data: rejected")
        return

    # Check for duplicate data
    cursor.execute(
        "SELECT 1 FROM records WHERE email = ?", (email,)
    )

    if cursor.fetchone():
        print("Redundant data: duplicate found")
        return

    # Insert unique and valid data
    cursor.execute(
        "INSERT INTO records (name, email) VALUES (?, ?)",
        (name, email)
    )
    conn.commit()
    print("Verified data added successfully")


# Test the system
add_record("Arun", "arun@gmail.com")
add_record("Arun", "arun@gmail.com")
add_record("", "invalid-email")

# Display stored records
cursor.execute("SELECT * FROM records")
print("\nDatabase Records:")
for record in cursor.fetchall():
    print(record)

conn.close()
