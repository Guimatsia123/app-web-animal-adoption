# Copyright 2024 <Votre nom et code permanent>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask import render_template, request, jsonify, redirect, url_for
from flask import g
from .database import Database

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.after_request
def add_header(response):
    # Disable caching by setting Cache-Control headers
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response



def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route('/')
def index():
    db = get_db()
    # À remplacer par le contenu de votre choix.
    random_animals = db.get_random_animals()

    return render_template('index.html', animals = random_animals)

@app.route('/animal/<int:animal_id>')
def animal_details(animal_id):
    db = get_db()
    animal = db.get_animal(animal_id)
    msg = ''
    if not animal:
        msg = "Aucun animal trouve !!!"

    return render_template('animal-details.html', animal = animal, message = msg)

@app.route('/search', methods = ['GET'])
def search():
    db = get_db()
    query = request.args.get('query','')
    results = db.search_animals(query)

    return render_template('search-result.html', results = results, query = query)


@app.route('/mettre-en-adoption', methods = ['GET','POST'])
def add_animal():
    db = get_db()

    if request.method =='POST':
        new_animal_id = db.add_animal(
            request.form['nom'], request.form['espece'], request.form['race'],
            request.form['age'], request.form['description'], request.form['courriel'],
            request.form['adresse'], request.form['ville'], request.form['cp']
        )
        return redirect(url_for('animal_details', animal_id = new_animal_id))
    
    return render_template('adopter-form.html')


if __name__ == '__name__':
    app.run(debug=True, threaded=False)
