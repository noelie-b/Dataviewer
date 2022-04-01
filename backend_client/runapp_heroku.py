import json
import datetime
from flask import Flask, request, jsonify, make_response, Response, render_template
from flask_restful import Resource, Api
from flasgger import Swagger
from flask_apscheduler import APScheduler
import requests, random, string


# set configuration values for the APSheduler
class Config:
    SCHEDULER_API_ENABLED = True


# app creation
app = Flask(__name__)
api = Api(app)

# utils related to the app
swagger = Swagger(app)

# initialize scheduler
scheduler = APScheduler()

date = datetime.datetime.strptime("2022-09", '%Y-%W')
with open("./datas/donnees-de-vaccination-par-commune_reduit.json", "r") as f:
    data = f.read()
    records = json.loads(data)


def generation_id():
  global records
  while True:
    # on génère aléatoirement un identifiant
    output_string = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(40))
    find = False
    # on cherche si cet identifiant est déjà utilisé
    for record in records:
      if output_string in record["recordid"]:
          find = True
    # si ce n'est pas le cas, on le retourne
    if find == False:
      return output_string
    # sinon, on génère un autre identifiant


class DonneesCommune(Resource):
    
    def get(self):
        """Retourne la liste des entrées du dataset
        ---
        tags:
          - restful
        responses:
          200:
            description: Liste des entrées de la base de donnée
            schema:
              id: donnees-de-vaccination
              properties:
                datasetid:
                  type: string
                  description: Le nom de dataset
                  exemple: donnees-de-vaccination-par-commune
                recordid:
                  type: string
                  description: L'identifiant de l'entrée de la base de donnée
                  exemple: 8d40bdd24b81cc060ba7ee0388db711d4fa7eac5
                fields:
                  type: object
                  description: Les données d'une entrée
                  properties:
                    classe_age:
                      type: string
                      exemple: 65-74
                    libelle_commune:
                      type: string
                      exemple: MONTANAY
                    date_reference:
                      type: string
                      exemple: 2022-03-06
                    taux_cumu_1_inj:
                      type: float
                      exemple: 0.963
                    population_carto:
                      type: integer
                      exemple: 380
                    date:
                      type: string
                      exemple: 2021-11-14
                    semaine_injection:
                      type: string
                      exemple: 2021-45
                    libelle_classe_age:
                      type: string
                      exemple: de 65 à 74 ans
                    effectif_cumu_1_inj:
                      type: integer
                      exemple: 360
                    effectif_cumu_termine:
                      type: integer
                      exemple: 360
                    taux_cumu_termine:
                      type: float
                      exemple: 0.96
                    taux_termine:
                      type: float
                      exemple: 0.003
                    taux_1_inj:
                      type: float
                      exemple: 0.006
                record_timestamp:
                  type: string
                  description: La date et l'heure de la dernière modification
                  exemple: 2022-03-11T10:30:35.173Z
        """
        global records
        # on retourne l'ensemble des données au format json
        return make_response(jsonify(records), 200)


    def post(self):
        """
        Ajouter une entrée
        ---
        tags:
          - restful
        parameters:
          - in: body
            name: body
            schema:
              id: Entry
              properties:
                classe_age:
                    type: string
                    exemple: 65-74
                libelle_commune:
                    type: string
                    exemple: MONTANAY
                date_reference:
                    type: string
                    exemple: 2022-03-06
                taux_cumu_1_inj:
                    type: float
                    exemple: 0.963
                population_carto:
                    type: integer
                    exemple: 380
                date:
                    type: string
                    exemple: 2021-11-14
                semaine_injection:
                    type: string
                    exemple: 2021-45
                libelle_classe_age:
                    type: string
                    exemple: de 65 à 74 ans
                effectif_cumu_1_inj:
                    type: integer
                    exemple: 360
                effectif_cumu_termine:
                    type: integer
                    exemple: 360
                taux_cumu_termine:
                    type: float
                    exemple: 0.96
                taux_termine:
                    type: float
                    exemple: 0.003
                taux_1_inj:
                    type: float
                    exemple: 0.006
        responses:
          201:
            description: L'entrée a été crée
            schema:
              $ref: '#/definitions/donnees-de-vaccination'
        """
        # on récupère leeeeees nouvelles données
        new_datas = request.json
        # on génère un identifiant à ces données
        new_datas["recordid"] = generation_id()
        # on met en forme ces nouvelles données suivant le format de nos données (en respectant bien le type des données)
        rec = {'datasetid': "donnees-de-vaccination-par-commune",
               "fields": {
                   "classe_age": "",
                   "commune_residence": "",
                   "date": "",
                   "date_reference": "",
                   "effectif_cumu_1_inj": 0,
                   "effectif_cumu_termine": 0,
                   "libelle_classe_age": "",
                   "libelle_commune": "",
                   "population_carto": 0,
                   "semaine_injection": "",
                   "taux_1_inj": 0,
                   "taux_cumu_1_inj": 0,
                   "taux_cumu_termine": 0,
                   "taux_termine": 0}
               }
        for data in new_datas.keys():
            if data == "recordid":
                rec["recordid"] = new_datas["recordid"]
            elif data == "classe_age":
                rec["fields"]["classe_age"] = new_datas["classe_age"]
            elif data == "commune_residence":
                rec["fields"]["commune_residence"] = new_datas["commune_residence"]
            elif data == "date":
                rec["fields"]["date"] = new_datas["date"]
            elif data == "date_reference":
                rec["fields"]["date_reference"] = new_datas["date_reference"]
            elif data == "effectif_cumu_1_inj":
                rec["fields"]["effectif_cumu_1_inj"] = new_datas["effectif_cumu_1_inj"]
            elif data == "effectif_cumu_termine":
                rec["fields"]["effectif_cumu_termine"] = new_datas["effectif_cumu_termine"]
            elif data == "libelle_classe_age":
                rec["fields"]["libelle_classe_age"] = new_datas["libelle_classe_age"]
            elif data == "libelle_commune":
                rec["fields"]["libelle_commune"] = new_datas["libelle_commune"]
            elif data == "population_carto":
                rec["fields"]["population_carto"] = new_datas["population_carto"]
            elif data == "semaine_injection":
                rec["fields"]["semaine_injection"] = new_datas["semaine_injection"]
            elif data == "taux_1_inj":
                rec["fields"]["taux_1_inj"] = new_datas["taux_1_inj"]
            elif data == "taux_cumu_1_inj":
                rec["fields"]["taux_cumu_1_inj"] = new_datas["taux_cumu_1_inj"]
            elif data == "taux_cumu_termine":
                rec["fields"]["taux_cumu_termine"] = new_datas["taux_cumu_termine"]
            elif data == "taux_termine":
                rec["fields"]["taux_termine"] = new_datas["taux_termine"]
            rec["record_timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%F.%f")
        # on ajoute les nouvelles données à nos données
        global records
        records.append(rec)
        # on retourne les nouvelles données au bon format
        return make_response(jsonify(rec), 201)


