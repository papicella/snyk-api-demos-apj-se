from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://pasapicella:Wk0VQv9y2GD940PR@pas-mongodb-cluster.ik3ak.mongodb.net/snyk')
db = cluster['snyk']
collection = db['test']

post = {'_id': 0, 'name': 'Jeff', 'score': 9}
collection.insert_one(post)

print("all done ..")