#! /usr/bin/env python
# --*-- coding:utf-8 --*--

__author__ = 'jeff.yu'

import json
import pymongo

class Parser(object):

    def __init__(self, jsonFile):
        self.jsonFile = jsonFile
        self.jsonList = []

    def setJsonList(self):
        try:
            fileObject = open(self.jsonFile, 'r')
        except Exception as e:
            raise e
        for line in fileObject:
            tableData = []
            jsonLine = json.loads(line)
            if jsonLine.get('log_tye') == 1 and jsonLine.get('datasource') == 'hasoffer':
                if jsonLine.get('status') == "Accepted":
                    offerId = findOfferFromDB(jsonLine.get("transaction_id"))
                else:
                    offerId = jsonLine.get("offer_id")
                conv_time = jsonLine.get("conv_time")
                status = jsonLine.get("status")
                url = jsonLine.get("request_url")
                tableData.append(conv_time)
                tableData.append(offerId)
                tableData.append(status)
                tableData.append(url)
                self.jsonList.append(tableData)
            else:
                pass
    def getJsonList(self):
        self.setJsonList()
        for jsonRecord in self.jsonList:
            print jsonRecord

def findOfferFromDB(id):
    conn = pymongo.Connection("127.0.0.1",27017)


if __name__ == '__main__':
    p = Parser(r'C:\Users\jeff.yu\Desktop\hasofferConv')
    p.getJsonList()