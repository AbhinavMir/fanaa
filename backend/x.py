import sqlite3
import json

# Connect to the perfumes.sqlite database
conn = sqlite3.connect('perfumes.sqlite')
c = conn.cursor()

# Enter the names of five perfumes to test
perfumes = ['Santal Blush', 'Tobacco Vanille', 'Tuscan Leather', 'Velvet Gardenia', 'Vert Bohème']

# Extract the notes, main accords, longevity, and sillage for the entered perfumes
notes = []
main_accords = []
longevity = []
sillage = []
for perfume in perfumes:
    query = "SELECT perfume, notes, main_accords, longevity, sillage FROM perfumes WHERE perfume=?"
    c.execute(query, (perfume,))
    result = c.fetchone()
    if result:
        title = json.loads(result[0])['title']
        notes.append(result[1]['general'])
        main_accords.append(result[2])
        longevity.append(result[3])
        sillage.append(result[4])

# Score the notes for each perfume based on their frequency
note_scores = {}
for note_list in notes:
    for note in note_list:
        note = note.strip()
        if note in note_scores:
            note_scores[note] += 1
        else:
            note_scores[note] = 1

# Determine the minimum number of matching notes required for a perfume to be recommended
min_matches = len(perfumes) * 0.3

# Query the database to find new perfumes that match the user's preferred notes
preferred_notes = sorted(note_scores, key=note_scores.get, reverse=True)[:3]
query = "SELECT perfume FROM perfumes WHERE notes LIKE ?"
params = ('%{}%'.format('%'.join(preferred_notes)),)
c.execute(query, params)
results = c.fetchall()

# Filter the recommended perfumes based on the number of matching notes and main accords
recommended = []
for result in results:
    perfume = json.loads(result[0])
    if perfume['title'] not in perfumes:
        num_matches = 0
        for note in perfume['notes']['general']:
            if note.strip() in preferred_notes:
                num_matches += 1
        if num_matches >= min_matches:
            match = False
            for accord in perfume['main_accords']:
                if accord in ['warm spicy', 'balsamic', 'smoky', 'floral', 'woody']:
                    match = True
                    break
            if match:
                recommended.append(perfume)

# Print the recommended perfumes
print("Recommended perfumes:")
for perfume in recommended:
    print(perfume['title'])

# Close the database connection
conn.close()
