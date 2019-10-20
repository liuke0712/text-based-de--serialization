#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
Created on Sat Oct 12 03:31:45 2019

@author: Maggie
"""
#import flask related functions
from flask import Flask, jsonify
from flask import abort
from flask import request

#import csv & json functions
import csv
import json
import random

#define file paths
DVD_csv_file = '/Users/Maggie/Desktop/DVD-testing.csv'
DVD_json_file = '/Users/Maggie/Desktop/DVD-testing.json'
NDBench_csv_file = '/Users/Maggie/Desktop/NDBench-testing.csv'
NDBench_json_file = '/Users/Maggie/Desktop/NDBench-testing.json'

#define global parameters
json_file_path = ''
TotalList = []
BatchList = []
MatricList = []
MatricItem = int
RFWID = int
LastBatchID = int

app = Flask(__name__)

#Generate RFW ID (random number)
# def Gen_RFW_ID():
#     global RFWID
#     RFWID = random.randrange(100000,1000000)
    
'''?????how to transfer all parameters to each function'''
# @app.route('/getdata/NDBench?BatchUnit=10&&BatchID=1&&BatchSize=5&&Item1&&Item2', methods=['GET'])
@app.route('/api/workload', methods=['GET'])
def workload():
    validFields = [ "rfwID", "fields", "unitSize", "batchID", "batchSize"]
    queryReq = request.args
    query = {}
    for field in validFields:
        if queryReq.__contains__(field):
            query[field] = queryReq[field]


    # format fields
    if queryReq.__contains__("fields"):
        query["fields"] = queryReq["fields"].split(",")

    return query



#Read CSV File
def read_csv_file(csv_file):
    global DVD_csv_file
    global DVD_json_file
    global NDBench_csv_file
    global NDBench_json_file
    global json_file_path
    global TotalList
    FileType = csv_file
    #Request DVD Store Data
    if FileType == "DVD":
        json_file_path = DVD_csv_file
        with open(DVD_csv_file) as csvfile:
            reader = csv.DictReader(csvfile)
            field = reader.fieldnames
            for row in reader:
                TotalList.extend([{field[i]:row[field[i]] for i in range(len(row))}])       
    #Request NDBench Data
    elif FileType == "NDBench":
        json_file_path = NDBench_json_file
        with open(NDBench_csv_file) as csvfile:
            reader = csv.DictReader(csvfile)
            field = reader.fieldnames
            for row in reader:
                TotalList.extend([{field[i]:row[field[i]] for i in range(len(row))}])       
    #Exception
    else:
        print ("Do not have this type!")
        
#Generate requited batch
def batch_list_dist(TotalList, BatchUnit, BatchID, BatchSize):
    global BatchList
    global LastBatchID
    BatchList = TotalList[(BatchID-1)*BatchUnit:((BatchID-1)*BatchUnit)+BatchUnit*BatchSize]
    LastBatchID = BatchID + BatchSize - 1        

'''?????how to transfer list to this function'''
#Select Show Matric from BatchList
def matric_list(BatchList, Item1, Item2):
    global MatricList
    Items = [Item1, Item2]
    for workload in BatchList:
        extractedData = {}
        for item in Items:
            extractedData[item] = workload[item]
        MatricList.append(extractedData)
    
#Convert csv data into json
def convert_write_json(MatricList, json_file_path):
    with open(json_file_path, "w") as output:
        output.write(json.dumps(MatricList, sort_keys=False, separators=((',',':'))))

if __name__=='__main__':
    app.run(debug=True)
    
'''used for check the output'''    
# '''read_csv_file("NDBench") '''
# batch_list_dist(TotalList, 2, 10, 3)
# matric_list(BatchList,"NetworkIn_Average","NetworkOut_Average")
# convert_write_json(MatricList, json_file_path)