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
    # Desactiver le cache en mode dev.
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

    random_animals = db.get_random_animals()
    if not random_animals :
        message = "Aucun animal n'a ete publie dans la base de donnees."     

    return render_template('index.html', animals = random_animals, message = message)

@app.route('/animal/<int:animal_id>')
def animal_details(animal_id):
    db = get_db()
    animal = db.get_animal(animal_id)
    msg = ''
    if not animal:
        msg = "Aucun animal trouve !!!"

    return render_template('animal-details.html', animal = animal, message = msg)

@app.route('/rechercher', methods = ['GET'])
def rechercher():
    db = get_db()
    if 'query' in request.args: 
        query = request.args.get('query','').strip()
        if(query):
            results = db.search_animals(query)
            return render_template('search-result.html', results = results, query = query)
        else: 
            redirect(url_for('page_not_found.html'))
    
    return render_template('search-page.html')


@app.route('/mettre-en-adoption', methods=['GET', 'POST'])
def add_animal():
    db = get_db()
    
    if request.method == 'POST':
        # Recuperer et netoyer les donnees du formulaire.
        try:
            nom = request.form['nom'].strip()
            espece = request.form['espece'].strip()
            race = request.form['race'].strip()
            age = int(request.form['age'])  
            description = request.form['description'].strip()
            courriel = request.form['courriel'].strip()
            adresse = request.form['adresse'].strip()
            ville = request.form['ville'].strip()
            cp = request.form['cp'].strip()
        except (KeyError, ValueError):
            return render_template('adopter-form.html', message="Entree Invalide: Verifier les donnees et recommencer.")
        
        # Tentative d'insertion des donnees dans la bd.
        try:
            new_animal_id = db.add_animal(nom, espece, race, age, description, courriel, adresse, ville, cp)
        except Exception as e:
            app.logger.error(f"Echec d'ajout de l'animal: {e}")
            return render_template('adopter-form.html', message="Erreur d'insertion dans la base de donnees ")
        
        # Redirige l'utilisateur vers la page des details sur l'animal recement ajouter 
        return redirect(url_for('animal_details', animal_id=new_animal_id))
    
    
    return render_template('adopter-form.html')

# page 404 personnalise
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__name__':
    app.run(debug=True, threaded=False)
