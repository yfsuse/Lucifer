#! /usr/bin/env python
# --*-- coding:utf-8 --*--

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

__author__ = 'jeff.yu'

import json
import pymongo
import MySQLdb
import os
import datetime
import socket



class Integration(object):

    def __init__(self, jsonFile):
        self.jsonFile = jsonFile
        self.jsonList = []
        self.setJsonList()

    def setJsonList(self):
        try:
            fileObject = open(self.jsonFile, 'r')
        except Exception as e:
            raise e
        for line in fileObject:
            tableData = []
            jsonLine = json.loads(line)
            if jsonLine.get('log_tye') == 1 and jsonLine.get('datasource') == 'hasoffer' and jsonLine.get("status") in ("Accepted", "Confirmed"):
                if jsonLine.get('status') == "Accepted":
                    offerId = findOfferFromDB(jsonLine.get("transaction_id"))
                else:
                    offerId = jsonLine.get("offer_id")
                conv_time = jsonLine.get("conv_time")
                status = jsonLine.get("status")
                url = jsonLine.get("request_url").decode("gbk").encode("utf8")
                tableData.append(convertConvTime(conv_time))
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

    def insertMysql(self):
        conn = MySQLdb.connect(host="10.1.5.60", user="django", passwd="django", db="statusdb", charset="utf8")
        """
        <1> create database statusdb;
        <2> use statusdb;
        <3> create table statustable(conv_time datetime,
                                     offer_id varchar(20),
                                     status varchar(10),
                                     url varchar(255));
        <4> grant select,insert,update,delete,create,drop on statusdb.* to django@'%' identified by 'django';
        """
        cursor = conn.cursor()
        for record in self.jsonList:
            sql = "insert into statustable(conv_time, offer_id, status, url) values(%s, %s, %s, %s)"
            result = cursor.execute(sql, record)
        conn.commit()
        conn.close()

def convertConvTime(conv_time):
    date = conv_time.split(' ')[0]
    hour = conv_time.split(' ')[1].split(':')[0]
    return '{0} {1}:00:00'.format(date, hour)

def findOfferFromDB(id):
    conn = pymongo.Connection("10.1.0.30", 40001)
    collections = [conn.report.click_log, conn.report.click_log0, conn.report.click_log1, conn.report.click_log2, conn.report.click_log3, conn.report.click_log4, conn.report.click_log5, conn.report.click_log6, conn.report.click_log7]
    for collection in collections:
        find = collection.find_one({'_id': id})
        if find:
            conn.disconnect()
            return find.get("offer")
    conn.disconnect()

def getRangeHour():
    now = datetime.datetime.now()
    previous = now + datetime.timedelta(hours=-1)
    return (previous.strftime('%Y-%m-%dT%H'), now.strftime('%Y-%m-%dT%H'))

def getip():
    return socket.gethostbyname(socket.gethostname()).replace('.', '-')

def control(batchFilePath= '/data2/druidBatchData'):
    """
    :param batchFilePath:
    :return: ip-10-1-15-13.ec2.internaldata_2014-11-21T23_2014-11-22T00_druid.json
    """
    localIp = getip()
    previousHour, nextHour = getRangeHour()
    batchJsonFile = 'ip-{0}.ec2.internaldata_{1}_{2}_druid.json'.format(localIp, previousHour, nextHour)
    batchJsonFullPath = os.path.join(batchFilePath, batchJsonFile)
    integration = Integration(batchJsonFullPath)
    integration.insertMysql()

if __name__ == '__main__':
    control()