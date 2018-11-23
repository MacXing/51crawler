# -*- coding: utf-8 -*- 
# @Time : 2018/11/23 10:06 
# @Author : Allen 
# @Site :  链接mongodb
from pymongo import MongoClient


class Mongodb:
    def __init__(self):
        self.db = self.get_db()
        print("Finished Loaded Mongodb")

    def get_db(self):
        client = MongoClient("mongodb://localhost:27017/")
        return client['job']['job']

    def insert_document(self, document_dict):
        try:
            self.db.insert(document_dict)
            print("Success insert {}".format(document_dict['company_name']))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    mongodb = Mongodb()
    document_dict = {"document_name": "demo"}
    mongodb.insert_document(document_dict)
