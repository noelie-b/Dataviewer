

# *DataViewer API* - Manuel d'utilisation





Vous êtes un utilisateur et souhaitez contribuer aux ressources sur la Covid-19 accessibles en ligne sur *data.gouv.fr*. Pour cela, il y a plusieurs étapes à suivre. 

Dans un premier temps, nous allons vous montrer comment vous connecter à l'application. Sans connexion, vous ne pouvez pas manipuler les données. **Néanmoins, vous pouvez tout le même récupérer et lire les données (requête GET).**

Dans un second temps, nous vous montrerons l'architecture des données. Cela vous permettra de mieux comprendre comment est organisé l'API et comment accéder à un certain type de données. 

Enfin, nous vous expliquerons le type d'opérations que vous pouvez effectuer sur les données et les requêtes associées. 



> **REMARQUE** : Pour simuler le client web, nous passons par Postman. Il vous faut donc utiliser Postman en ligne, ou bien l'installer au préalable sur votre machine.
>
> Nous utilisons également des bases de données MongoDB. Il vous faut donc [installer MongoBD](https://docs.mongodb.com/manual/administration/install-on-linux/) sur votre machine, si ce n'est pas déjà fait. 
>
> Ainsi, pour que Postman fonctionne bien avec notre application en local, *Flask* et *MongoDB* doivent être activé en arrière-plan et un environnement virtuel avec toutes les librairies téléchargées doit être activé, ou bien même créé. 
>
> ```bash
> # Installer MongoBD et l'activer
> sudo systemctl start mongod
> 
> cd ~/backend_client
> # Etape nécessaire à l'authentification (et pour garder secrètes les données servant à la connexion des utilisateurs)
> export ENV_FILE_LOCATION=./.env
> 
> # Environnement virtuel
> # pip3 install pipenv --user
> # export PATH="$PATH:/home/${whoami}/.local/bin" 
> # PIPENV_NO_INHERIT=True pipenv --python 3.7
> pipenv shell 
> # pipenv install flask flask_restful Flask-APScheduler flask-bcrypt flask-jwt-extended setuptools flasgger gunicorn
> 
> # Pour lancer l'application directement via Flask 
> python3 runapp.py 
> 
> # Pour lancer l'application avec Gunicorn 
> gunicorn -b dataviewer.api.localhost:8000 --reload --threads 3 --pythonpath  /home/${whoami}/backend_client  runapp:app
> ```



Malheureusement, nous n'avons pas réussi à déployer l'application sur le serveur Nginx, donc nous lançons l'application :

- soit avec Flask, sur le port 5000, 
- soit avec Gunicorn, sur le port 8000.

Afin de simplifier les manipulations, nous allons utiliser l'application via Gunicorn dans les exemples suivants. Par conséquent, les requêtes seront lancées à l'adresse *http://dataviewer.api.localhost:8000/*.

Pour faire des requêtes, nous pouvons passer par une ligne de commande (par exemple utiliser `curl`) ou utiliser un outil client API Web, comme **Postman**. Nous allons vous montrer les deux méthodes.





## Authentification 



### *Inscription*

Si vous ne vous êtes jamais inscrit sur l'API, il vous faut passer par une étape d'inscription. Vous allez donc réaliser une requête ***POST*** à l'adresse suivante : *http://dataviewer.api.localhost:8000/apidocs/inscription*. Il vous suffit seulement de renseigner votre email et un mot de passe (**8 caractères minimum**). Vous allez être enregistré dans la base de données avec un identifiant unique. Des exemples vous sont donnés ci-dessous : 



***Exemple d'inscription :***

- ***sur Postman***

<img src="img/postman/inscription.png" alt="inscription_postman" style="zoom: 67%;" />

| POST                      | http://dataviewer.api.localhost:8000/apidocs/inscription     |
| ------------------------- | ------------------------------------------------------------ |
| JSON en entrée            | {<br/>    "email": "user@gmail.com", <br/>    "password": "monmotdepasse"<br/>} |
| exemple de JSON en sortie | {<br/>    "id": "623de670c19e08c9bb02a713"<br/>}             |

- ***en ligne de commande*** (exemple avec un autre email car on ne peut s'incrire plusieurs fois avec la même adresse mail)

```bash
# Schéma : curl -i -X POST -H "Content-Type: application/json" -d '{"email":"<votre_adresse_mail>", "password":"<votre_mot_de_passe>"}' http://dataviewer.api.localhost:8000/apidocs/inscription

curl -i -X POST -H "Content-Type: application/json" -d '{"email":"anotheruser@hotmail.fr", "password":"monautremotdepasse"}' http://dataviewer.api.localhost:8000/apidocs/inscription
```

<img src="img/lignes_commandes/inscription.png" alt="inscription_curl" style="zoom:67%;" />



------



### *Connexion*

Si vous vous êtes déjà inscrit sur la plateforme, vous pouvez directement vous connecter à l'API. Vous allez réaliser une requête ***POST*** à l'adresse suivante : *http://dataviewer.api.localhost:8000/apidocs/connexion*. Il faut saisir l'adresse mail et le mot de passe que vous avez renseigné à votre inscription. Si les données sont correctes, vous recevrez un *token*. 
Ce *token* agit comme une clé de connexion : il vous faut renseigner cette clé pour pouvoir manipuler les données de l'API. Sans cette clé, cela revient à dire que vous ne vous êtes pas connecté et, par conséquent, vous ne pouvez pas effectuer les opérations de modifications de données. 
Cette clé de connexion est valable pour une durée de 2 jours. Au-delà de cette période, il faudra vous connecter à nouveau et obtenir une nouvelle clé. Voici des exemples de connexion : 



***Exemple de connexion :***

- ***sur Postman***

<img src="img/postman/connexion.png" alt="connexion_postman" style="zoom:67%;" />

| POST                     | http://dataviewer.api.localhost:8000/apidocs/connexion       |
| ------------------------ | ------------------------------------------------------------ |
| exemple en entrée (JSON) | <br/>    "email": "user@gmail.com", <br/>    "password": "monmotdepasse"<br/>} |
| exemple de sortie (JSON) | {<br/>    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0ODIyNDU0NiwianRpIjoiYmZkMzNmYWYtNWYwNS00Y2YzLTllNTAtMWVhZDE2NDcwZjNmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYyM2RlNjcwYzE5ZTA4YzliYjAyYTcxMyIsIm5iZiI6MTY0ODIyNDU0NiwiZXhwIjoxNjQ4Mzk3MzQ2fQ.I3JJeR7QCUG9SQAucyYHxjqv1LlNYpk8jQjkDD_0Auk"<br/>} |



- ***en ligne de commande***

```bash
# Schéma : curl -i -X POST -H "Content-Type: application/json" -d '{"email":"<votre_adresse_mail>", "password":"<votre_mot_de_passe>"}' http://dataviewer.api.localhost:8000/apidocs/connexion

curl -i -X POST -H "Content-Type: application/json" -d '{"email":"user@gmail.com", "password":"monmotdepasse"}' http://dataviewer.api.localhost:8000/apidocs/connexion
```

<img src="img/lignes_commandes/connexion.png" alt="connexion_curl" style="zoom:67%;" />





## Hiérarchisation des données 



Vous pouvez accéder à la documentation sur le lien suivant : http://dataviewer.api.localhost:8000/apidocs/

Cela vous permettra de voir les adresses de l'API et les méthodes associées à celles-ci. 

| Adresses                                                     | Méthodes HTTP disponibles |
| ------------------------------------------------------------ | ------------------------- |
| /apidocs/vaccination/                                        | GET, POST                 |
| /apidocs/vaccination/<id>                                    | GET, PUT, DELETE          |
| /apidocs/vaccination/commune                                 | GET                       |
| /apidocs/vaccination/commune/<code-commune>                  | GET, POST, PUT            |
| /apidocs/vaccination/commune/<code-commune>/semaine          | GET                       |
| /apidocs/vaccination/commune/<code-commune>/semaine/<semaine> | GET, POST, PUT            |
| /apidocs/vaccination/commune/<code-commune>/semaine/<semaine>/classe_age | GET                       |
| /apidocs/vaccination/commune/<code-commune>/semaine/<semaine>/classe_age/<classe-age> | GET, POST, PUT            |



<img src="img/documentation/1.png" alt="apidocs_1" style="zoom:67%;" />

<img src="img/documentation/2.png" alt="apidocs_2" style="zoom:67%;" />





## Requêtes liées aux méthodes HTTP



Dans cette API, nous utilisons les méthodes suivantes : 

- GET, pour demander une ressource, 
- POST, pour créer une nouvelle donnée,
- PUT, pour modifer une donnée déjà existante, 
- et DELETE, pour supprimer une entrée complète liée à une donnée. 

Nous notons que DELETE est utilisable qu'avec l'adresse incluant le *recordid* d'une donnée, car nous souhaitons permettre la suppression d'une donnée précise. Nous ne voulons pas que l'utilisateur puisse supprimer un ensemble de données en une seule fois.



### Exemples de requêtes en ligne de commandes

Pour utiliser les méthodes HTTP en ligne de commandes, nous utilisons la commande `curl`.



***Exemples de requêtes GET*** : 

```bash
# Pattern :
# curl -i -X GET http://dataviewer.api.localhost:8000/...

# Requête pour voir toutes les entrées
curl -i -X GET http://dataviewer.api.localhost:8000/apidocs/vaccination
# Requête pour voir l'entrée ayant l'identifiant (recordid) 8d40bdd24b81cc060ba7ee0388db711d4fa7eac5
curl -i -X GET http://dataviewer.api.localhost:8000/apidocs/vaccination/8d40bdd24b81cc060ba7ee0388db711d4fa7eac5
# Requête pour voir la liste des communes présentes dans les données
curl -i -X GET http://dataviewer.api.localhost:8000/apidocs/vaccination/commune
# Requête pour voir les entrées de Marseille 3ème arrondissement (13203), de la 11ème semaine de l'année 2021
curl -i -X GET http://dataviewer.api.localhost:8000/apidocs/vaccination/commune/13203/semaine/2021-11
# Requête pour voir la liste des classes d'âge des entrées de Marseille 3ème arrondissement (13203), de la 11ème semaine de l'année 2012
curl -i -X GET http://dataviewer.api.localhost:8000/apidocs/vaccination/commune/13203/semaine/2021-11/classe_age
# Requête pour voir les entrées de Marseille 3ème arrondissement (13203), de la 11ème semaine de l'année 2021, de la classe d'âge 20 à 39 ans
curl -i -X GET http://dataviewer.api.localhost:8000/apidocs/vaccination/commune/13203/semaine/2021-11/classe_age/20-39
```



<img src="img/lignes_commandes/GET_data_recordid.png" alt="GET_data_recordid" style="zoom:67%;" />

<img src="img/lignes_commandes/GET_classe_age.png" alt="GET_classe_age" style="zoom:67%;" />





Ensuite, pour réaliser les autres requêtes sur les données de vaccinations (notamment POST, PUT ou DELETE), il faut utiliser le token lié à votre connexion utilisateur.

- En ligne de commande, il faut aujouter l'argument suivant, avec l'option H : *-H "Authorization: Bearer <votre_token>"*



***Exemples de requêtes POST*** : 

```bash
# Pattern : 
# curl -i -X POST -H "Content-Type: application/json" -d '{...}' http://dataviewer.api.localhost:8000/... -H  "Authorization: Bearer <votre_token>"

# Requête pour poster une entrée
curl -i -X POST -H "Content-Type: application/json" -d '{"libelle_commune":"MARSEILLE 2E ARRONDISSEMENT", "commune_residence": "13202"}' http://dataviewer.api.localhost:8000/apidocs/vaccination/commune/13202 -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0ODIyNDU0NiwianRpIjoiYmZkMzNmYWYtNWYwNS00Y2YzLTllNTAtMWVhZDE2NDcwZjNmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYyM2RlNjcwYzE5ZTA4YzliYjAyYTcxMyIsIm5iZiI6MTY0ODIyNDU0NiwiZXhwIjoxNjQ4Mzk3MzQ2fQ.I3JJeR7QCUG9SQAucyYHxjqv1LlNYpk8jQjkDD_0Auk"
```

<img src="img/lignes_commandes/POST_with_commune.png" alt="POST_with_commune.png" style="zoom:67%;" />



L'identifiant (recordid) est généré automatiquement. Comme vous pouvez le remarquer, les champs non spécifiés dans le contenu JSON sont des champs vides. Dans cette requête, étant donnée que "commune_residence" dans le JSON a la même valeur que le code de la commune dans l'URL (13202), il n'y a pas forcément besoin de le spécifier dans le JSON. On aurait aussi pu écrire ceci:

```bash
curl -i -X POST -H "Content-Type: application/json" -d '{"libelle_commune":"MARSEILLE 2E ARRONDISSEMENT"}' http://dataviewer.api.localhost:8000/apidocs/vaccination/commune/13202 -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0ODIyNDU0NiwianRpIjoiYmZkMzNmYWYtNWYwNS00Y2YzLTllNTAtMWVhZDE2NDcwZjNmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYyM2RlNjcwYzE5ZTA4YzliYjAyYTcxMyIsIm5iZiI6MTY0ODIyNDU0NiwiZXhwIjoxNjQ4Mzk3MzQ2fQ.I3JJeR7QCUG9SQAucyYHxjqv1LlNYpk8jQjkDD_0Auk"
```

<img src="img/lignes_commandes/POST_without_commune.png" alt="POST_without_commune.png" style="zoom:67%;" />



***Exemples de requêtes PUT*** : 

```bash
# Pattern : 
# curl -i -X PUT -H "Content-Type: application/json" -d '{...}' http://dataviewer.api.localhost:8000/... -H  "Authorization: Bearer <votre_token>"

# Modification des informations de "libelle_commune" et "commune_residence" de l'entrée ayant identifiant (recordid) 8d40bdd24b81cc060ba7ee0388db711d4fa7eac5
curl -i -X PUT -H "Content-Type: application/json" -d '{"libelle_commune":"Paris 13ème arrondissement", "commune_residence": "75013"}' http://dataviewer.api.localhost:8000/apidocs/vaccination/8d40bdd24b81cc060ba7ee0388db711d4fa7eac5 -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0ODIyNDU0NiwianRpIjoiYmZkMzNmYWYtNWYwNS00Y2YzLTllNTAtMWVhZDE2NDcwZjNmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYyM2RlNjcwYzE5ZTA4YzliYjAyYTcxMyIsIm5iZiI6MTY0ODIyNDU0NiwiZXhwIjoxNjQ4Mzk3MzQ2fQ.I3JJeR7QCUG9SQAucyYHxjqv1LlNYpk8jQjkDD_0Auk"

# Modifie les informations de l'entrée concernant la donnée dans la commune 75113 et ayant identifiant (recordid) *8d40bdd24b81cc060ba7ee0388db711d4fa7eac5*
curl -i -X PUT -H "Content-Type: application/json" -d '{"recordid":"8d40bdd24b81cc060ba7ee0388db711d4fa7eac5", "libelle_commune":"Paris 13ème arrondissement"}' http://dataviewer.api.localhost:8000/apidocs/vaccination/commune/75113 -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0ODIyNDU0NiwianRpIjoiYmZkMzNmYWYtNWYwNS00Y2YzLTllNTAtMWVhZDE2NDcwZjNmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYyM2RlNjcwYzE5ZTA4YzliYjAyYTcxMyIsIm5iZiI6MTY0ODIyNDU0NiwiZXhwIjoxNjQ4Mzk3MzQ2fQ.I3JJeR7QCUG9SQAucyYHxjqv1LlNYpk8jQjkDD_0Auk"
```

Dans la dernière requête, l'identifiant (*recordid*) n'étant pas précisé dans l'URL, il faut le préciser dans le contenu JSON.



<img src="img/lignes_commandes/PUT_data_recordid.png" alt="PUT_data_recordid.png" style="zoom:67%;" />

<img src="img/lignes_commandes/PUT_commune_id.png" alt="PUT_commune_id.png" style="zoom:67%;" />



***Exemple de requêtes DELETE*** : 

```bash
# Pattern : 
# curl -i -X DELETE http://dataviewer.api.localhost:8000/... -H  "Authorization: Bearer <votre_token>"

# Requête pour supprimer l'entrée ayant le recordid 8d40bdd24b81cc060ba7ee0388db711d4fa7eac5
curl -i -X DELETE http://dataviewer.api.localhost:8000/apidocs/vaccination/8d40bdd24b81cc060ba7ee0388db711d4fa7eac5 -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0ODIyNDU0NiwianRpIjoiYmZkMzNmYWYtNWYwNS00Y2YzLTllNTAtMWVhZDE2NDcwZjNmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYyM2RlNjcwYzE5ZTA4YzliYjAyYTcxMyIsIm5iZiI6MTY0ODIyNDU0NiwiZXhwIjoxNjQ4Mzk3MzQ2fQ.I3JJeR7QCUG9SQAucyYHxjqv1LlNYpk8jQjkDD_0Auk"
```

<img src="img/lignes_commandes/DELETE.png" alt="DELETE" style="zoom:67%;" />



------



### Exemples de requêtes avec Postman

Les mêmes requêtes peuvent être lancé via Postman. 

Nous rappelons que pour les méthodes GET, nous avons fait en sorte que l'utilisateur n'ait pas besoin de s'identifier. 



***Exemples de requêtes GET*** : 

<img src="img/postman/GET_commune_semaine.png" alt="GET_commune_semaine.png" style="zoom:67%;" />

<img src="img/postman/GET_commune_classeage.png" alt="GET_commune_classeage.png" style="zoom:67%;" />





Ensuite, pour réaliser les autres requêtes sur les données de vaccinations (notamment POST, PUT ou DELETE), il faut utiliser le token lié à votre connexion utilisateur.

- Sur Postman, il faut le renseigner dans la partie **[Auth]**
  1.  **[Auth]** => **Type : [Bearer Token]**  
  2.  Copier le token 
  3.  Renseigner la/les données à envoyer/modifier/supprimer (sous le format JSON)
  4.  Envoyer la requête

<img src="img/postman/token_use.png" alt="token_use.png" style="zoom:67%;" />

Il est bien plus facile d'utiliser le token sur Postman car nous avons besoin de le renseigner une seule fois. Ensuite, l'authentification sera gardée pour toutes les requêtes suivantes, jusqu'à ce qu'on retire le token de l'onglet **[Auth]** ou qu'on ferme Postman. 



***Exemple de requêtes POST, PUT et DELETE*** : 

<img src="img/postman/POST.png" alt="POST" style="zoom:67%;" />

<img src="img/postman/PUT.png" alt="PUT" style="zoom:67%;" />

<img src="img/postman/DELETE.png" alt="DELETE" style="zoom:67%;" />



> **ATTENTION** : Un token a une durée du vie : il peut être utilisé pendant 2 jours. Au-delà cette durée, le token est expiré et il faut vous connecter à nouveau.





## Heroku



N'ayant pas réussi à lier la base de données à Heroku, l'utilisation de l'application sur Heroku ne nécessite pas d'authentification.
Vous pouvez accéder au site grâce au lien suivant : http://dataviewer-groupe2.herokuapp.com



Pour rappel, la RAM proposée gratuitement par Heroku étant limitée, nous n'avons pas pu y introduire l'entièreté du fichier de données sur la Covid-19 car le chargement de celle-ci nécessitait plus de RAM. Nous avons donc réduit ce fichier pour que l'utilisateur puisse tout de même accéder à quelques données. 

