import pymongo
import random
import string



client = pymongo.MongoClient(
    "mongodb+srv://shawen17:Shawenbaba1@shawencluster.jzsljb4.mongodb.net/?retryWrites=true&w=majority")

db = client['user_details']
# documents = db['users'].find({"userName": {"$exists": True}})
# for doc in documents:
#     field_value = doc.pop("userName")
#     doc["profile.userName"] = field_value
#     db['users'].update_one({"_id": doc["_id"]}, {"$set": {"profile.userName":field_value}})
# db['users'].update_many({}, {"$unset": {"userName": ""}})


def add_new_field_with_nested_value(new_field_name, nested_field_names):
    # Query documents where the existing field exists
    documents = db['users'].find({nested_field_names[0]: {"$exists": True}})
    
    for doc in documents:
        # Extract the nested field values and remove them from the document
        nested_values = {}
        for nested_field_name in nested_field_names:
            print(doc["education"][nested_field_name])
            nested_values[nested_field_name] = doc.pop("education"+"."+nested_field_name)

        # Add the new field with the extracted values as nested fields
        doc[new_field_name] = nested_values

        # Update the document in the collection
        db['users'].update_one({"_id": doc["_id"]}, {"$set": doc})



def update_field_with_nested_values(source_field_name, target_field_name, nested_field_names):
    # Query documents where the source field exists
    documents = db['users'].find({source_field_name: {"$exists": True}})

    for doc in documents:
        # Extract the specific nested field values from the source field
        nested_values_to_add = {nested_field: doc.get(source_field_name, {}).get(nested_field) for nested_field in nested_field_names}

        # Get existing nested values of the target field
        existing_nested_values = doc.get(target_field_name, {})

        # Merge the existing nested values with the extracted nested values
        updated_nested_values = {**existing_nested_values, **nested_values_to_add}

        # Update the target field with the merged nested values
        db['users'].update_one({"_id": doc["_id"]}, {"$set": {target_field_name: updated_nested_values}})

def remove_all_nested_fields_except(source_field_name, nested_field_to_keep):
    # Query documents where the source field exists
    documents = db['users'].find({source_field_name: {"$exists": True}})

    for doc in documents:
        # Create a list of nested fields to remove
        fields_to_remove = []
        for nested_field in doc.get(source_field_name, {}).keys():
            if nested_field != nested_field_to_keep:
                fields_to_remove.append(nested_field)

        # Remove nested fields except for the particular one to keep
        for field_to_remove in fields_to_remove:
            del doc[source_field_name][field_to_remove]

        # Update the document in the collection
        db['users'].update_one({"_id": doc["_id"]}, {"$set": {source_field_name: doc[source_field_name]}})


def generate_random_loan_repayment():
    # Generate a random loan repayment amount between 200 and 500
    return round(random.uniform(5000.0, 200000), 2)

def generate_random_min_income():
    # Generate a random account balance between 400.0 and 100,000.0
    return round(random.uniform(30000.0, 80000.0), 2)

def generate_random_max_income():
    # Generate a random account balance between 400.0 and 100,000.0
    return round(random.uniform(100000.0, 3000000.0), 2)

def add_random_nested_field_values():
    # Retrieve all documents in the collection
    documents = db['users'].find()

    for doc in documents:
        # Generate random nested field values
        loan_repayment = generate_random_loan_repayment()
        min_income = generate_random_min_income()
        max_income = generate_random_max_income()
        monthly_income = [min_income,max_income]
        # Update the document with the generated nested field values
        db['users'].update_one({"_id": doc["_id"]}, {"$set": {"account.monthlyIncome": monthly_income, "account.loanRepayment": loan_repayment}})

# Example usage: Add random nested field values to the "account" field in all documents
add_random_nested_field_values()

