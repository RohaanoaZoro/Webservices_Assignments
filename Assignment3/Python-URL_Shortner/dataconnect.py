from pymongo import MongoClient
import mysql.connector


def MongoDatabaseConnect():
    #client = MongoClient('mongodb://uva-devops-api:Ysl6nuTUn1TTHlskJuGCkBycbYHembMm1fJm1VfrrcHjdYjSYX8co3e7TS2yWkiNrTwOlcLGsl7NACDbRVyvOQ==@uva-devops-api.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@uva-devops-api@')
    client = MongoClient('172.25.0.3', 27017)
    db = client.tinyUrl
    return db

def MySQLConnect():
    # connect to database
    cnx = mysql.connector.connect(user='root', password='Zxcvbnm@2',host='172.25.0.2', database='Oauth2')

    return cnx
