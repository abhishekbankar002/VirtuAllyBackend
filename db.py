import base64
import io
import os

from bson.binary import Binary
import datetime

from pymongo import MongoClient
from VTryon import settings
import jwt
from PIL import Image

client = MongoClient('mongodb://localhost:27017/')

mydb = client["VTryon"]

users = mydb['users']

image_collection = mydb['imageCollection']

image_collection.create_index('date', expireAfterSeconds=600)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'myNewApp\\PFAFNModel\\dataset\\test_img')

def writeDB(obj):
    userinfo = users.find()
    for user in userinfo:
        if (user['email'] == obj['email']):
            print("Not Created")
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
    print(token)
    users.insert_one({'email': obj['email'], 'password': token})
    return ("Created", token)


def Login_DB(obj):
    userinfo = users.find()
    for user in userinfo:
        if (user['email'] == obj['email']):
            if (user['password'] == obj['password']):
                return ("True", user["email"])
    return ("False", obj['email'])


def saveImage(request):
    token = request.POST.get('token')
    userinfo = users.find()
    decoded_token = jwt.decode(token,
                               settings.SECRET_KEY,
                               algorithms=['HS256'])
    image_file = request.FILES['queryImage']
    # pil_img = Image.open(image_file)
    # pil_img.show()
    image_file.seek(0)
    sample_string_bytes = request.FILES['queryImage'].read()
    for user in userinfo:
        if (user['email'] == decoded_token['email'] and user['password'] == token):
            image = {
                'data': sample_string_bytes
            }
            timestamp = datetime.datetime.utcnow()
            image_collection.update({'email': user['email']}, {'email': user['email'], 'image': image, "date": timestamp}, upsert=True)
            return True
    return False

    return ("Success")


def checkLogIn(obj):
    userinfo = users.find()
    print(obj['token'])
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

def loadImage(obj):
    print(obj)
    decoded_token = jwt.decode(obj['token'],
                               settings.SECRET_KEY,
                               algorithms=['HS256'])
    print(decoded_token['email'])
    imageInfo = image_collection.find()
    file_path = os.path.join(UPLOAD_FOLDER, f'{decoded_token["email"]}.jpg')
    for user in imageInfo:
        if (user['email'] == decoded_token['email']):
            with open(file_path, 'wb') as f:
                pil_img = Image.open(io.BytesIO(user['image']['data']))
                pil_img.show()
                pil_img.save(file_path)
                # f.write(io.BytesIO(user['image']['data']))
                return f'{decoded_token["email"]}.jpg'
    return ''