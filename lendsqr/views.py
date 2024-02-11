from django.shortcuts import render
import pymongo
from rest_framework.response import Response
from rest_framework.decorators import api_view 
from rest_framework import status
from django.http import JsonResponse
import os


db_user = os.environ.get("USERNAME")
db_password=os.environ.get("PASSWORD")
db_cluster = os.environ.get("CLUSTERNAME")

client = pymongo.MongoClient(
    f"mongodb+srv://{db_user}:{db_password}@{db_cluster}.jzsljb4.mongodb.net/?retryWrites=true&w=majority")

db = client['user_details']


@api_view(['GET'])
def users(request):
    if request.method=='GET':
        users=db['users'].find({})
        page = int(request.GET.get('page', 1))
        per_page = 20  
        start_index = (page - 1) * per_page
        end_index = page * per_page
        all_documents = [{**doc, '_id': str(doc['_id'])} for doc in users]
        users_paginated = all_documents[start_index:end_index]
        
        return Response(users_paginated,status=status.HTTP_200_OK)

