import random
import string

# Génération d'une chaine de caractères aléatoire
def generate_random_text(longueur):
    lettres = string.ascii_letters
    return ''.join(random.choice(lettres) for i in range(longueur))

# Définir les images pour les éléments de l'interface utilisateur
champ_nom = "champ_nom.png"
champ_fonction = "champ_fonction.png"
bouton_envoyer = "bouton_envoyer.png"

# Région où le tableau des résultats devrait apparaître
region_tableau = Region(627,606,661,289)

# Nombre de tests à effectuer
nombre_iterations = 20

# Compteurs pour les tests réussis et échoués
tests_reussis = 0
tests_echoues = 0

for _ in range(nombre_iterations):
    # Générer des valeurs aléatoires pour les champs
    nom = generate_random_text(8)
    fonction = generate_random_text(8)

    # Remplirle formulaire
    click(champ_nom)
    type(nom)
    click(champ_fonction)
    type(fonction)
    click(bouton_envoyer)

    # Attendre la mise à jour des résultats
    wait(2)

    # Capturer la région et afficher le texte détecté
    texte_capture = region_tableau.text()
    print("Texte capturé : {}".format(texte_capture))

    # Vérifier que les valeurs s'affichent correctement dans le tableau
    if region_tableau.text().find(nom) != -1 and region_tableau.text().find(fonction) != -1:
        print("Test réussi pour {} : {}".format(nom, fonction))
        tests_reussis += 1
    else:
        print("Test échoué pour {} : {}".format(nom, fonction))
        tests_echoues += 1

# Calculer et afficher le taux de succès
taux_succes = (float(tests_reussis) / float(nombre_iterations)) * 100
print("Tests réussis : {}".format(tests_reussis))
print("Tests échoués : {}".format(tests_echoues))
print("Taux de succès : {:.2f}%".format(taux_succes))
