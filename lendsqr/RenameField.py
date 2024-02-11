import pymongo



client = pymongo.MongoClient(
    "mongodb+srv://shawen17:Shawenbaba1@shawencluster.jzsljb4.mongodb.net/?retryWrites=true&w=majority")

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