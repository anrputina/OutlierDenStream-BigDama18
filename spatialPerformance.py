#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 11:36:54 2018

@author: andrian
"""

import json
import numpy as np
import pandas as pd
import sys
sys.path.append('/Users/andrian/Desktop/DenStreamRelease')
sys.path.append('/Users/andrian/Desktop/DenStreamRelease/Examples')
from readGroundTruth import groundTruth

import statsmodels.stats.api as sms

configuration = json.load(open('./configuration.json'))

path = 'Data/ResultsSpatialDetection/'
features = configuration['featureModel']

algorithm = 'DENSTREAM'

def extractSyncResults(node, dataset, indexTime):
    df = pd.read_csv(path+features+'/'+dataset+'_'+algorithm+'_'+node+'.csv')
    df['datetime'] = pd.to_datetime(df.time, unit='s')
    df = df.set_index('datetime')
    dfresampled = df.resample('5s')
    
    listResults = []
    precedent = None
    
    for index in indexTime:
        try:
            currentSample = dfresampled.get_group(index)['result']
            
            if len(currentSample) > 1:
                listResults.append(currentSample.iloc[-1])
                precedent = currentSample.iloc[-1]
            elif len(currentSample) == 1:
                listResults.append(currentSample.iloc[0])
                precedent = currentSample.iloc[0]
            else:
                print 'Something wrong in indexing and resampling'
        except:
            listResults.append(precedent)
    return listResults
            
def findIndexTime (node, dataset):
    
    df = pd.read_csv(path+features+'/'+dataset+'_'+algorithm+'_'+node+'.csv')
    times = pd.to_datetime(df.time, unit='s')
    
    startTime = times.iloc[0].replace(second=0, microsecond=0)
    endTime = times.iloc[-1].replace(second=0, microsecond=0)    
    indexTime = pd.date_range(start=startTime, end=endTime, freq='5s')

    return indexTime


resultSimulation = {}
"""Iterate on all the datasets chosen, load the results for each node obtained with the main.py script (spatialDetection mode) and load the ground truth file"""
for dataset in configuration['dataset']['list']:
    
    """Extract Index for the first dataset"""
    indexTime = findIndexTime('leaf1', dataset)
    df = pd.DataFrame(index=indexTime)
    df['time'] = indexTime.astype('int64')//1e9
    
    for node in configuration['nodes']:
        """Sync all the datasets index"""
        df[node] = extractSyncResults(node, dataset, indexTime)
    
    df = df.dropna()
                
    truth = groundTruth('GrounTruth/'+dataset+'.txt', fileType='csv')
    
    kMAX = 5
    eventPerformance = {}
    
    for k in range(1, kMAX+1):
        eventPerformance[k] = {}
        eventPerformance[k]['Precision'] = []
        eventPerformance[k]['Recall'] = []
        eventPerformance[k]['False'] = []
        eventPerformance[k]['Delay'] = []

    for eventNumber in range(len(truth.events)):

        event = truth.events[eventNumber]
        clear = truth.clears[eventNumber]
        
        for k in range(1, kMAX+1):

            check = (df['time'] >= event['startTime']) & (df['time'] <= event['endTime'])
            times = df['time']
            currentEvent = df[check].drop('time', axis=1)

            checkOnce = True
            
            for row in currentEvent.iterrows():
                                
                if (row[1] == True).sum() >= k and checkOnce:
                    checkOnce = False
                    eventPerformance[k]['Delay'].append(times.loc[row[0]] - event['startTime'])
                    
            if checkOnce == False:
                eventPerformance[k]['Recall'].append(1)
                    
            check = (times > clear['startTime']) & (times <= clear['endTime'])
            currentEvent = df[check]
            currentEvent = currentEvent.drop(currentEvent.tail(1).index)
            
            counterFalsePositives = 0
            lastDetection = 0
            
            for row in currentEvent.iterrows():
                
                if (row[1] == True).sum() >= k and row[1]['time'] > lastDetection + 300:
                    counterFalsePositives += 1
                    lastDetection = row[1]['time']
            
            if counterFalsePositives > 0 and checkOnce == False :
                eventPerformance[k]['Precision'].append(1.0/(1.0+counterFalsePositives))
            elif counterFalsePositives > 0 and checkOnce == True:
                eventPerformance[k]['Precision'].append(0)
            elif counterFalsePositives == 0 and checkOnce == False:
                eventPerformance[k]['Precision'].append(1)
            elif counterFalsePositives == 0 and checkOnce == True:
                pass
            else:
                print 'event :#{}'.format(eventNumber)
                print 'K: #{}'.format(k)
                print 'False positives: {}'.format(counterFalsePositives)
                print 'CheckOnce: {}'.format(checkOnce)
                sys.exit('Problem in Precision K')
                
            if counterFalsePositives > 0:
                eventPerformance[k]['False'].append(counterFalsePositives)
            elif counterFalsePositives == 0:
                eventPerformance[k]['False'].append(0)
            else:
                sys.exit('Problem in False')

result = {}
Precision = []
Recall = []
FalsePositives = []
Delay = []

errorPrecision = []
errorRecall = []
errorFalsePositives = []
errorDelay = []

"""Organize results for increasing K"""
for k in range(1, kMAX+1):
    
    Precision.append(np.mean(eventPerformance[k]['Precision']))
    errorPrecision.append(sms.DescrStatsW(eventPerformance[k]['Precision']).tconfint_mean()[1]-np.mean(eventPerformance[k]['Precision']))
    
    Recall.append(np.mean(eventPerformance[k]['Recall']))
    errorRecall.append(sms.DescrStatsW(eventPerformance[k]['Recall']).tconfint_mean()[1]-np.mean(eventPerformance[k]['Recall']))
    
    FalsePositives.append(np.mean(eventPerformance[k]['False']))
    errorFalsePositives.append(sms.DescrStatsW(eventPerformance[k]['False']).tconfint_mean()[1]-np.mean(eventPerformance[k]['False']))            
           
    Delay.append(np.mean(eventPerformance[k]['Delay']))         
    errorDelay.append(sms.DescrStatsW(eventPerformance[k]['Delay']).tconfint_mean()[1]-np.mean(eventPerformance[k]['Delay']))
    
result['Precision'] = Precision 
result['errPrecision'] = errorPrecision

result['Recall'] = Recall
result['errRecall'] = errorRecall

result['FalseRate'] = FalsePositives
result['errFalseRate'] = errorFalsePositives

result['Delay'] = Delay
result['errDelay'] = errorDelay

"""Write the results on "resultsKS.json" file, in the "Visualization" folder"""
with open('Visualization/resultsKS_'+configuration['featureModel']+'.json', 'w') as outfile:
   json.dump(result, outfile, indent=2)