from pymongo import MongoClient

def MongoDatabaseConnect():
    #client = MongoClient('mongodb://uva-devops-api:Ysl6nuTUn1TTHlskJuGCkBycbYHembMm1fJm1VfrrcHjdYjSYX8co3e7TS2yWkiNrTwOlcLGsl7NACDbRVyvOQ==@uva-devops-api.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@uva-devops-api@')
    client = MongoClient('localhost', 27017)
    db = client.tinyUrl
    return db