import sqlite3

conn = sqlite3.connect("data/volunteer_data.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM persona_analysis")
cursor.execute("DELETE FROM member_skills")
cursor.execute("DELETE FROM skills")
cursor.execute("DELETE FROM enrichment_runs")

conn.commit()
conn.close()

print("Enrichment tables reset.")
