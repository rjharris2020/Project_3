import pymongo

# Local DB Connection
connectionstring = 'mongodb://localhost:27017'
local_client = pymongo.MongoClient(connectionstring)
local_DB = local_client.evDB
print(local_DB)
# Remote DB Connection
remote_client = pymongo.MongoClient("mongodb://abarmago:GaTech1234@evdata-shard-00-00.lcvwb.mongodb.net:27017,evdata-shard-00-01.lcvwb.mongodb.net:27017,evdata-shard-00-02.lcvwb.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-g33pj8-shard-0&authSource=admin&retryWrites=true&w=majority")
remote_DB = remote_client.EVData

for l_col in local_DB.list_collection_names():
    print(l_col)
    remote_DB[l_col].insert_many(local_DB[l_col].find())