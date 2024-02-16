from django.shortcuts import render
import pymongo
from rest_framework.response import Response
from rest_framework.decorators import api_view 
from rest_framework import status
from django.http import JsonResponse
from decouple import config
import json
import os 
from django.conf import settings
from datetime import datetime
from bson.objectid import ObjectId


db_user = config("DB_USER")
db_password=config("PASSWORD")
db_cluster = config("CLUSTERNAME")
client = pymongo.MongoClient(
    f"mongodb+srv://{db_user}:{db_password}@{db_cluster}.jzsljb4.mongodb.net/?retryWrites=true&w=majority")

db = client['user_details']



@api_view(['GET','POST'])
def users(request):
    if request.method=='GET':
        users=db['users'].find({})
        page = int(request.GET.get('page', 1))
        
        per_page = 20  
        start_index = (page - 1) * per_page
        end_index = page * per_page
        all_documents = [{**doc, '_id': str(doc['_id'])} for doc in users]
        users_paginated = all_documents[start_index:end_index]
        all_users = db['users'].count_documents({})
        active=db['users'].count_documents({"profile.status":"Active"})
        savings= db['users'].count_documents({"account.accountBalance":{"$gt":0}})
        loan =  db['users'].count_documents({"account.loanRepayment":{"$gt":0}})

        return Response({"users_paginated":users_paginated,"all_users":all_users,"active":active,"loan":loan,"savings":savings},status=status.HTTP_200_OK)

    if request.method=='POST':
        
        avatar=request.FILES.get('avatar')
        
        media_root = settings.MEDIA_ROOT
        avatars_dir = os.path.join(media_root, 'avatars')
        os.makedirs(avatars_dir, exist_ok=True)

        file_path = os.path.join(avatars_dir, avatar.name)
        with open(file_path, 'wb') as file:
            for chunk in avatar.chunks():
                file.write(chunk)

        account = json.loads(request.POST.get('account')) if 'account' in request.POST else None
        
        organization = json.loads(request.POST.get('organization')) if 'organization' in request.POST else None
        education = json.loads(request.POST.get('education')) if 'education' in request.POST else None
        socials = json.loads(request.POST.get('socials')) if 'socials' in request.POST else None
        guarantor = json.loads(request.POST.get('guarantor')) if 'guarantor' in request.POST else None
        profile = json.loads(request.POST.get('profile')) if 'profile' in request.POST else None
        profile['avatar'] = file_path

        data ={
            "profile":profile,
            "account":account,
            "organization": organization,
            "education":education,
            "socials":socials,
            "guarantor":guarantor,
            "createdAt":datetime.now()
        }
        db['users'].insert_one(data)

        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def filter_users(request):
    if request.method=="GET":
        search = request.GET.get("search")
        regex_pattern = f".*{search}.*"

        query={
            "$or":[
                {"profile.email":{"$regex": regex_pattern, "$options": "i"}},
                {"profile.userName":{"$regex": regex_pattern, "$options": "i"}},
                {"profile.firstName":{"$regex": regex_pattern, "$options": "i"}},
                {"profile.lastName":{"$regex": regex_pattern, "$options": "i"}},
                {"profile.status":{"$regex": regex_pattern, "$options": "i"}},
                {"profile.address":{"$regex": regex_pattern, "$options": "i"}},
                {"account.accountName":{"$regex": regex_pattern, "$options": "i"}},
                {"guarantor.guaAddress":{"$regex": regex_pattern, "$options": "i"}},
                {"guarantor.guaFirstName":{"$regex": regex_pattern, "$options": "i"}},
                {"guarantor.guaLastName":{"$regex": regex_pattern, "$options": "i"}},
                {"organization.orgName":{"$regex": regex_pattern, "$options": "i"}},
                {"organization.employmentStatus":{"$regex": regex_pattern, "$options": "i"}},
                {"organization.sector":{"$regex": regex_pattern, "$options": "i"}},
                {"organization.officeEmail":{"$regex": regex_pattern, "$options": "i"}},
            ]
        }
        users=db['users'].find(query)
        all_documents = [{**doc, '_id': str(doc['_id'])} for doc in users]
        return Response(all_documents,status=status.HTTP_200_OK)

@api_view(['PUT'])    
def update_status(request,id,action):
    user_id = ObjectId(id)
    update=db['users'].update_one({"_id":user_id},{"$set":{"profile.status":action}})
    print(update.modified_count)
    return Response(status=status.HTTP_201_CREATED)

@api_view(['GET']) 
def advance_filter(request):
    organization = json.loads(request.GET.get('organization')) if 'organization' in request.GET else None
    profile = json.loads(request.GET.get('profile')) if 'profile' in request.GET else None
    
    combined={}
    if profile:
        combined={**profile}
    if organization:
        combined={**combined,**organization}
    
    query={}

    for key,value in combined.items():
        if key=="profile" and len(value)>0:
                for i,j in value.items():
                    if j!='':
                        query_key=f"profile.{i}"
                        query[query_key] = j
        if key=="organization" and len(value)>0:
                for i,j in value.items():
                    if j!='':
                        query_key=f"organization.{i}"
                        query[query_key] = j
    print({"$and":[query]})
    users=db['users'].find({"$and":[query]})
    all_documents = [{**doc, '_id': str(doc['_id'])} for doc in users] 
       
    
    return Response(all_documents,status=status.HTTP_200_OK)
