from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
import re
from datetime import datetime

# Found here : https://a-tokyo.medium.com/first-and-last-name-validation-for-forms-and-databases-d3edf29ad29d
REGEX_NOM = r"^[a-zA-Z\xC0-\uFFFF]+([ \-']{0,1}[a-zA-Z\xC0-\uFFFF]+){0,2}[.]{0,1}$"

app = Flask(__name__, template_folder='views')

# Configuration de la base de données
db_config = {
    'user': os.getenv('DATABASE_USER'),
    'password': os.getenv('DATABASE_PASSWORD'),
    'host': os.getenv('DATABASE_HOST'),
    'database': os.getenv('DATABASE_NAME'),
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def initialize_database():
    """
    Initialisation de la base de données
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # On vérifie si la table existe déjà
        cursor.execute("SHOW TABLES LIKE 'formulaire'")
        result = cursor.fetchone()
        if not result:
            # Si non, on la crée et la popule
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS formulaire (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nom VARCHAR(255) NOT NULL,
                    fonction VARCHAR(255) NOT NULL,
                    date_permis DATE NOT NULL
                );
            """)
            cursor.execute("""
                INSERT INTO formulaire (nom, fonction, date_permis) VALUES
                ('Alice', 'Développeuse', '2020-01-15'),
                ('Bob', 'Designer', '2019-05-20'),
                ('Charlie', 'Chef de projet', '2018-08-30');
            """)
            conn.commit()
            print("Table 'formulaire' created successfully.")
        else:
            print("Table 'formulaire' already exists.")
    except mysql.connector.Error as err:
        print(f"Error initializing database: {err}")
    finally:
        cursor.close()
        conn.close()

def validate_text_field(field, regex):
    '''
    Utilisation de regex pour la vérification des données du champ
    '''

    pattern = re.compile(regex)
    if not pattern.match(field):
        return "Invalid input."
    return None

def valider_date(date_str):
    try:
        # Essayer de créer un objet date à partir de la chaîne
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return None
    except ValueError:
        # Si une exception est levée, la date n'est pas valide
        return "Invalid date."

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Affichage de la page d'accueil du site et interactions avec la base de données
    """
    entries = []
    error_messages = {}

    if request.method == 'POST':
        nom = request.form.get('champ_nom')
        fonction = request.form.get('champ_fonction')
        date_permis = request.form.get('champ_date_permis')

        # Validation des champs
        error_messages['champ_nom'] = validate_text_field(nom, REGEX_NOM)
        error_messages['champ_fonction'] = validate_text_field(fonction, REGEX_NOM)
        error_messages['champ_date_permis'] = valider_date(date_permis)

        # Insertion des valeurs dans la base si tous les champs sont valides
        if not any(error_messages.values()):
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO formulaire (nom, fonction, date_permis) VALUES (%s, %s, %s)',
                               (nom, fonction, date_permis))
                conn.commit()
            except mysql.connector.Error as err:
                print(f"Error inserting data: {err}")
            finally:
                cursor.close()
                conn.close()
            return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM formulaire ORDER BY id DESC')
        entries = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
    finally:
        cursor.close()
        conn.close()
    return render_template('index.html', entries=entries, error_messages=error_messages)

initialize_database()
app.run(host='0.0.0.0', port=5000)
