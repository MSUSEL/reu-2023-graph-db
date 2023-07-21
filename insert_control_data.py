# This script creates control collection

def insert(db, data):
    CTRL = 'control'
    # if the arango db does not have a control collection, make one
    if db.has_collection(CTRL):
        db.delete_collection(CTRL)
    
    db.create_collection(CTRL)

    # open the control collection
    collection = db.collection(CTRL)

    # variables to hold important information
    control_id = ''
    control_name = ''
    control_id_name = ''

    for obj in data:

        # take the Control_ID and match it to the variable controlID
        key = 'Control_ID'
        if key in obj:
            control_id = obj[key]

        # take the Control_Name and match it to the variable controlName
        key2 = 'Control_Name'
        if key2 in obj:
            control_name = obj[key2]
        
        control_id_name = control_id + ' (' + control_name + ')'

        # If the controlID does not exist in the control collection, insert into collection
        if not collection.has(control_id):
            temp = {'_key': control_id, 'name': control_name, 'id_name': control_id_name, 'datatype': CTRL}
            collection.insert(temp)
