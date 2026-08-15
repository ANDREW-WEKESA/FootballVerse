import sqlite3

db = sqlite3.connect("footballverse.db")

specs = {
    "youtube_video_id": "VARCHAR(100)",
    "youtube_timestamp": "VARCHAR(50)",
    "youtube_channel": "VARCHAR(200)",
    "youtube_title": "VARCHAR(500)",
    "evidence_notes": "TEXT",
}

columns = {
    row[1]
    for row in db.execute("PRAGMA table_info(player_goals)")
}

for name, sql_type in specs.items():
    if name not in columns:
        db.execute(
            f'ALTER TABLE player_goals ADD COLUMN {name} {sql_type} NOT NULL DEFAULT ""'
        )
        print("ADDED:", name)
    else:
        print("EXISTS:", name)

db.commit()

print("\nPLAYER GOALS COLUMNS:")
for row in db.execute("PRAGMA table_info(player_goals)"):
    print(row[1])

db.close()
