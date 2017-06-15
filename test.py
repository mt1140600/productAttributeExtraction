import pickle
def save_model(file_name, model_list):
    with open(file_name, 'wb') as fid:
        pickle.dump(model_list, fid)


def load_model(file_name):
    with open(file_name, 'rb') as fid:
        model = pickle.load(fid)
    return model
from pymongo import MongoClient
client = MongoClient('10.240.0.9')
db = client.prokure2
pincodedetails = db.productfinals
brands=[]
i=0
x = []
for row in pincodedetails.find():
    x.append(row)
    print
    print
    i=i+1
    if i>10:
        break
save_model('details.pkl', x)
# with open('newFile.csv','w') as svfile:
#     spmwriter = csv.writer(svfile)
#     with open('products.csv') as ifile:
#         read = csv.reader(ifile)
#         for row in read:
#             x = str(row[0])
#             if 'back' in x.lower():
#                 spmwriter.writerow([x])
    # print
# print brands
# for i in range(n):
#     print 'Brand: '+str(brands[i])
#     with open('products.csv') as ifile:
#         read = csv.reader(ifile)
#         for row in read:
#             x = str(row[0])
#             if str(brands[i]).lower() in x.lower():
#                 print x
#     print

