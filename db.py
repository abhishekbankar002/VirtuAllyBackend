import base64
import datetime

from pymongo import MongoClient
from VTryon import settings
import jwt

client = MongoClient('mongodb://localhost:27017/')

mydb = client["VTryon"]

users = mydb['users']

users.create_index('date', expireAfterSeconds=60)


def writeDB(obj):
    userinfo = users.find()
    for user in userinfo:
        if (user['email'] == obj['email']):
            return ("Not Created", "")
    token = jwt.encode(
        {
            'email': obj['email'],
            'password': obj['password']
        },
        settings.SECRET_KEY,
        algorithm="HS256"
    )

    # print(token)
    #
    # decoded_token = jwt.decode(token,
    #                            settings.SECRET_KEY,
    #                            algorithms=['HS256'])
    #
    # print(decoded_token['email'])
    users.insert_one({'email': obj['email'], 'password': token})
    return ("Created", token)


def Login_DB(obj):
    userinfo = users.find()
    for user in userinfo:
        if (user['email'] == obj['email']):
            if (user['password'] == obj['password']):
                # token= jwt.encode(
                #     {
                #         'email':obj['email'],
                #     },
                #     settings.SECRET_KEY,
                #     algorithm="HS256"
                # )
                # print(token)
                # return(["True",token])
                return ("True", user["email"])
    return ("False", obj['email'])


def saveImage(file):
    sample_string_bytes = file.read()
    image = {
        'data': sample_string_bytes
    }
    timestamp = datetime.datetime.utcnow()
    users.storage.insert_one({'email': 'ac@32341123', 'image': image, "date": timestamp})
    return ("Success")


def checkLogIn(obj):
    userinfo = users.find()
    decoded_token = jwt.decode(obj['token'],
                               settings.SECRET_KEY,
                               algorithms=['HS256'])
    print(decoded_token['email'])
    print(decoded_token['password'])
    print(obj['token'])
    for user in userinfo:
        if (user['email'] == decoded_token['email'] and user['password'] == obj['token']):
            print(decoded_token['email'])
            print(decoded_token['password'])
            return True
    return False