class DonneeCommune(Resource):
    def get(self, id):
        """
        Lire une entrée
        ---
        tags:
          - restful
        parameters:
          - in: path
            name: id
            required: true
            description: L'identifiant de l'entrée (recordid)
            type: string
        responses:
          200:
            description: Les données de l'entrée
            schema:
              $ref: '#/definitions/donnees-de-vacination'
        """
        global records
        #  on cherche dans l'ensemble des données, 
        # une entrée avec le même identifiant que celui entrée dans l'url
        for record in records:
            if record["recordid"] == id:
              # si trouvé, on retourne cette entrée auuu format json
                return make_response(jsonify(record), 200 )
        # sinon, on retourne un message d'erreur
        return make_response(jsonify({"message": "data not found"}), 204)


    def put(self, id):
        """
        Modifier une entrée
        ---
        tags:
          - restful
        parameters:
          - in: body
            name: body
            schema:
              $ref: '#/definitions/Entry'
          - in: path
            name: id
            required: true
            description: L'identifiant de l'entrée (recordid)
            type: string
        responses:
          201:
            description: L'entrée a été modifié
            schema:
              $ref: '#/definitions/donnees-de-vaccination'
          404:
            description: L'entrée à modifier n'a pas été trouvé
        """
        global records
        # on réccupère les données d'entrée
        datas = request.json
        # on modie nos données par rapport à ceux de l'entrée
        for record in records:
            if record["recordid"] == id:
                for data in datas.keys():
                    if data == "classe_age":
                        record["fields"]["classe_age"] = datas["classe_age"]
                    elif data == "commune_residence":
                        record["fields"]["commune_residence"] = datas["commune_residence"]
                    elif data == "date":
                        record["fields"]["date"] = datas["date"]
                    elif data == "date_reference":
                        record["fields"]["date_reference"] = datas["date_reference"]
                    elif data == "effectif_cumu_1_inj":
                        record["fields"]["effectif_cumu_1_inj"] = datas["effectif_cumu_1_inj"]
                    elif data == "effectif_cumu_termine":
                        record["fields"]["effectif_cumu_termine"] = datas["effectif_cumu_termine"]
                    elif data == "libelle_classe_age":
                        record["fields"]["libelle_classe_age"] = datas["libelle_classe_age"]
                    elif data == "libelle_commune":
                        record["fields"]["libelle_commune"] = datas["libelle_commune"]
                    elif data == "population_carto":
                        record["fields"]["population_carto"] = datas["population_carto"]
                    elif data == "semaine_injection":
                        record["fields"]["semaine_injection"] = datas["semaine_injection"]
                    elif data == "taux_1_inj":
                        record["fields"]["taux_1_inj"] = datas["taux_1_inj"]
                    elif data == "taux_cumu_1_inj":
                        record["fields"]["taux_cumu_1_inj"] = datas["taux_cumu_1_inj"]
                    elif data == "taux_cumu_termine":
                        record["fields"]["taux_cumu_termine"] = datas["taux_cumu_termine"]
                    elif data == "taux_termine":
                        record["fields"]["taux_termine"] = datas["taux_termine"]
                record["record_timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%F.%f")
                record_modifie = record
                return make_response(jsonify(record_modifie), 201)
        return make_response(jsonify({"message": "data not found"}), 404)


    def delete(self, id):
        """
        Supprimer une entrée
        ---
        tags:
          - restful
        parameters:
          - in: path
            name: id
            required: true
            description: L'identifiant de l'entrée (recordid)
            type: string
        responses:
          200: 
            description: L'entrée a été supprimée
          204:
            description: L'entrée voulu n'a pas été trouvé
        """
        global records
        find = False
        new_records = []
        # on cherche dans nos données un entrée avec le même identifiant que dans l'url
        for record in records:
            if record["recordid"] == id:
                find = True
                continue
            # on sauvegarde les données qui n'ont pas l'identifiant de l'url
            new_records.append(record)
        # on remplace les anciennes ddonénes par les nouvelles
        records = new_records
        if find == True:
          # on retourne un message de validation si une entrée a été supprimée
            return make_response(jsonify({"validation": "data deleted"}), 200)
        else:
          # sinon, onn retourne un message d'erreur
            return make_response(jsonify({"message": "data not found"}), 204)


