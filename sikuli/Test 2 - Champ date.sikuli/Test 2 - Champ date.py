import random
import string
import datetime

# Génération d'une chaîne de caractères aléatoire
def generate_random_text(longueur):
    lettres = string.ascii_letters
    return ''.join(random.choice(lettres) for i in range(longueur))

# Génération d'une date invalide
def generate_invalid_date():
    # Exemple de dates invalides : 31 février, 31 avril, 31 juin, 31 septembre, 31 novembre
    invalid_dates = ["2023-02-30", "2023-04-31", "2023-06-31", "2023-09-31", "2023-11-31"]
    return random.choice(invalid_dates)

# Génération d'une date valide
def generate_valid_date():
    # Générer une date aléatoire dans une plage valide
    start_date = datetime.date(1900, 1, 1)
    end_date = datetime.date(2099, 12, 31)
    random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.strftime("%Y-%m-%d")

# Définir les images pour les éléments de l'interface utilisateur
champ_nom = "champ_nom.png"
champ_fonction = "champ_fonction.png"
champ_date = "champ_date.png"
bouton_envoyer = "bouton_envoyer.png"

# Région où le tableau des résultats devrait apparaître
region_tableau = Region(627, 606, 661, 400)

# Nombre de tests à effectuer
nombre_iterations = 20

# Compteurs pour les tests réussis et échoués
tests_reussis = 0
tests_echoues = 0

for i in range(nombre_iterations):
    # Générer des valeurs aléatoires pour les champs
    nom = generate_random_text(8)
    fonction = generate_random_text(8)

    # Alterner entre dates valides et invalides
    if i % 2 == 0:
        date_test = generate_valid_date()
        print("Test avec une date valide : {}".format(date_test))
        attendu_dans_tableau = True
    else:
        date_test = generate_invalid_date()
        print("Test avec une date invalide : {}".format(date_test))
        attendu_dans_tableau = False

    # Remplir le formulaire
    click(champ_nom)
    type(nom)
    click(champ_fonction)
    type(fonction)
    click(champ_date)
    type(date_test)
    click(bouton_envoyer)

    # Attendre la mise à jour des résultats
    wait(2)

    # Capturer la région et afficher le texte détecté
    texte_capture = region_tableau.text()
    print("Texte capturé : {}".format(texte_capture))

    # Vérifier les résultats en fonction du type de date
    if attendu_dans_tableau:
        # Pour une date valide, vérifier que les données apparaissent
        if nom in texte_capture and fonction in texte_capture and date_test in texte_capture:
            print("Test réussi : les données du formulaire apparaissent dans le tableau.")
            tests_reussis += 1
        else:
            print("Test échoué : les données du formulaire n'apparaissent pas dans le tableau.")
            tests_echoues += 1
    else:
        # Pour une date invalide, vérifier que les données n'apparaissent pas
        if nom not in texte_capture and fonction not in texte_capture and date_test not in texte_capture:
            print("Test réussi : les données du formulaire n'apparaissent pas dans le tableau.")
            tests_reussis += 1
        else:
            print("Test échoué : les données du formulaire apparaissent dans le tableau.")
            tests_echoues += 1

# Calculer et afficher le taux de succès
taux_succes = (float(tests_reussis) / float(nombre_iterations)) * 100
print("Tests réussis : {}".format(tests_reussis))
print("Tests échoués : {}".format(tests_echoues))
print("Taux de succès : {:.2f}%".format(taux_succes))
