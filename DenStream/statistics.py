#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 11:06:54 2017

@author: anr.putina
"""

import copy
import numpy as np

from itertools import groupby
from operator import itemgetter

from visualization import Visualization

import statsmodels.stats.api as sms


def findDistance(node, eventNode):
    
    if node == eventNode:
        return 0
    
    elif (('leaf' in node) and ('spine' in eventNode)) or (('spine' in node) and ('leaf' in eventNode)):
        return 1
    
    elif (('leaf' in node) and ('dr' in eventNode) or ('dr' in node) and ('leaf' in eventNode)):
        return 1
    
    elif ('dr' in node) and ('dr' in eventNode):
        return 1

    elif (('dr' in node) and ('spine' in eventNode) or ('spine' in node) and ('dr' in eventNode)):
        return 2
    
    elif ('leaf' in node) and ('leaf' in eventNode):
        return 2
    
    elif ('leaf' in node) and ('rswA5' in eventNode):
        return 1

    elif ('spine' in node) and ('rswA5' in eventNode):
        return 2

    elif ('dr' in node) and ('rswA5' in eventNode):
        return 2

    elif (('spine' in node) and ('spine' in eventNode)):
        return 2
    else:
        return 2

class Statistics():
    
    def __init__(self, node, truth):
        self.node = node             
        self.truth = truth

    def computeDetectionProbability(self, df, time, kMAX):

        """
        Check detection of the events.
        - Consider only the convergence interval (of each event)
        and check if K consecutive samples are labeled anomalous
        in that interval. If the event is detected, computes the 
        detection time as currentTime - event starting time.
        - The algorithm considers also the distance between the
        nodes for further investigations.
        - A dictionary with the number of detections and number
        of events is created as well as the list of delays
        """

        detections = {}

        for k in range(1, kMAX+1):
            detection = 0
            events = 0
            delays = []

            for event in self.truth.events:
                if event['type'] == 'single':
                    check = (time >= event['startTime']) & (time <= event['endTime'])
                    currentEvent = df[check]
                    indexes = currentEvent[currentEvent['result']==True].index
                    position = findDistance(self.node, event['node'])

                    lista = []
                    for key, g in groupby(enumerate(indexes), lambda (i, x): i-x):
                        lista.append(map(itemgetter(1), g))    
                    
                    checkOnce = True

                    for sub in lista:
                        if checkOnce:
                            if len(sub) > k - 1:
                                detection += 1
                                events += 1

                                eventDelay = {
                                        'type' : 'single',
                                        'position' : position,
                                        'delay': time.loc[sub[k-1]] - event['startTime']
                                        }
                                delays.append(eventDelay)
                                checkOnce = False

                    if checkOnce:
                        events += 1

            detections[k] = {'detection': detection,
                             'events': events, 
                             'delays': delays}

        return detections
                      
    def findFalsePositiveDetection(self, df, time, kMAX):

        """
        Check false positives.
        - Consider only the clear interval (after each event)
        and check if K consecutive samples are labeled anomalous
        in that interval. If true, a false alarm is generated 
        - If an alarm is raised, the system does not raise other
        alarm for the next 5 minutes (as if true event)
        - A dictionary with the number of false alarms for each 
        K is created.
        """

        false = {}
        
        for k in range(1, kMAX+1):
                        
            counterFalsePositives = 0
            for event in self.truth.clears:
                
                check = (time > event['startTime']) & (time <= event['endTime'])
                currentEvent = df[check]
                currentEvent = currentEvent.drop(currentEvent.tail(1).index)

                indexes = currentEvent[currentEvent['result']==True].index
                
                lista = []
                for key, g in groupby(enumerate(indexes), lambda (i, x): i-x):
                    lista.append(map(itemgetter(1), g))
        
                lastDetection = 0
                for sub in lista:
                    if len(sub) > k-1 and time.loc[sub[k-1]] > lastDetection + 300:
                        counterFalsePositives += 1
                        lastDetection = time.loc[sub[k-1]]

            false[k] = counterFalsePositives

        return false

    def getNodeResult(self, df, times, kMAX=5):

        """
        Computes detections/false alarms statistics
        Returns dict with the info for the current node
        """

        probabilityDetection = self.computeDetectionProbability(df, times, kMAX)
        falsePositives = self.findFalsePositiveDetection(df, times, kMAX)

        result = {
                    'detections': probabilityDetection,
                    'falsePositives': falsePositives
                }

        return result

    def getPrecisionRecallFalseRate(self, resultSimulation, kMAX, plot=False, output='dict'):

        """
        The function receives the detections/false alarms of all the nodes
        and computes the Precision/Recall for all the K.
        """

        precisionConfInterval = {}
        recallConfInterval = {}
        falseConfInterval = {}

        for k in range(1, kMAX + 1):
            precisionConfInterval[k] = []
            recallConfInterval[k] = []
            falseConfInterval[k] = []

        for key, value in resultSimulation.iteritems():

            detections = value['detections']
            falsePositives = value['falsePositives']

            for k in range(1, kMAX + 1):
                
                if detections[k]['events'] != 0:
                    recallConfInterval[k].append(detections[k]['detection']/float(detections[k]['events']))
                            
                if (detections[k]['detection'])!= 0 and falsePositives != 0:
                    precisionConfInterval[k].append((detections[k]['detection'])/(float(detections[k]['detection']) + falsePositives[k] ))    
                
                falseConfInterval[k].append(falsePositives[k]/float(len(self.truth.clears)))

        errorRecall = np.ndarray(kMAX)
        errorPrecision = np.ndarray(kMAX)
        errorFalse = np.ndarray(kMAX)

        meanRecall = np.ndarray(kMAX)
        meanPrecision = np.ndarray(kMAX)
        meanFalseRate = np.ndarray(kMAX)

        for k in range(1, kMAX + 1):
            a = recallConfInterval[k]
            meanRecall[k-1] = np.mean(a)
            interval = sms.DescrStatsW(a).tconfint_mean()    
            errorRecall[k-1] = interval[1] - np.mean(a)
            
            a = precisionConfInterval[k]
            meanPrecision[k-1] = np.mean(a)
            interval = sms.DescrStatsW(a).tconfint_mean()  
            errorPrecision[k-1] = interval[1] - np.mean(a)
            
            a = falseConfInterval[k]
            meanFalseRate[k-1] = np.mean(a)
            interval = sms.DescrStatsW(a).tconfint_mean()    
            errorFalse[k-1] = interval[1] - np.mean(a)

        if plot:
            visual = Visualization()
            visual.barRecallPrecisionvsK2(meanRecall, meanFalseRate, meanPrecision, errorRecall, errorPrecision, errorFalse)

        if output == 'dict':

            if meanFalseRate[0] > 1:
                meanFalseRate[0] = 1

            result = {

                'Precision': np.nan_to_num(meanPrecision).tolist(),
                'errPrecision': errorPrecision.tolist(),
                'Recall': np.nan_to_num(meanRecall).tolist(),
                'errRecall': errorRecall.tolist(),
                'FalseRate': np.nan_to_num(meanFalseRate).tolist(),
                'errFalseRate': errorFalse.tolist()
            }

            return result

        elif output == 'tuple':

            return meanPrecision, errorPrecision, meanRecall, errorRecall, meanFalseRate, errorFalse

        else:
            return 

    def getDelay(self, resultSimulation, kMAX, plot=False, samplingRate = 5):

        """
        The function receives the results previously obtained and computes
        the average detection delay for all the K and with respect to the 
        distance from the root node (how fare is the event).
        """

        depth = 3

        delay0 = {}
        delay1 = {}
        delay2 = {}

        for k in range(1, kMAX + 1):
            delay0[k] = []
            delay1[k] = []
            delay2[k] = []

        for key, value in resultSimulation.iteritems():

            detections = value['detections']
                        
            for k in range(1, kMAX + 1):

                delays = detections[k]['delays']
                        
                for delay in delays:
                                        
                    if delay['position'] == 0:
                        delay0[k].append(delay['delay'])
                
                    if delay['position'] == 1:
                        delay1[k].append(delay['delay'])
                
                    if delay['position'] == 2:
                        delay2[k].append(delay['delay'])
                                 
        delayConfInterval =  {'hop0': np.ndarray(kMAX),
                              'hop1': np.ndarray(kMAX),
                              'hop2': np.ndarray(kMAX)}

        delaymeansConfInterval = np.ndarray((kMAX,depth))  

        for k in range(1, kMAX + 1):
            
            a = delay0[k]
            b = delay1[k]
            c = delay2[k]
          
            delaymeansConfInterval[k-1][0] = np.mean(a)
            delaymeansConfInterval[k-1][1] = np.mean(b)
            delaymeansConfInterval[k-1][2] = np.mean(c)
            
            interval = sms.DescrStatsW(a).tconfint_mean()    
            delayConfInterval['hop0'][k-1] = interval[1] - np.mean(a)
            
            interval = sms.DescrStatsW(b).tconfint_mean()    
            delayConfInterval['hop1'][k-1] = interval[1] - np.mean(b)
            
            interval = sms.DescrStatsW(c).tconfint_mean()    
            delayConfInterval['hop2'][k-1] = interval[1] - np.mean(c)

        if plot:
            visual = Visualization()
            visual.plotBarDelay(delaymeansConfInterval, delayConfInterval, trunc='yes')

        return delaymeansConfInterval, delayConfInterval


    ###########################################################################
    ###########################################################################
    ###########################################################################
    ######### FUNCTIONS NEEDED ONLY FOR THE DEMO AVAILABLE ONLINE AT  #########
    #########               telemetry.telecom-paristech               #########
    #########       Same functions with minor modifications           #########
    ###########################################################################
    ###########################################################################
    ###########################################################################


    def getNodeResultRealTime(self, df, times, kMAX=5):

        probabilityDetection = self.computeDetectionProbabilityRealTime(df, times, kMAX)
        falsePositives = self.findFalsePositiveDetectionRealTime(df, times, kMAX)

        result = {
                    'detections': probabilityDetection,
                    'falsePositives': falsePositives
                }

        return result

    def computeDetectionProbabilityRealTime(self, df, time, kMAX):

        detections = {}

        for k in range(1, kMAX+1):
            detection = 0
            events = 0
            delays = []

            for event in self.truth.events:

                if event['ONLINE'] == True:
                    if event['type'] == 'single':
                        check = (time >= event['startTime']) & (time <= event['endTime'])
                        currentEvent = df[check]
                        indexes = currentEvent[currentEvent['result']==True].index
                        position = findDistance(self.node, event['node'])

                        lista = []
                        for key, g in groupby(enumerate(indexes), lambda (i, x): i-x):
                            lista.append(map(itemgetter(1), g))    
                        
                        checkOnce = True

                        for sub in lista:
                            if checkOnce:
                                if len(sub) > k - 1:
                                    detection += 1
                                    events += 1

                                    eventDelay = {
                                            'type' : 'single',
                                            'position' : position,
                                            'delay': time.loc[sub[k-1]] - event['startTime']
                                            }     
                                    delays.append(eventDelay)
                                    checkOnce = False

                        if checkOnce:
                            events += 1

            detections[k] = {'detection': detection,
                             'events': events, 
                             'delays': delays}

        return detections

    def findFalsePositiveDetectionRealTime(self, df, time, kMAX):

        false = {}
        
        for k in range(1, kMAX+1):
                        
            counterFalsePositives = 0
            for event in self.truth.clears:
                
                check = (time > event['startTime']) & (time <= event['endTime'])
                currentEvent = df[check]

                indexes = currentEvent[currentEvent['result']==True].index
                
                lista = []
                for key, g in groupby(enumerate(indexes), lambda (i, x): i-x):
                    lista.append(map(itemgetter(1), g))
        
                for sub in lista:
                    if len(sub) > k - 1:
                        counterFalsePositives += 1
                        
            false[k] = counterFalsePositives

        return false