class Commune(Resource):

    def get(self):
      """Retourne la liste des codes des communes
        ---
        tags:
          - restful
        responses:
          200:
            description: Liste des codes des communes (commune_code)
            schema:
              $ref: '#/definitions/donnees-de-vaccination'
      """
      global records
      communes = {"commune_code":[]}
      # on cherche dans nos données, les codes des communes
      for record in records:
          if record["fields"]["commune_residence"] not in communes["commune_code"]:
              communes["commune_code"].append(record["fields"]["commune_residence"])
      # on retourne au format json les codes des communes
      return make_response(jsonify(communes), 200)
    

class CodeCommune(Resource):

    def get(self, code_commune):
        """Retourne la liste des entrées du dataset suivant sa commune
        ---
        tags:
          - restful
        parameters:
          - in: path
            name: commune_code
            required: true
            description: Le code de la commune (commune_residence)
            type: string
        responses:
          200:
            description: Liste des entrées de la base de donnée suivant le libellé de commune
            schema:
              $ref: '#/definitions/donnees-de-vaccination'
        """
        global records
        sort_records = []
        # on cherche dans nos données les entrée ayant le même code commune que celui de l'url
        for record in records:
            if str(code_commune) == record["fields"]["commune_residence"]:
                sort_records.append(record)
        if sort_records == {}:
          # si aucun code_commune n'a été trouvé, on renvoie un message
            return make_response(jsonify({"message": "No data"}), 200)
        #sinon, on retourne en json la liste des codes dees communes
        return make_response(jsonify(sort_records), 200)


    def post(self, code_commune):
        """
        Ajouter une entrée
        ---
        tags:
          - restful
        parameters:
          - in: body
            name: body
            schema:
              $ref: '#/definitions/Entry'
          - in: path
            name: commune_code
            required: true
            description: Le code de la commune (commune_residence)
            type: string
        responses:
          201:
            description: L'entrée a été crée
            schema:
              $ref: '#/definitions/donnees-de-vaccination'
        """
        # on récupère les nouvelles données
        new_datas = request.json
        # on fait des vérifications sur ces nouvelles données
        if "commune_residence" in new_datas.keys() and new_datas["commune_residence"] != code_commune:
            return make_response(jsonify({"message": "your entry's code_commune and the dataset one doesn't match "}), 400)
        # on met en forme ces nouvelles données suivant le format de nos données (en respectant bien le type des données)
        rec = {'datasetid': "donnees-de-vaccination-par-commune",
               "fields": {
                   "classe_age": "",
                   "commune_residence": "",
                   "date": "",
                   "date_reference": "",
                   "effectif_cumu_1_inj": 0,
                   "effectif_cumu_termine": 0,
                   "libelle_classe_age": "",
                   "libelle_commune": "",
                   "population_carto": 0,
                   "semaine_injection": "",
                   "taux_1_inj": 0,
                   "taux_cumu_1_inj": 0,
                   "taux_cumu_termine": 0,
                   "taux_termine": 0}
               }
        if "commune_residence" not in new_datas.keys():
            rec["fields"]["commune_residence"] = code_commune
        # on génère un identifiant à ces données
        new_datas["recordid"] = generation_id()
        for data in new_datas.keys():
            if data == "recordid":
                rec["recordid"] = new_datas["recordid"]
            elif data == "classe_age":
                rec["fields"]["classe_age"] = new_datas["classe_age"]
            elif data == "commune_residence":
                rec["fields"]["commune_residence"] = new_datas["commune_residence"]
            elif data == "date":
                rec["fields"]["date"] = new_datas["date"]
            elif data == "date_reference":
                rec["fields"]["date_reference"] = new_datas["date_reference"]
            elif data == "effectif_cumu_1_inj":
                rec["fields"]["effectif_cumu_1_inj"] = new_datas["effectif_cumu_1_inj"]
            elif data == "effectif_cumu_termine":
                rec["fields"]["effectif_cumu_termine"] = new_datas["effectif_cumu_termine"]
            elif data == "libelle_classe_age":
                rec["fields"]["libelle_classe_age"] = new_datas["libelle_classe_age"]
            elif data == "libelle_commune":
                rec["fields"]["libelle_commune"] = new_datas["libelle_commune"]
            elif data == "population_carto":
                rec["fields"]["population_carto"] = new_datas["population_carto"]
            elif data == "semaine_injection":
                rec["fields"]["semaine_injection"] = new_datas["semaine_injection"]
            elif data == "taux_1_inj":
                rec["fields"]["taux_1_inj"] = new_datas["taux_1_inj"]
            elif data == "taux_cumu_1_inj":
                rec["fields"]["taux_cumu_1_inj"] = new_datas["taux_cumu_1_inj"]
            elif data == "taux_cumu_termine":
                rec["fields"]["taux_cumu_termine"] = new_datas["taux_cumu_termine"]
            elif data == "taux_termine":
                rec["fields"]["taux_termine"] = new_datas["taux_termine"]
            rec["record_timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%F.%f")
        # on ajoute les nouvelles données à nos données
        global records
        records.append(rec)
        # on retourne les nouvelles données au bon format
        return make_response(jsonify(rec), 201)


    def put(self, code_commune):
        """
        Modifier une entrée
        ---
        tags:
          - restful
        parameters:
          - in: body
            name: body
            schema:
              id: Entry2
              properties:
                recordid:
                  type: string
                classe_age:
                    type: string
                    exemple: 65-74
                libelle_commune:
                    type: string
                    exemple: MONTANAY
                date_reference:
                    type: string
                    exemple: 2022-03-06
                taux_cumu_1_inj:
                    type: float
                    exemple: 0.963
                population_carto:
                    type: integer
                    exemple: 380
                date:
                    type: string
                    exemple: 2021-11-14
                semaine_injection:
                    type: string
                    exemple: 2021-45
                libelle_classe_age:
                    type: string
                    exemple: de 65 à 74 ans
                effectif_cumu_1_inj:
                    type: integer
                    exemple: 360
                effectif_cumu_termine:
                    type: integer
                    exemple: 360
                taux_cumu_termine:
                    type: float
                    exemple: 0.96
                taux_termine:
                    type: float
                    exemple: 0.003
                taux_1_inj:
                    type: float
                    exemple: 0.006
          - in: path
            name: commune_code
            required: true
            description: Le code de la commune (commune_residence)
            type: string
        responses:
          201:
            description: L'entrée a été modifié
            schema:
              $ref: '#/definitions/donnees-de-vaccination'
          204:
            description: recordid n'a pas été trouvé dans les données d'entrées ou dans la base de données
        """
        global records
        # on récupère les modifications à apporter
        datas = request.json
        # on vérifie qu'il y a bien un identifiant
        if "recordid" not in datas.keys():
            return make_response(jsonify({"message": "not recordid in the new entry"}), 204)
        # on apporte les modifications
        for record in records:
            if record["recordid"] == datas["recordid"]:
                for data in datas.keys():
                    if data == "classe_age":
                        record["fields"]["classe_age"] = datas["classe_age"]
                    elif data == "commune_residence":
                        record["fields"]["commune_residence"] = datas["commune_residence"]
                    elif data == "date":
                        record["fields"]["date"] = datas["date"]
                    elif data == "date_reference":
                        record["fields"]["date_reference"] = datas["date_reference"]
                    elif data == "effectif_cumu_1_inj":
                        record["fields"]["effectif_cumu_1_inj"] = datas["effectif_cumu_1_inj"]
                    elif data == "effectif_cumu_termine":
                        record["fields"]["effectif_cumu_termine"] = datas["effectif_cumu_termine"]
                    elif data == "libelle_classe_age":
                        record["fields"]["libelle_classe_age"] = datas["libelle_classe_age"]
                    elif data == "libelle_commune":
                        record["fields"]["libelle_commune"] = datas["libelle_commune"]
                    elif data == "population_carto":
                        record["fields"]["population_carto"] = datas["population_carto"]
                    elif data == "semaine_injection":
                        record["fields"]["semaine_injection"] = datas["semaine_injection"]
                    elif data == "taux_1_inj":
                        record["fields"]["taux_1_inj"] = datas["taux_1_inj"]
                    elif data == "taux_cumu_1_inj":
                        record["fields"]["taux_cumu_1_inj"] = datas["taux_cumu_1_inj"]
                    elif data == "taux_cumu_termine":
                        record["fields"]["taux_cumu_termine"] = datas["taux_cumu_termine"]
                    elif data == "taux_termine":
                        record["fields"]["taux_termine"] = datas["taux_termine"]
                record["record_timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%F.%f")
                record_modifie = record
                # on retourne l'entrée modifié
                return make_response(jsonify(record_modifie), 201)
        # s'il n'y a pas eu de return avant, c'est qu'aucune entrée ne correspond à l'identifiant entrée
        return make_response(jsonify({"message": "recordid not found"}), 204)


