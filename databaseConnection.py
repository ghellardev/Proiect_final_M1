import pymongo


def databaseConnection(collection):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Firma"]
    angajat = db[collection]
    return angajat
