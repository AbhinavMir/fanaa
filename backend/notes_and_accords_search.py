from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Connect to the perfumes.sqlite database
conn = sqlite3.connect('perfumes.sqlite')
c = conn.cursor()

def get_common_patterns(perfumes):
    # Create a list of sets of the main accords and notes for each perfume
    main_accords_sets = [set(perfume['main_accords']) for perfume in perfumes]
    notes_sets = [set(perfume['notes']['general']) for perfume in perfumes]

    # Calculate the common patterns in the main accords and notes
    common_main_accords = sorted(set.intersection(*main_accords_sets), key=lambda x: main_accords_sets[0].index(x))
    common_notes = sorted(set.intersection(*notes_sets), key=lambda x: notes_sets[0].index(x))

    # Format the common patterns as a dictionary
    result = {
        'common_main_accords': common_main_accords,
        'common_notes': common_notes
    }
    return result

@app.route('/patterns', methods=['POST'])
def get_patterns():
    print("called   ")
    # Parse the request body to get the list of favorite perfumes
    perfumes = request.json['perfumes']

    # Query the perfumes table to get the main accords and notes for each perfume
    query = "SELECT main_accords, notes FROM perfumes WHERE title = ?"
    perfume_data = []
    for perfume in perfumes:
        c.execute(query, (perfume,))
        result = c.fetchone()
        if result is not None:
            main_accords = result[0]
            notes = result[1]
            perfume_data.append({
                'title': perfume,
                'main_accords': main_accords,
                'notes': notes
            })

    # Calculate the common patterns in the main accords and notes
    result = get_common_patterns(perfume_data)

    # Return the common patterns as a JSON response
    return jsonify(result)

if __name__ == '__main__':
    app.run()
