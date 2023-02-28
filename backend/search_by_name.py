from flask import Flask, request, jsonify
from fuzzywuzzy import fuzz
import sqlite3

app = Flask(__name__)

def fuzzy_search_perfume(name):
    # Connect to the perfumes.sqlite database
    conn = sqlite3.connect('../perfumes.sqlite')
    c = conn.cursor()

    # Find the closest match for the given name in the title and brand columns
    query = "SELECT title, brand FROM perfumes"
    c.execute(query)
    results = c.fetchall()
    matches = []
    for result in results:
        title = result[0]
        brand = result[1]
        title_ratio = fuzz.ratio(name.lower(), title.lower())
        brand_ratio = fuzz.ratio(name.lower(), brand.lower())
        if title_ratio > 70 or brand_ratio > 70:
            matches.append((title, brand, max(title_ratio, brand_ratio)))
    matches.sort(key=lambda x: x[2], reverse=True)

    # Close the database connection
    c.close()
    conn.close()

    return matches

@app.route('/perfumes', methods=['GET'])
def search_perfumes():
    # Get the query parameter from the request
    query = request.args.get('q')

    # Perform a fuzzy search for perfumes based on the query
    matches = fuzzy_search_perfume(query)

    # Format the results as a list of dictionaries
    results = [{'title': match[0], 'brand': match[1], 'score': match[2]} for match in matches]

    # Return the results as a JSON response
    return jsonify(results)

if __name__ == '__main__':
    app.run()
