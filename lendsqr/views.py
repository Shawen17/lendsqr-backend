from django.shortcuts import render
import pymongo
from rest_framework.response import Response
from rest_framework.decorators import api_view 
from rest_framework import status
from django.http import JsonResponse
from decouple import config
import json


db_user = config("DB_USER")
db_password=config("PASSWORD")
db_cluster = config("CLUSTERNAME")




@api_view(['GET','POST'])
def users(request):
    
    client = pymongo.MongoClient(
    f"mongodb+srv://{db_user}:{db_password}@{db_cluster}.jzsljb4.mongodb.net/?retryWrites=true&w=majority")

    db = client['user_details']
    
    if request.method=='GET':
        users=db['users'].find({})
        page = int(request.GET.get('page', 1))
        per_page = 20  
        start_index = (page - 1) * per_page
        end_index = page * per_page
        all_documents = [{**doc, '_id': str(doc['_id'])} for doc in users]
        users_paginated = all_documents[start_index:end_index]
        
        return Response(users_paginated,status=status.HTTP_200_OK)

    if request.method=='POST':
        
        avatar=str(request.FILES.get('avatar'))
        account = json.loads(request.POST.get('account')) if 'account' in request.POST else None
        
        organization = json.loads(request.POST.get('organization')) if 'organization' in request.POST else None
        education = json.loads(request.POST.get('education')) if 'education' in request.POST else None
        socials = json.loads(request.POST.get('socials')) if 'socials' in request.POST else None
        guarantor = json.loads(request.POST.get('guarantor')) if 'guarantor' in request.POST else None
        profile = json.loads(request.POST.get('profile')) if 'profile' in request.POST else None
        profile['avatar'] = avatar

        data ={
            "profile":profile,
            "account":account,
            "organization": organization,
            "education":education,
            "socials":socials,
            "guarantor":guarantor
        }
        db['users'].insert_one(data)

        client.close()

        return Response(status=status.HTTP_201_CREATED)


