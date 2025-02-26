<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulaire</title>
    <link rel="stylesheet" type="text/css" href="/static/styles.css">
</head>
<body>
    <h1>Formulaire</h1>
    <form method="POST">
        <input type="text" id="champ_nom" name="champ_nom" placeholder="Nom"><br><br>
        <input type="text" id="champ_fonction" name="champ_fonction" placeholder="Fonction"><br><br>
        <input type="submit" value="Envoyer">
    </form>

    <h2>Entrées de la base de données</h2>
    <ul>
        % for entry in entries:
            <li>{{ entry[1] }} : {{ entry[2] }}</li>
        % end
    </ul>
</body>
</html>
