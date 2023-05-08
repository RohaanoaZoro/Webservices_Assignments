import re
import hashlib
from dataconnect import MongoDatabaseConnect
from database_functions import getMatchedURLs
import bson.json_util as json_util

# Regex we created to extract url parameters
dns_regex = '^(?:(https|http)?:\/\/)?(?:[^@\n]+@)?(?:\.)?([^:\/\n?]+)(.*)\?(.*)'

mongoDB = MongoDatabaseConnect()

# Substring the characters at index array
def extractCharacters(arr_of_indexes, char_string):
    result = ""
    for i in arr_of_indexes:
        result+= char_string[i:i+1]

    return result

# Creates the short id
def getShortId(_url):

    # Extract the groups from the domain
    regex_match_arr = re.match(dns_regex, _url)

    #Match output
    protocol = regex_match_arr.group(1)
    domain = regex_match_arr.group(2)
    domain_extension = regex_match_arr.group(3)
    excess_url_info = regex_match_arr.group(4)
    domain_split_info = domain.split(".")

    remainder_url = domain_extension + excess_url_info

    # Hash with 3 characters from domain name
    hash_first_3 = extractCharacters([0, int(len(domain_split_info[1])/2), len(domain_split_info[1])-1], domain_split_info[1])

    # Hash of 4 characters using md5 hash
    hash_next_3 = hashlib.md5(remainder_url.encode()).hexdigest()[:4]

    # Check in the database of there are any id collisions
    url_collection = getMatchedURLs(hash_first_3+hash_next_3, hash_first_3)

    # Adjust the if to incorporate the number of collisions
    hash_collisions=0
    for url in url_collection:
        print(url)
        hash_collisions+=1

    # Return based on the collisions occred
    if hash_collisions>0:
        return hash_first_3+hash_next_3+str(hash_collisions)
    else:
        return hash_first_3+hash_next_3