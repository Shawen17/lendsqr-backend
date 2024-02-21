import pymongo
from decouple import config




db_user = config("DB_USER")
db_password=config("PASSWORD")
db_cluster = config("CLUSTERNAME")


client = pymongo.MongoClient(
    f"mongodb+srv://{db_user}:{db_password}@{db_cluster}.jzsljb4.mongodb.net/?retryWrites=true&w=majority")

db = client['user_details']
db['users'].update_many(
  {},
  {
    "$rename":{
      "phoneNumber":"orgNumber",
      "guarantor.firstName":"guarantor.guaFirstName",
      "guarantor.lastName":"guarantor.guaLastName",
      "guarantor.phoneNumber":"guarantor.guaNumber",
      "guarantor.gender":"guarantor.guaGender",
      "guarantor.address":"guarantor.guaAddress"

    }
  }
)