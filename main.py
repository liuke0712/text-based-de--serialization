#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
Created on Sat Oct 12 03:31:45 2019

@author: Maggie
"""
#import flask related functions
from flask import Flask, jsonify
# from flask import abort
from flask import request

#import csv & json functions
import csv
# import json

import uuid


#define global parameters

TotalList = []
BatchList = []
MatricList = []
RFWID = uuid.uuid4()
LastBatchID = int

app = Flask(__name__)
    
@app.route('/api/workload/<category>', methods=['GET'])
def workload(category):

    global MatricList
    global RFWID
    global LastBatchID

    validFields = [ "rfwID", "fields", "unitSize", "batchID", "batchSize"]
    queryReq = request.args
    query = {}
    for field in validFields:
        if queryReq.__contains__(field):
            query[field] = queryReq[field]


    # format fields
    if queryReq.__contains__("fields"):
        query["fields"] = queryReq["fields"].split(",")
    else:
        query["fields"] = []

    if query.__contains__("rfwID"):
        RFWID = query["rfwID"]

    # Start Actions

    read_csv_file(request.view_args["category"])

    if len(query["fields"]) > 0:
        matric_list(query["fields"])
    else:
        MatricList = TotalList

    unitSize = 100
    if query.__contains__("unitSize"):
        unitSize = query["unitSize"]

    batches = splitData(unitSize)

    selectStartIndex = 0
    if query.__contains__("batchID"):
        selectStartIndex = query["batchID"]
    
    batchSize = len(MatricList)
    if query.__contains__("batchSize"):
        batchSize = query["batchSize"]

    # batch_list_dist(unitSize, batchStartIndex, batchSize)

    selectBatch(selectStartIndex, batchSize)

    # Prepare for the response
    res = {}

    res["rfwID"] = RFWID
    res["lastBatchID"] = LastBatchID
    res["workloadBatches"] = BatchList

    return jsonify(res)

def read_csv_file(csv_file_name):
    global TotalList
    #Request DVD Store Data
    basePath = "./statics/"
    filePath = basePath + csv_file_name + ".csv"
    try:
        with open(filePath) as csvfile:
            reader = csv.DictReader(csvfile)
            field = reader.fieldnames
            for row in reader:
                TotalList.extend([{field[i]:row[field[i]] for i in range(len(row))}])
        pass
    except:
        print ("Do not have this type! " + filePath)
        pass
        
#Select Show Matric

def matric_list(fields):
    global TotalList
    global MatricList

    for workload in TotalList:
        extractedData = {}
        for field in fields:
            extractedData[field] = workload[field]
        MatricList.append(extractedData)

def splitData(unitSize):
    global MatricList

    unitSize = int(unitSize)

    index = 0
    while (index < len(MatricList)):
        end = index + unitSize
        BatchList.append(MatricList[index: end])
        index = end

def selectBatch(BatchID, BatchSize):
    global MatricList
    global BatchList
    global LastBatchID

    BatchID = int(BatchID)
    BatchSize = int(BatchSize)

    BatchList = BatchList[BatchID:BatchSize]

    LastBatchID = BatchID + BatchSize - 1      
    
#Convert csv data into json
# def convert_write_json(MatricList, json_file_path):
#     with open(json_file_path, "w") as output:
#         output.write(json.dumps(MatricList, sort_keys=False, separators=((',',':'))))

if __name__=='__main__':
    app.run(debug=True)
    