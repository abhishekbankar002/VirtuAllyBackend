import io
import json
import os

from PIL import Image

# Create your views here.
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core import serializers
from .PFAFNModel.runModel import runModel
from django.middleware.csrf import get_token
from db import writeDB, Login_DB, saveImage, checkLogIn, loadImage, getProductsFromDB


UPLOAD_FOLDER = os.path.join(os.getcwd(), 'myNewApp\\PFAFNModel\\dataset\\test_img')

RESULT_FOLDER = os.path.join(os.getcwd(), 'results\\demo\\PFAFN')

@csrf_exempt
def getImage(request):
    if request.method == 'POST':
        saveImage(request)
        return JsonResponse({'image': True, 'status': 200})
        filename, extension = os.path.splitext(image_file.name)


        file_path = os.path.join(UPLOAD_FOLDER, f'{filename}{extension}')
        # pil_img.save(UPLOAD_FOLDER,'test.jpg')
        # with open(file_path,'wb') as f:
        #     f.write(image_file.read())

            # save the file with the same extension as it was received
        with open(file_path, 'wb') as f:
            for chunk in image_file.chunks():
                f.write(chunk)


        runModel(f'{filename}{extension}','017575_1.jpg')

        if(saveImage(image_file)):
            return HttpResponse('',status=200)
        else:
            return HttpResponse('',status=404)

        # plt.imshow(pil_img)
        # plt.show()

@csrf_exempt
def registerUser(request):
    if request.method == "POST":
        dicObj=json.loads(request.body)
        # if(dicObj['add']=='true'):
        o=dicObj
        flag,token=writeDB(obj=o)
        if(flag=="Created"):
            return JsonResponse({'token':token,'status':200})
        elif(flag=="Not Created"):
            return JsonResponse({'token':'','status':404})

@csrf_exempt
def logIn(request):
    if request.method == "POST":
        # print(request.headers.)
        dicObj = json.loads(request.body)
        flag, token = Login_DB(obj=dicObj)
        if flag:
            return JsonResponse({'token':token,'status':200})  # Loggend In
        else:
            return JsonResponse({'token':'','status':404})  # Wrong Credentials

@csrf_exempt
def checkLogin(request):
    if request.method == "POST":
        dicObj = json.loads(request.body)
        flag = checkLogIn(dicObj)
        if flag:
            return JsonResponse({'loggedIn': 'True'})
        else:
            return JsonResponse({'loggedIn': 'False'})


@csrf_exempt
def tryImage(request):
    if request.method == "POST":
        dicObj=json.loads(request.body)
        print(dicObj)
        test,cloth_image = loadImage(dicObj)
        runModel(test, cloth_image)
        image_path = os.path.join(RESULT_FOLDER, f'{test}')
        with open(image_path, 'rb') as f:
            image = Image.open(f)
            # Set the content type of the response to image/jpeg
            response = HttpResponse(content_type='image/jpeg')

            # Save the image to the response object
            image.save(response, 'JPEG')
            print(response)
            return response
        # return JsonResponse({'status' : 200})

        # if getImage(dicObj)!='':
        #     runModel(f'{filename}{extension}', '017575_1.jpg')

@csrf_exempt
def getProducts(request):
    if request.method == "POST":
        products = getProductsFromDB()
        # data_json = json.dumps(products)
        # print(data_json)
        return JsonResponse(products, safe=False)

def get_csrf_token(request):
    return JsonResponse({'csrf_token': get_token(request)})
