from flask import Flask, request, jsonify
import pymongo
import json
from bson.objectid import ObjectId


myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["mydatabase"]

app = Flask(__name__)

dblist = myclient.list_database_names()
mycol = mydb["Address_Book"]

collist = mydb.list_collection_names()

@app.route("/", methods=['GET','POST'])
def address_book():
    if request.method=='GET':
        addresses = list(mycol.find())
        if len(addresses)!=0:
            print('list',list(addresses))
            for a in addresses:
                a["_id"] = str(a["_id"])
            return jsonify(json.dumps(addresses))
        else:
            return "No addresses found"

@app.route("/address", methods=['GET','POST'])
def view():
    try:
        if request.method == 'GET':
            find_address = request.get_json()

            for i in list(find_address):
                print(i, ':', find_address[i])
                if find_address[i] == '':
                    find_address.pop(f"{i}")

            find_address=list(mycol.find(find_address))

            if len(find_address)!=0:
                for a in find_address:
                    a["_id"] = str(a["_id"])
                print('JSON',json.dumps(list(find_address)))
                return jsonify(json.dumps(list(find_address)))
            else:
                return 'No address found'
    except:
        return 'Address not found'

    if request.method == 'POST':
        insert_address = request.get_json()
        mycol.insert(insert_address)
        return jsonify(json.dumps('Data Inserted'))

@app.route("/update/<id>", methods=['PUT','DELETE'])
def update(id):

    try:
        if request.method == 'PUT':
            id=ObjectId(id)
            print('ID',id)
            update_response = mycol.update_one({"_id": id}, {"$set": request.get_json()})
            if update_response.matched_count==0:
                return 'Address not found'
            elif update_response.modified_count==0:
                return 'Address not updated'
            else:
                return 'Address updated'
    except:
        return 'Address not found'
    if request.method == 'DELETE':
        try:
            print('inside delete')
            delete_response=mycol.delete_one({"_id": ObjectId(id)})
            print(delete_response['n'])
            print(delete_response)
            if delete_response['n']!=0:
                return 'row deleted'
            else:
                return 'Address not found'
        except:
            return 'Address not found'

app.run(debug=True)
