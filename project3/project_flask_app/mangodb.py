from api11st import get_page,tojson_PS
from pymongo import MongoClient
import time

def get_result(key="",number=99,pSize=20,SortCd="CP"):
    if key=="":
        print("Key가 입력되지않았습니다.")
        return {}

    pNum=int(number/pSize)  #4
    ectNum=number%pSize     #19
    
    data_json={}
    
    data=get_page(keyword=key,pageNum=1,pageSize=pSize,sortCd=SortCd)
    data_json=tojson_PS(data,Data_Origin=data_json,start_num=0)
    
    for i in range(1,pNum):
        data=get_page(keyword=key,pageNum=1+i,pageSize=pSize,sortCd=SortCd)
        data_json=tojson_PS(data,Data_Origin=data_json[0],start_num=data_json[2])
    
    data=get_page(keyword=key,pageNum=pNum+1,pageSize=ectNum,sortCd=SortCd)
    data_json=tojson_PS(data,Data_Origin=data_json[0],start_num=data_json[2])
    
    return data_json
'''
            → CP : 인기도순
            → A : 누적판매순
            → G : 평가높은순
            → I : 후기/리뷰많은순
            → L : 낮은가격순
            → H : 높은가격순
            → N : 최근등록순
'''
class hosts:
    def __init__(self):
        time.sleep(1)
        self.HOST = 'cluster0.3dnjb.mongodb.net'
        self.USER = 'project3'
        self.PASSWORD = '1q2w3e4r'
        self.DATABASE_NAME = 'productSearch'
        self.MONGO_URI = f"mongodb+srv://{self.USER}:{self.PASSWORD}@{self.HOST}/{self.DATABASE_NAME}?retryWrites=true&w=majority"
        self.client=MongoClient(self.MONGO_URI)
        self.database=self.client[self.DATABASE_NAME]

def insertCollection(data):
    COLLECTION_NAME = data[4]
    Collection=hosts().database[COLLECTION_NAME]
    Collection.insert_one(document=data[0])

def dropCollection(COLLECTION_NAME):
    database=hosts().database
    database.drop_collection(COLLECTION_NAME)
'''
def dropCollection(COLLECTION_NAME_Detail):
    Collection=hosts().database[COLLECTION_NAME]
    Collection.delete_one(COLLECTION_NAME_Detail)
''' 

#result=get_result("사과",number=20,pSize=20,SortCd="CP")    
#insertCollection(result)

#breakpoint()
#result=get_result("손전등",number=20,pSize=20,SortCd="L")    
#insertCollection(result)
#dropCollection(result[4])

'''
for value in Collection.find():
    values=[value['col1'],value['col2'],.......]
'''