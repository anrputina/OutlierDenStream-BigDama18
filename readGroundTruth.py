#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 17:29:39 2018

@author: andrian
"""

import pandas as pd

class groundTruth():
    
    def __init__(self, filename, fileType='txt'):
        self.filename = filename
        self.events = []
        self.clears = []
        if fileType =='txt':
            self.readFile()
        elif fileType == 'csv':
            self.readFileCsv()
        
    def addEvent(self, event):
        self.events.append(event)        
    
    def addClear(self, clear):
        self.clears.append(clear)

    # BUILD CLEAR GOOD
    def buildClear(self):

        for idx in range(len(self.events)):

            if self.events[idx]['type']=='single':

                if idx < len(self.events) - 1:

                    idx2 = idx + 1
                    if idx2 <= len(self.events) - 1:
                        while (self.events[idx2]['type']=='multiple' and idx2 < len(self.events) - 1):
                            idx2+=1

                        clearRecord = {
                            'name': 'clear'+str(idx),
                            'startTime': self.events[idx]['endTime'] + 1,
                            'endTime': self.events[idx2]['startTime'] - 1
                        }

                    self.clears.append(clearRecord)

                if idx == len(self.events) - 1:

                    clearRecord = {   
                        'name': 'clear'+str(idx),
                        'startTime': self.events[idx]['endTime'] + 1,
                        'endTime': self.events[idx]['endTime'] + 1 + 300
                        }          

                    self.clears.append(clearRecord)

        for event in self.events:
            event['type'] = 'single'
        
    def readFile(self):
        
        df = pd.read_csv(self.filename, sep='\t', header=None)
        df.columns = ["node", "ip", "startTime", "event"]
        
        df['endTime'] = df['startTime'] + 300
        df['clearStart'] = df['endTime'] + 1
        df['clearEnd'] = df['startTime'].shift(-1) - 1 - 5
        
        df['clearEnd'].iloc[-1] = 2000000000
                
        for row in df.iterrows():
        
            eventRecord = {
                    'name': row[0],
                    'startTime': row[1]['startTime'],
                    'endTime': row[1]['endTime'],
                    'node': row[1]['node'],
                    'type': 'single',
                    'ONLINE' : False,
                    'endSent': False
                }
            
            self.addEvent(eventRecord)
            
            clearRecord = {
                    'name': row[0],
                    'startTime': row[1]['clearStart'],
                    'endTime': row[1]['clearEnd']
                }
            
            self.addClear(clearRecord)

    def readFileCsv(self):
        self.df = pd.read_csv(self.filename, sep=',')
        for row in self.df.iterrows():
            eventRecord = {
                'name': row[0],
                'startTime': row[1]['Start'],
                'endTime': row[1]['End'],
                'node': row[1]['Node'],
                'type': row[1]['Type'],
                'ONLINE' : False,
                'endSent': False
            }
            self.addEvent(eventRecord)

        self.buildClear()







