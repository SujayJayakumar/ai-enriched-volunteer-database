import sqlite3

DB_PATH = "data/volunteer_data.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("\nTables:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
for t in cursor.fetchall():
    print("-", t[0])

print("\nSample members:")
cursor.execute("SELECT member_id, name, last_active FROM members LIMIT 5")
for row in cursor.fetchall():
    print(row)

print("\nSample persona analysis:")
cursor.execute("""
    SELECT m.name, p.persona, p.confidence
    FROM persona_analysis p
    JOIN members m ON m.member_id = p.member_id
    LIMIT 5
""")
for row in cursor.fetchall():
    print(row)

print("\nUncertain personas:")
cursor.execute("""
    SELECT m.name, p.confidence
    FROM persona_analysis p
    JOIN members m ON m.member_id = p.member_id
    WHERE p.persona = 'Uncertain'
""")
for row in cursor.fetchall():
    print(row)

print("\nSkills distribution:")
cursor.execute("""
    SELECT s.skill_name, COUNT(*) 
    FROM member_skills ms
    JOIN skills s ON s.skill_id = ms.skill_id
    GROUP BY s.skill_name
""")
for row in cursor.fetchall():
    print(row)

conn.close()
