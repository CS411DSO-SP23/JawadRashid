from pymongo import MongoClient
import pprint
client = MongoClient("localhost", 27017, maxPoolSize=50)
db = client.academicworld

collection = db.publications

pipeline = [   
 [
    {
        '$match': {
            'year': 2017
        }
    }, {
        '$lookup': {
            'from': 'faculty', 
            'localField': 'id', 
            'foreignField': 'publications', 
            'as': 'result'
        }
    }, {
        '$unwind': '$result'
    }, {
        '$match': {
            'result.affiliation.name': 'University of Michigan'
        }
    }, {
        '$count': 'result.affiliaton.name'
    }
]
]
pprint.pprint(list(db.publications.aggregate(pipeline)))

