import pickle
def save_model(file_name, model_list):
    with open(file_name, 'wb') as fid:
        pickle.dump(model_list, fid)


def load_model(file_name):
    with open(file_name, 'rb') as fid:
        model = pickle.load(fid)
    return model
# from pymongo import MongoClient
# client = MongoClient('10.240.0.9')
# db = client.prokure2
# pincodedetails = db.productfinals
brands=[]
types = []
subcategory = []
i=0
# for row in pincodedetails.find():
#     x.append(row)
#     i = i+1
#     print i
#     # if i==101:
#     #     break
import csv
b = load_model('details.pkl')
for row in b:
    if row['subCategoryFilters']['Brand'] not in brands:
        brands.append(row['subCategoryFilters']['Brand'])
    if row['subCategory'] not in subcategory:
        subcategory.append(row['subCategory'])

typeMap = {}
for cat in subcategory:
    arr = []
    for row in b:
        x = row['subCategoryFilters']
        if 'Type' in x and (x['Type'])[0] not in arr:
            arr.append((x['Type'])[0])
    typeMap[cat[0]] = arr

# print types
for brand in brands:
    for cat in subcategory:
        for t in typeMap[cat[0]]:
            print brand[0]+' '+t+' '+cat[0]