class SemaineListe(Resource):

    def get(self,code_commune):
        """Retourne la liste des semaines d'injections
        ---
        tags:
          - restful
        parameters:
          - in: path
            name: code_commune
            type: string
            description: le code de la commune (commune_residence)
        responses:
          200:
            description: Liste des semaines d'injections (semaine_injection)
            schema:
              $ref: '#/definitions/donnees-de-vaccination'
        """
        global records
        semaine_liste = {"semaine_injection":[]}
        # on cherche la liste des semaines d'injection enrigistré dans la commune donnée en url:
        for record in records:
            if record["fields"]["semaine_injection"] not in semaine_liste["semaine_injection"] and code_commune == record["fields"]["commune_residence"]:
                semaine_liste["semaine_injection"].append(record["fields"]["semaine_injection"])
        # on retourne ce qui a été trouvé
        return make_response(jsonify(semaine_liste), 200)


class Semaine(Resource):

    def get(self, code_commune, semaine):
        """Retourne la liste des entrées du dataset suivant sa commune et la semaine d'injection
        ---
        tags:
          - restful
        parameters:
          - in: path
            name: code_commune
            required: true
            description: le code de la commune(commune_residence)
            type: string
          - in: path
            name: semaine
            required: true
            description: la semaine d'injection (semaine_injection)
            type: string
        responses:
          200:
            description: Liste des entrées de la base de donnée suivant la  semaine d'injection
            schema:
              $ref: '#/definitions/donnees-de-vaccination'
        """
        global records
        sort_records = []
        # on cherche les entrées enrigistré de la commune et de la semaine d'injection données en url:
        for record in records:
            if str(code_commune) == record["fields"]["commune_residence"] and str(semaine) == record["fields"]["semaine_injection"]:
                sort_records.append(record)
        # si aucune entrée a été trouvé: on retourne un message
        if sort_records == {}:
            return make_response(jsonify({"message": "No data"}), 200)
        # sinon, onn retourne ce qui a été trouvé
        return make_response(jsonify(sort_records), 200)


    def post(self, code_commune, semaine):
        """
        Ajouter une entrée
        ---
        tags:
          - restful
        parameters:
          - in: body
            name: body
            schema:
              $ref: '#/definitions/Entry'
          - in: path
            name: code_commune
            required: true
            description: le code de la commune (commune_residence)
            type: string
          - in: path
            name: semaine
            required: true
            description: la semaine d'injection (semaine_injection)
            type: string
        responses:
          201:
            description: L'entrée a été crée
            schema:
              $ref: '#/definitions/donnees-de-vaccination'
        """
        # on récupère les nouvelles données
        new_datas = request.json
        # on fait des vérifications sur ces nouvelles données
        if "commune_residence" in new_datas.keys() and new_datas["commune_residence"] != code_commune:
            return make_response(jsonify({"message": "your entry's code_commune and the dataset one doesn't match "}), 400)
        if "semaine_injection" in new_datas.keys() and new_datas["semaine_injection"] != semaine:
            return make_response(jsonify({"message": "your entry's code_commune and the dataset one doesn't match "}), 400)
        # on met en forme ces nouvelles données suivant le format de nos données (en respectant bien le type des données)
        rec = {'datasetid': "donnees-de-vaccination-par-commune",
               "fields": {
                   "classe_age": "",
                   "commune_residence": "",
                   "date": "",
                   "date_reference": "",
                   "effectif_cumu_1_inj": 0,
                   "effectif_cumu_termine": 0,
                   "libelle_classe_age": "",
                   "libelle_commune": "",
                   "population_carto": 0,
                   "semaine_injection": "",
                   "taux_1_inj": 0,
                   "taux_cumu_1_inj": 0,
                   "taux_cumu_termine": 0,
                   "taux_termine": 0}
               }
        if "commune_residence" not in new_datas.keys():
            rec["fields"]["commune_residence"] = code_commune
        if "semaine_injection" not in new_datas.keys():
            rec["fields"]["semaine_injection"] = semaine
        # on génère un identifiant à ces données
        new_datas["recordid"] = generation_id()
        for data in new_datas.keys():
            if data == "recordid":
                rec["recordid"] = new_datas["recordid"]
            elif data == "classe_age":
                rec["fields"]["classe_age"] = new_datas["classe_age"]
            elif data == "commune_residence":
                rec["fields"]["commune_residence"] = new_datas["commune_residence"]
            elif data == "date":
                rec["fields"]["date"] = new_datas["date"]
            elif data == "date_reference":
                rec["fields"]["date_reference"] = new_datas["date_reference"]
            elif data == "effectif_cumu_1_inj":
                rec["fields"]["effectif_cumu_1_inj"] = new_datas["effectif_cumu_1_inj"]
            elif data == "effectif_cumu_termine":
                rec["fields"]["effectif_cumu_termine"] = new_datas["effectif_cumu_termine"]
            elif data == "libelle_classe_age":
                rec["fields"]["libelle_classe_age"] = new_datas["libelle_classe_age"]
            elif data == "libelle_commune":
                rec["fields"]["libelle_commune"] = new_datas["libelle_commune"]
            elif data == "population_carto":
                rec["fields"]["population_carto"] = new_datas["population_carto"]
            elif data == "semaine_injection":
                rec["fields"]["semaine_injection"] = new_datas["semaine_injection"]
            elif data == "taux_1_inj":
                rec["fields"]["taux_1_inj"] = new_datas["taux_1_inj"]
            elif data == "taux_cumu_1_inj":
                rec["fields"]["taux_cumu_1_inj"] = new_datas["taux_cumu_1_inj"]
            elif data == "taux_cumu_termine":
                rec["fields"]["taux_cumu_termine"] = new_datas["taux_cumu_termine"]
            elif data == "taux_termine":
                rec["fields"]["taux_termine"] = new_datas["taux_termine"]
            rec["record_timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%F.%f")
        # on ajoute les nouvelles données à nos données
        global records
        records.append(rec)
        # on retourne les nouvelles données au bon format
        return make_response(jsonify(rec), 201)


    def put(self, code_commune, semaine):
        """
        Modifier une entrée
        ---
        tags:
          - restful
        parameters:
          - in: body
            name: body
            schema:
              $ref: '#/definitions/Entry2'
          - in: path
            name: code_commune
            required: true
            description: le code de la commune(commune_residence)
            type: string
          - in: path
            name: semaine
            required: true
            description: la semaine d'injection (semaine_injection)
            type: string
        responses:
          201:
            description: L'entrée a été modifié
            schema:
              $ref: '#/definitions/donnees-de-vaccination'
          204:
            description: recordid n'a pas été trouvé dans les données d'entrées ou dans la base de donnée
        """
        global records
        # on récupère les modifications à apporter
        datas = request.json
        # on vérifie qu'il y a bien un identifiant
        if "recordid" not in datas.keys():
            return make_response(jsonify({"message": "not recordid in the new entry"}), 204)
        # on apporte les modifications
        for record in records:
            if record["recordid"] == datas["recordid"]:
                for data in datas.keys():
                    if data == "classe_age":
                        record["fields"]["classe_age"] = datas["classe_age"]
                    elif data == "commune_residence":
                        record["fields"]["commune_residence"] = datas["commune_residence"]
                    elif data == "date":
                        record["fields"]["date"] = datas["date"]
                    elif data == "date_reference":
                        record["fields"]["date_reference"] = datas["date_reference"]
                    elif data == "effectif_cumu_1_inj":
                        record["fields"]["effectif_cumu_1_inj"] = datas["effectif_cumu_1_inj"]
                    elif data == "effectif_cumu_termine":
                        record["fields"]["effectif_cumu_termine"] = datas["effectif_cumu_termine"]
                    elif data == "libelle_classe_age":
                        record["fields"]["libelle_classe_age"] = datas["libelle_classe_age"]
                    elif data == "libelle_commune":
                        record["fields"]["libelle_commune"] = datas["libelle_commune"]
                    elif data == "population_carto":
                        record["fields"]["population_carto"] = datas["population_carto"]
                    elif data == "semaine_injection":
                        record["fields"]["semaine_injection"] = datas["semaine_injection"]
                    elif data == "taux_1_inj":
                        record["fields"]["taux_1_inj"] = datas["taux_1_inj"]
                    elif data == "taux_cumu_1_inj":
                        record["fields"]["taux_cumu_1_inj"] = datas["taux_cumu_1_inj"]
                    elif data == "taux_cumu_termine":
                        record["fields"]["taux_cumu_termine"] = datas["taux_cumu_termine"]
                    elif data == "taux_termine":
                        record["fields"]["taux_termine"] = datas["taux_termine"]
                record["record_timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%F.%f")
                record_modifie = record
                # on retourne l'entrée modifié
                return make_response(jsonify(record_modifie), 201)
        # s'il n'y a pas eu de return avant, c'est qu'aucune entrée ne correspond à l'identifiant entrée
        return make_response(jsonify({"message": "recordid not found"}), 204)


