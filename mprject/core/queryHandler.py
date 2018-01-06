from pymongo import MongoClient
def get_db():
    connection_=MongoClient()['testDB']
    return connection_
