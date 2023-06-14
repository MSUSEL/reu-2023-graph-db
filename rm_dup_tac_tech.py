# This script remove the duplicate data in TacticTechinique Edge Collection

def remove_duplicates(db):
    # query that removes all duplicate data
    query = 'for data in TacticTechnique '\
            + 'collect to = data._to, from = data._from into keys = data._key '\
            + 'let first = SLICE(keys, 1) '\
            + 'for k in first '\
            + 'remove k in TacticTechnique'
    
    # executes the query
    db.aql.execute(query)