class ClasseAgeListe(Resource):

    def get(self, code_commune, semaine):
        """Retourne la liste des classes d'age
        ---
        tags:
          - restful
        parameters:
          - in: path
            name: code_commune
            required: true
            description: le code de la commune(commune_residence)
            type: string
          - in: path
            name: semaine_injection
            required: true
            description: le numéro de la semaine d'injection
            type: string
        responses:
          200:
            description: Liste des classes d'age (classe_age)
            schema:
              $ref: '#/definitions/donnees-de-vaccination'
        """
        global records
        classe_liste = {"classe_age":[]}
        # on cherche la liste des classes d'âge présent dans la commune et la semaine d'injection donnée en url
        for record in records:
          if record["fields"]["classe_age"] not in classe_liste["classe_age"] and code_commune == record["fields"]["commune_residence"] and semaine == record["fields"]["semaine_injection"]:
              classe_liste["classe_age"].append(record["fields"]["classe_age"])
        # on retourne ce qui a été trouvé
        return make_response(jsonify(classe_liste), 200)


class ClasseAge(Resource):

    def get(self, code_commune, semaine, classe_age):
        """Retourne la liste des entrées du dataset suivant sa commune, la semaine d'injection et sa classe d'age
        ---
        tags:
          - restful
        parameters:
          - in: path
            name: code_commune
            required: true
            description: le code de la commune(commune_residence)
            type: string
          - in: path
            name: semaine
            required: true
            description: la semaine d'injection (semaine_injection)
            type: string
          - in: path
            name: classe_age
            required: true
            description: la classe d'age s(classe_age)
            type: string
        responses:
          200:
            description: Liste des entrées de la base de donnée suivant le code de la commune, la semaine d'injection et sa classe d'age
            schema:
              $ref: '#/definitions/donnees-de-vaccination'
        """
        global records
        sort_records = []
        # on cherche dans les données, les entrées ayaant
        # les mêmes commune_residence, semaine_injection et classe_age que ceux dans l'url
        for record in records:
            if str(code_commune) == record["fields"]["commune_residence"] and str(semaine) == record["fields"]["semaine_injection"] and str(classe_age) == record["fields"]["classe_age"]:
                sort_records.append(record)
        # si il n'y en a pas, on retourne un message d'erreur
        if sort_records == []:
            return make_response(jsonify({"message": "No data"}), 200)
        # sinon, on les retourne au format json
        return make_response(jsonify(sort_records), 200)


    def post(self, code_commune, semaine, classe_age):
        """
        Ajouter une entrée
        ---
        tags:
          - restful
        parameters:
          - in: body
            name: body
            schema:
              $ref: '#/definitions/Entry'
          - in: path
            name: code_commune
            required: true
            description: le code de la commune(commune_residence)
            type: string
          - in: path
            name: semaine
            required: true
            description: la semaine d'injection (semaine_injection)
            type: string
          - in: path
            name: classe_age
            required: true
            description: la classe d'age (classe_age)
            type: string
        responses:
          201:
            description: L'entrée a été crée
            schema:
              $ref: '#/definitions/donnees-de-vaccination'
        """
        # on récupère les nouvelles données
        new_datas = request.json
        # on fait quelques vérifications sur les données
        if "commune_residence" in new_datas.keys() and new_datas["commune_residence"] != code_commune:
            return make_response(jsonify({"message": "your entry's code_commune and the dataset one doesn't match "}), 400)
        if "semaine_injection" in new_datas.keys() and new_datas["semaine_injection"] != semaine:
            return make_response(jsonify({"message": "your entry's code_commune and the dataset one doesn't match "}), 400)
        if "classe_age" in new_datas.keys() and new_datas["classe_age"] != classe_age:
            return make_response(jsonify({"message": "your entry's code_commune and the dataset one doesn't match "}), 400)
        # on met en forme ces nouvelles données suivant le format de nos données (en respectant bien le type des données)
        rec = {'datasetid': "donnees-de-vaccination-par-commune",
               "fields": {
                   "classe_age": "",
                   "commune_residence": "",
                   "date": "",
                   "date_reference": "",
                   "effectif_cumu_1_inj": 0,
                   "effectif_cumu_termine": 0,
                   "libelle_classe_age": "",
                   "libelle_commune": "",
                   "population_carto": 0,
                   "semaine_injection": "",
                   "taux_1_inj": 0,
                   "taux_cumu_1_inj": 0,
                   "taux_cumu_termine": 0,
                   "taux_termine": 0}
               }
        if "commune_residence" not in new_datas.keys():
            rec["fields"]["commune_residence"] = code_commune
        if "semaine_injection" not in new_datas.keys():
            rec["fields"]["semaine_injection"] = semaine
        if "classe_age" not in new_datas.keys():
            rec["fields"]["classe_age"] = classe_age
        # on génère un identifiant à ces données
        new_datas["recordid"] = generation_id()
        for data in new_datas.keys():
            if data == "recordid":
                rec["recordid"] = new_datas["recordid"]
            elif data == "classe_age":
                rec["fields"]["classe_age"] = new_datas["classe_age"]
            elif data == "commune_residence":
                rec["fields"]["commune_residence"] = new_datas["commune_residence"]
            elif data == "date":
                rec["fields"]["date"] = new_datas["date"]
            elif data == "date_reference":
                rec["fields"]["date_reference"] = new_datas["date_reference"]
            elif data == "effectif_cumu_1_inj":
                rec["fields"]["effectif_cumu_1_inj"] = new_datas["effectif_cumu_1_inj"]
            elif data == "effectif_cumu_termine":
                rec["fields"]["effectif_cumu_termine"] = new_datas["effectif_cumu_termine"]
            elif data == "libelle_classe_age":
                rec["fields"]["libelle_classe_age"] = new_datas["libelle_classe_age"]
            elif data == "libelle_commune":
                rec["fields"]["libelle_commune"] = new_datas["libelle_commune"]
            elif data == "population_carto":
                rec["fields"]["population_carto"] = new_datas["population_carto"]
            elif data == "semaine_injection":
                rec["fields"]["semaine_injection"] = new_datas["semaine_injection"]
            elif data == "taux_1_inj":
                rec["fields"]["taux_1_inj"] = new_datas["taux_1_inj"]
            elif data == "taux_cumu_1_inj":
                rec["fields"]["taux_cumu_1_inj"] = new_datas["taux_cumu_1_inj"]
            elif data == "taux_cumu_termine":
                rec["fields"]["taux_cumu_termine"] = new_datas["taux_cumu_termine"]
            elif data == "taux_termine":
                rec["fields"]["taux_termine"] = new_datas["taux_termine"]
            rec["record_timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%F.%f")
        # on ajoute les nouvelles données à nos données
        global records
        records.append(rec)
        # on retourne les nouvelles données au bon format
        return make_response(jsonify(rec), 201)


    def put(self, code_commune, semaine, classe_age):
        """
        Modifier une entrée
        ---
        tags:
          - restful
        parameters:
          - in: body
            name: body
            schema:
              $ref: '#/definitions/Entry2'
          - in: path
            name: code_commune
            required: true
            description: le code de la commune(commune_residence)
            type: string
          - in: path
            name: semaine
            required: true
            description: la semaine d'injection (semaine_injection)
            type: string
          - in: path
            name: classe_age
            required: true
            description: la classe d'age (classe_age)
            type: string
        responses:
          201:
            description: L'entrée a été modifié
            schema:
              $ref: '#/definitions/donnees-de-vaccination'
          204:
            description: recordid n'a pas été trouvé dans les données d'entrées ou dans les données de la base de donnée
        """
        global records
        # on récupère les modifications à apporter
        datas = request.json
        # on vérifie qu'il y a bien un identifiant
        if "recordid" not in datas.keys():
            return make_response(jsonify({"message": "not recordid in the new entry"}), 204)
        # on apporte les modifications
        for record in records:
            if record["recordid"] == datas["recordid"]:
                for data in datas.keys():
                    if data == "classe_age":
                        record["fields"]["classe_age"] = datas["classe_age"]
                    elif data == "commune_residence":
                        record["fields"]["commune_residence"] = datas["commune_residence"]
                    elif data == "date":
                        record["fields"]["date"] = datas["date"]
                    elif data == "date_reference":
                        record["fields"]["date_reference"] = datas["date_reference"]
                    elif data == "effectif_cumu_1_inj":
                        record["fields"]["effectif_cumu_1_inj"] = datas["effectif_cumu_1_inj"]
                    elif data == "effectif_cumu_termine":
                        record["fields"]["effectif_cumu_termine"] = datas["effectif_cumu_termine"]
                    elif data == "libelle_classe_age":
                        record["fields"]["libelle_classe_age"] = datas["libelle_classe_age"]
                    elif data == "libelle_commune":
                        record["fields"]["libelle_commune"] = datas["libelle_commune"]
                    elif data == "population_carto":
                        record["fields"]["population_carto"] = datas["population_carto"]
                    elif data == "semaine_injection":
                        record["fields"]["semaine_injection"] = datas["semaine_injection"]
                    elif data == "taux_1_inj":
                        record["fields"]["taux_1_inj"] = datas["taux_1_inj"]
                    elif data == "taux_cumu_1_inj":
                        record["fields"]["taux_cumu_1_inj"] = datas["taux_cumu_1_inj"]
                    elif data == "taux_cumu_termine":
                        record["fields"]["taux_cumu_termine"] = datas["taux_cumu_termine"]
                    elif data == "taux_termine":
                        record["fields"]["taux_termine"] = datas["taux_termine"]
                record["record_timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%F.%f")
                record_modifie = record
                # on retourne l'entrée modifié
                return make_response(jsonify(record_modifie), 201)
        # s'il n'y a pas eu de return avant, c'est qu'aucune entrée ne correspond à l'identifiant entrée
        return make_response(jsonify({"message": "recordid not found"}), 204)


