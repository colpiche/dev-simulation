from bottle import Bottle, template, request, redirect, static_file
import mysql.connector
import os

app = Bottle()

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

@app.route('/static/<filename:path>', name='static')
def serve_static(filename):
    return static_file(filename, root='./')

@app.route('/', method=['GET', 'POST'])
def index():
    """
    Affichage de la page d'accueil du site et interactions avec la base de données
    """

    entries = []
    if request.method == 'POST':
        nom = request.forms.get('champ_nom')
        fonction = request.forms.get('champ_fonction')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO formulaire (nom, fonction) VALUES (%s, %s)', (nom, fonction))
        conn.commit()
        cursor.close()
        conn.close()
        redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM formulaire')
    entries = cursor.fetchall()
    cursor.close()
    conn.close()
    return template('index', entries=entries)

if __name__ == '__main__':
    initialize_database()
    app.run(host='0.0.0.0', port=5000)
