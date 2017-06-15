import csv
from pymongo import MongoClient
client = MongoClient('10.240.0.9')
db = client.prokure2
pincodedetails = db.productfinals
brands=[]
for row in pincodedetails.find():
    print row['name']

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