# Fonction qui se déclanche toute les 24h
@scheduler.task('interval', id='do_job_1', hours=24, misfire_grace_time=900)
def job1():
    global date, records

    # si la date actuel est supérieur à la date en mémoire
    if date < datetime.datetime.now():
        ndate=date.strftime('%Y-%W') # numéro de la semaine de l'année
        
        # et si le numéro de semaine est différent
        if ndate != datetime.datetime.now().strftime('%Y-%W'):
            # on requête pour chercher le nombre d'entrée pour la semaine
            r1 = requests.get(f'https://datavaccin-covid.ameli.fr/api/records/1.0/search/?dataset=donnees-de-vaccination-par-commune&q=&rows=10&refine.semaine_injection={ndate}')
            
            n = r1.json().get("nhits") # nombre de nouvelles entrées
            
            # on cherche l'ensemble des nouvelles entrées
            r2 = requests.get(f'https://datavaccin-covid.ameli.fr/api/records/1.0/search/?dataset=donnees-de-vaccination-par-commune&q=&rows={n}&refine.semaine_injection={ndate}')

            # on met à jour la base de donnée en mémoire
            datas = r2.json().get("records")
            for record in datas:
                records.append(record)
        
        # on met à jour la base de donnée json
        with open("./datas/donnees-de-vaccination-par-commune_reduit.json", "w") as f:
            f.write(json.dumps(records, ensure_ascii=False))
        print('Data Base updated')
    
    # on sauvegarde en mémoire la date de la dernière mis à jour
    date = datetime.datetime.now()


@app.route('/')
def index():
    return render_template('index.html')
    

api.add_resource(DonneesCommune, '/apidocs/vaccination')
api.add_resource(DonneeCommune, '/apidocs/vaccination/<string:id>')
api.add_resource(Commune, '/apidocs/vaccination/commune')
api.add_resource(CodeCommune, '/apidocs/vaccination/commune/<string:code_commune>')
api.add_resource(SemaineListe, '/apidocs/vaccination/commune/<string:code_commune>/semaine')
api.add_resource(Semaine, '/apidocs/vaccination/commune/<string:code_commune>/semaine/<string:semaine>')
api.add_resource(ClasseAgeListe, '/apidocs/vaccination/commune/<string:code_commune>/semaine/<string:semaine>/classe_age')
api.add_resource(ClasseAge, '/apidocs/vaccination/commune/<string:code_commune>/semaine/<string:semaine>/classe_age/<string:classe_age>')


if __name__ == '__main__':
    scheduler.start()
    app.run(use_reloader=False, debug=True)

