# This script creates control collection

def insert(db, data):
    # a default collection that will be updated later
    collection = ''
    # if the arango db does not have a control collection, make one
    if not db.has_collection('control'):
        db.create_collection('control')

    # open the control collection
    collection = db.collection('control')

    # variables to hold important information
    controlID = ''
    controlName = ''

    for obj in data:

        # take the Control_ID and match it to the variable controlID
        key = 'Control_ID'
        if key in obj:
            controlID = obj[key]

        # take the Control_Name and match it to the variable controlName
        key2 = 'Control_Name'
        if key2 in obj:
            controlName = obj[key2]

        # If the controlID does not exist in the control collection, insert into collection
        if not collection.has(controlID):
            temp = {'_key': controlID, 'name': controlName, 'datatype': 'control'}
            collection.insert(temp)
