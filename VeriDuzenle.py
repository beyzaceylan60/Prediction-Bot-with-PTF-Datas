import pymongo

client = pymongo.MongoClient()
db = client.PTF

collection = db.ptf
    
for document in collection.find():
    
# Belgeyi güncellemek için güncelleme ifadesi
    update = {'$set': {'PTF (TL/MWh)': float(document['PTF (TL/MWh)'].replace('.', '').replace(',', '.'))}}
    collection.update_one(document, update)# Belgeyi işleyin
    update = {'$set': {'PTF (EUR/MWh)': float(document['PTF (EUR/MWh)'].replace('.', '').replace(',', '.'))}}
    collection.update_one(document, update)# Belgeyi işleyin
    update = {'$set': {'PTF (USD/MWh)': float(document['PTF (USD/MWh)'].replace('.', '').replace(',', '.'))}}
    collection.update_one(document, update)# Belgeyi işleyin

    