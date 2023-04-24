from dataconnect import MongoDatabaseConnect, MySQLConnect
import json
import bson.json_util as json_util
from bson import ObjectId

mongoDB = MongoDatabaseConnect()
MySQLCnx = MySQLConnect()

ApplicationID = "3e2d3f52-07d9-4163-94ce-df29819685f7"

# Adding sid and url to database
def addUrlToDb(sid, url, colname):
    try:
        mongoDB[colname].insert_one({
            'sid': sid,
            'uid': url
        })
    except:
        return -1
    return 0

# Check if sid is present based on mathcing the initial regex
def getMatchedURLs(shortid, colname):
    urls = mongoDB[colname].find({'sid': { "$regex" : '^'+ shortid}}, {"_id":0})
    return urls

# find sid in database
def findURLInDB(shortid, colname):
    urls = mongoDB[colname].find({'sid': shortid}, {"_id":0})
    return urls

# Update the URL for sid in database
def updateUrl(shortid, colname, new_url):
    doc = mongoDB[colname].find_one({'sid': shortid})
    # get new url from request data
    if (doc != None):
        # try to update, and if it does not work return 400 with "error"
        try:
            mongoDB[colname].update_one({'sid': shortid}, {"$set": {'uid': new_url}})
            return {"new_url": new_url}, 200
        except:
            return "error ", 400
    return {"error_msg":"Collection with that id does not exist"}, 404

# Get all url in collection
def getAllURLs(colname):
    urls = mongoDB[colname].find({}, {"_id":0})
    return urls

# Get all collections
def getCollections():
    collections = mongoDB.list_collection_names()
    return collections

# Delete Url in database
def deleteUrl(colname, shortid):
    res = list(mongoDB[colname].find({'sid': shortid}, {"_id":1}))
    if res:
        # Converting to the JSON
        mongoid = res[0]["_id"]
        mongoDB[colname].delete_one({"_id": ObjectId(mongoid)})
    
        return 204
    else:
        return 404

def getJwtKeys():

    # create a cursor object
    cursor = MySQLCnx.cursor()

    # execute a SELECT query to fetch multiple rows
    query = ('SELECT JWTKey FROM Oauth2.JWTKeys WHERE ApplicationId="'+ApplicationID+'"')
    cursor.execute(query)

    # fetch all the rows as a list of tuples
    rows = cursor.fetchall()

    # print the rows
    for row in rows:
        return row[0]

    # close the cursor and connection
    cursor.close()
