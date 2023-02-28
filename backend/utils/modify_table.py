import sqlite3
import json

# Connect to the perfumes.sqlite database
conn = sqlite3.connect('perfumes.sqlite')
c = conn.cursor()

# Add the image and title columns to the perfumes table
c.execute("ALTER TABLE perfumes ADD COLUMN image TEXT")
c.execute("ALTER TABLE perfumes ADD COLUMN title TEXT")

# Update the image and title columns based on the perfume data in the perfume column
query = "SELECT rowid, perfume FROM perfumes"
c.execute(query)
results = c.fetchall()
for result in results:
    rowid = result[0]
    perfume = json.loads(result[1])
    print("working!")
    c.execute("UPDATE perfumes SET image=?, title=? WHERE rowid=?", (perfume.get('image'), perfume['title'], rowid))

# Commit the changes and close the database connection
conn.commit()
conn.close()
