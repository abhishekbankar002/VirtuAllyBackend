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

productsCollection = mydb['Products']

image_collection.create_index('date', expireAfterSeconds=600)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'myNewApp\\PFAFNModel\\dataset\\test_img')

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
    users.insert_one({'email': obj['email'], 'password': token})
    return ("Created", token)


def Login_DB(obj):
    userinfo = users.find()
    for user in userinfo:
        if (user['email'] == obj['email']):
            decoded_token = jwt.decode(user['password'],
                                       settings.SECRET_KEY,
                                       algorithms=['HS256'])
            if (obj['password'] == decoded_token['password']):
                return (True, user['password'])
            else:
                return (False, obj['email'])
    return (False, obj['email'])


def saveImage(request):
    token = request.POST.get('token')
    userinfo = users.find()
    decoded_token = jwt.decode(token,
                               settings.SECRET_KEY,
                               algorithms=['HS256'])
    image_file = request.FILES['queryImage']
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
    decoded_token = jwt.decode(obj['token'],
                               settings.SECRET_KEY,
                               algorithms=['HS256'])
    for user in userinfo:
        if (user['email'] == decoded_token['email'] and user['password'] == obj['token']):
            return True
    return False

def loadImage(obj):
    decoded_token = jwt.decode(obj['token'],
                               settings.SECRET_KEY,
                               algorithms=['HS256'])
    imageInfo = image_collection.find()
    file_path = os.path.join(UPLOAD_FOLDER, f'{decoded_token["email"]}.jpg')
    for user in imageInfo:
        if (user['email'] == decoded_token['email']):
            with open(file_path, 'wb') as f:
                pil_img = Image.open(io.BytesIO(user['image']['data']))
                pil_img.save(file_path)
                return f'{decoded_token["email"]}.jpg',obj['cloth_image']
    return ''

def getProductsFromDB():
    products = productsCollection.find({}, {'_id': 0})
    return list(products)