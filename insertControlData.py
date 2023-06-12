from arango import ArangoClient
import json

client = ArangoClient()

db = client.db('BRON', username='root', password='changeme')

#print(db.collections())

#cve = db.collection('cve')

#print(cve.count())

collection = ''

with open("nist800-53-r5-mappings2.json", 'r') as file:
    data = json.load(file)

    if not db.has_collection('control'):
        db.create_collection('control')
        
    collection = db.collection('control')

    Somekey = ''
    name = ''

    for obj in data:

        key = 'Control_ID'
        if key in obj:
            Somekey = obj[key]

        key2 = 'Control_Name'
        if key2 in obj:
            name = obj[key2]

        if not collection.has(Somekey):
            temp = {'_key': Somekey, 'name': name, 'datatype': 'control'}
            collection.insert(temp)
