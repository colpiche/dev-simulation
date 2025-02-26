from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
import re

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
                    fonction VARCHAR(255) NOT NULL
                );
            """)
            cursor.execute("""
                INSERT INTO formulaire (nom, fonction) VALUES
                ('Alice', 'Développeuse'),
                ('Bob', 'Designer'),
                ('Charlie', 'Chef de projet');
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

def validate_field(field, regex):
    # Exemple de regex pour valider les champs (par exemple, accepter uniquement les lettres et les chiffres)
    pattern = re.compile(regex)
    if not pattern.match(field):
        return f"Invalid input. Only letters and numbers are allowed."
    return None

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

        # Validate each field
        error_messages['champ_nom'] = validate_field(nom, r'^[a-zA-Z0-9]+$')
        error_messages['champ_fonction'] = validate_field(fonction, r'^[a-zA-Z0-9]+$')

        if not any(error_messages.values()):
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO formulaire (nom, fonction) VALUES (%s, %s)', (nom, fonction))
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
        cursor.execute('SELECT * FROM formulaire')
        entries = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
    finally:
        cursor.close()
        conn.close()
    return render_template('index.html', entries=entries, error_messages=error_messages)

if __name__ == '__main__':
    initialize_database()
    app.run(host='0.0.0.0', port=5000)
