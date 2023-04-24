from flask import Flask, request, redirect
from database_functions import addUrlToDb, getCollections, getAllURLs, findURLInDB, deleteUrl, updateUrl, getJwtKeys

from flask_cors import cross_origin

from short_url import getShortId, dns_regex

from decode_token import verify_jwt

import re
from cache import Cache

import time

app = Flask(__name__)

secretKey = ""

#This is the regex we refrenced from stackoverflow
regex_match = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'

sid_cache = Cache(5)

#This is the GET method with id
@app.route('/<id>', methods = ['GET'])
@cross_origin()
def getSingleUrl(id):

    token=""
    if "Authorization" in request.headers:
        token = request.headers["Authorization"][7:]

    claims, err = verify_jwt(token, secretKey)
    if err :
        return claims, 403
    
    if token == "":
        return {"error_msg": "Missing Token in Header"}

    try:
        # This returns a list with a single url
        singleurl = list(findURLInDB(id, id[:3]))
    except:
        # Throws an exception if something goes wrong in list conversion
        return {"error_msg": "Could not find id provided"}, 404

    if len(singleurl) > 0:
        # The successful redirect with 301 status code
        # return redirect(singleurl[0]["uid"], 301)
        return {"url":singleurl[0]["uid"]}, 301
    else:
        # Error messsage if url was not found
        return {"error_msg": "Could not find id provided"}, 404

#This is the GET method without id
@app.route('/', methods = ['GET'])
@cross_origin()
def getAllUrls():
    token=""
    if "Authorization" in request.headers:
        token = request.headers["Authorization"][7:]

    claims, err = verify_jwt(token, secretKey)
    if err :
        return claims, 403
    
    if token == "":
        return {"error_msg": "Missing Token in Header"}

    # We get all the collection names 
    collections = getCollections()
    allurls = []

    # Iteratively we get all the URLs per collection
    for col in collections:
        allurls += list(getAllURLs(col))

    #We return the list of urls with status code 200
    return allurls, 200

#This is the post method
@app.route('/', methods = ['POST'])
@cross_origin()
def addNewUrl():

    token=""
    if "Authorization" in request.headers:
        token = request.headers["Authorization"][7:]

    claims, err = verify_jwt(token, secretKey)
    if err :
        return claims, 403
    
    if token == "":
        return {"error_msg": "Missing Token in Header"}


    # Extract the json body from the request
    post_body = request.json

    # Error response if `url` property is not present in json schema
    if "url" not in post_body:
        return {"error_msg":"No `url` in json body"}, 400

    # We match the url to the regex we defined above
    isMatch = re.match(regex_match, post_body["url"])
    if isMatch == None:
        return {"error_msg":'Error while parsing the URL'}, 400

    # We get the short id
    shortId = getShortId(post_body["url"])

    # We add the short-id and url to the database
    status = addUrlToDb(shortId, post_body["url"], shortId[:3])

    # Error status if db insertion fails
    if status != 0:
        return {"error_msg":"Error while inserting into DB"}, 400
    
    # Success message with 201 response code
    return {"sid":shortId}, 201

#Delete with id
@app.route('/<id>', methods = ['DELETE'])
@cross_origin()
def deleteURL(id):

    token=""
    if "Authorization" in request.headers:
        token = request.headers["Authorization"][7:]

    claims, err = verify_jwt(token, secretKey)
    if err :
        return claims, 403
    
    if token == "":
        return {"error_msg": "Missing Token in Header"}

    #This is to handle multiple requests
    while sid_cache.check(id) != -1:
        print("sleeping")
        time.sleep(1)

    sid_cache.enqueue(id, "")

    # We get the status_code if we are able to delete the url
    res_code = deleteUrl(id[:3], id)

    sid_cache.deleteItem(id)


    # Success message if delete was sucessful with response code 204
    if res_code == 204:
        return "", 204
    
    # Error messsage if url was not found
    else:
        return {"error_msg":"Error could not find collection with that id"}, 404

@app.route('/', methods = ['DELETE'])
@cross_origin()
def deleteAllURLs():
    # Error messsage to not allow the execution of this method
    return {"error_msg":"missing `id` for deletion"}, 404

@app.route('/<id>', methods=['PUT'])
def updateById(id):

    token=""
    if "Authorization" in request.headers:
        token = request.headers["Authorization"][7:]

    claims, err = verify_jwt(token, secretKey)
    if err :
        return claims, 403
    
    if token == "":
        return {"error_msg": "Missing Token in Header"}
        
    # Extract the json body from the request
    updated = request.json["url"]

    # We match the url to the regex we defined above
    isMatch = re.match(regex_match, updated)
    if isMatch == None:
        return {"error_msg":'Error while parsing the URL'}, 400

    #This is to handle multiple requests
    while sid_cache.check(id) != -1:
        print("sleeping")
        time.sleep(1)

    sid_cache.enqueue(id, updated)

    # Success message with 201 response code
    response = updateUrl(id, id[:3], updated)

    sid_cache.deleteItem(id)

    return response

# main driver function
if __name__ == '__main__':

    # This is the cache 
    # cacheObj = Cache("n"+str(i), 256*(1024**3), 200) #NodeId, CacheSize(256GB), RetrievalTime(200ms)

    # run() method of Flask class runs the application
    # on the local development server.
    secretKey = getJwtKeys()
    app.run(host='0.0.0.0', port=5000)