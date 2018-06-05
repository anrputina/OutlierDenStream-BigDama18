#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 16:53:52 2018

@author: andrian
"""

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "DenStream"))

import copy

### MATH, TIME, JSON
import json
import time
import numpy as np
import pandas as pd

### Anomaly DenStream Algorithm library
from sample import Sample
from DenStream import DenStream
from statistics import Statistics
from readGroundTruth import groundTruth

### Visualization library
from visualization import Visualization
from multiprocessing import Process

def normalize_matrix(df):
	return (df - df.mean())/df.std()

def main(configuration):

	resultByNode = {}

	totalExecutionTime = []

	for dataset in configuration['dataset']['list']:

		"""Iterate on all the datasets chosen in the configuration list and read the ground truth file"""
		truth = groundTruth('GrounTruth/'+dataset+'.txt', fileType='csv')

		"""Iterate on all the nodes chosen in the configuration file"""
		for node in configuration['nodes']:

			"""Read node dataset"""
			print 'Dataset {} - Node: {} loading ...'.format(dataset,node),
			df = pd.read_csv(configuration['dataset']['path']+node+dataset+'.csv', low_memory = False)\
							.dropna()\
							.drop('Unnamed: 0', axis=1)
			print 'Done.'

			times = df['time'].astype('int')
			df = df.drop(['time'], axis=1)

			"""Select the chosen features in the configuration file"""
			"""By default the dataset contains all the features"""
			"""If ControlPlane is chosen: only the CP features are extracted from the dataset"""
			"""If DataPlane is chosen: the CP features are discarded, obtaining a dataset with only DataPlane"""
			"""If CompleteFeatures is chosen: pass"""
			if configuration['featureModel'] == 'ControlPlane':
				df = df[configuration['featureList']]
			elif configuration['featureModel'] == 'DataPlane':
				df = df.drop(configuration['featureList'], axis=1)
			elif configuration['featureModel'] == 'CompleteFeatures':
				pass
			else:
				sys.exit('Something wrong in configuration feature model')

			"""Dataset normalization"""	
			df = df.loc[:,df.std()!=0]
			dfNormalized = normalize_matrix(df).dropna(axis=1)
           
			bufferDF = dfNormalized[0:configuration['sampleSkip']]
			testDF = dfNormalized[configuration['sampleSkip']:]

			"""Anomaly DenStream initialization with the parameters in the configuration file"""
			aden = DenStream(lamb = configuration['denstreamParameters']['lambda'],\
							epsilon = configuration['denstreamParameters']['epsilon'],\
							beta = configuration['denstreamParameters']['beta'],\
							mu = configuration['denstreamParameters']['mu'],\
							startingBuffer = bufferDF,
							tp = configuration['denstreamParameters']['tp'])
			aden.runInitialization()

			"""Iterate on all the rows in the dataset and run .runOnNewSample() method of the algorithm"""
			"""The algorithm tries to merge the new sample to the existing clusters"""
			"""If the algorithm merges the sample to a core-mmc: the sample is considered Normal and returns False"""
			"""If the algorithm merges the sample to a outlier-mc or generates a new outlier-mc: the sample is considered Anomalous and returns True""" 
			print 'Running algorithm ...',
			startingSimulation = time.time()
			outputCurrentNode = []
			for sampleNumber in range(len(testDF)):
				sample = testDF.iloc[sampleNumber]
				result = aden.runOnNewSample(Sample(sample.values, times.iloc[sampleNumber]))
				outputCurrentNode.append(result)
			### END Running ###
			endSimulation = time.time() - startingSimulation
			totalExecutionTime.append(endSimulation)
			print 'Done in {}'.format(endSimulation)

			df['result'] = [False] * configuration['sampleSkip'] + outputCurrentNode

			"""Depending on the detection criterion chosen in the configuration file the script produces:"""
			"""1- Results and statistics compared to grountruth if timedetection chosen"""
			"""2- Results for each node if spatialdetection chosen. To compare the results with the groundtruth there is the need to run spatialPerformance.py"""
			if configuration['detectionCriterion'] == 'spatialDetection':
				df['time'] =  times
				df[['result','time']].to_csv('Data/ResultsSpatialDetection/'+configuration['featureModel']+'/'+dataset+'_DENSTREAM_'+node+'.csv', sep=',')

			elif configuration['detectionCriterion'] == 'timeDetection':
				statistics = Statistics(node, truth)
				resultByNode[node+dataset] = statistics.getNodeResult(df, times, kMAX=5)
			else:
				sys.exit('Error detectionCriterion')

	"""	Print result on file if multicoreAnalysis ON. Used only for grid optimization. Very long task""" 
	if configuration['multicoreAnalysis']['ON'] == 'YES':
		path = "DataPlane/"
		with open("Results/"+path+str(configuration["algorithmParameters"]["lambda"])+"_"+str(configuration["algorithmParameters"]["beta"])+"_PRF.json", "w") as outputfile:
			json.dump(statistics.getPrecisionRecallFalseRate(resultByNode, kMAX=5, plot=False), outputfile, indent=4, sort_keys=True)

		resultdelay = statistics.getDelay(resultByNode, kMAX=5, plot=False)

		record = {}

		for row in range(len(resultdelay[0])):
			record['k'+str(row+1)] = list(resultdelay[0][row])

		for row in range(len(resultdelay[1])):
			record['hop'+str(row)] = list(resultdelay[1]['hop'+str(row)])

		with open("Results/"+path+str(configuration["algorithmParameters"]["lambda"])+"_"+str(configuration["algorithmParameters"]["beta"])+"_delay.json", "w") as outputfile:
			json.dump(record, outputfile, indent=4, sort_keys=True)

		with open("Results/"+path+str(configuration["algorithmParameters"]["lambda"])+"_"+str(configuration["algorithmParameters"]["beta"])+"_execTime.json", "w") as outputfile:
			json.dump({'execTime':totalExecutionTime}, outputfile, indent=4, sort_keys=True)

	else:
		"""Compute statistics if time detection chosen"""
		"""The script compares the results with the ground truth and computes precision/recall"""
		"""In the end, writes the results on "resultsKT.json" file, in the "Visualiation" folder""" 
		if configuration['detectionCriterion'] == 'timeDetection':
			resStatistics =  statistics.getPrecisionRecallFalseRate(resultByNode, kMAX=5, plot=True)
			resDelay =  statistics.getDelay(resultByNode, kMAX=5, plot=True)

			print resStatistics
			print resDelay

			resStatistics['Delay'] = resDelay[0][:,0].tolist()
			resStatistics['errDelay'] = resDelay[1]['hop0'].tolist()

			with open('Visualization/resultsKT_'+configuration['featureModel']+'.json', 'w') as outfile:
			    json.dump(resStatistics, outfile, indent=2)

			print 'Time: {}'.format(np.sum(totalExecutionTime))

		"""return all the variables"""
		return aden, truth, df, times, dfNormalized

if __name__ == "__main__":
	"""Load configuration file"""
	configuration = json.load(open('configuration.json'))

	"""Generate subprocess if multicoreAnalysis. Used only for grid optimization. Very long task"""
	if configuration['multicoreAnalysis']['ON'] == 'YES':
		lambdas = np.arange(configuration['multicoreAnalysis']["lambda"][0],
							configuration['multicoreAnalysis']["lambda"][1],
							configuration['multicoreAnalysis']["lambda"][2])

		betas = np.arange(configuration['multicoreAnalysis']["beta"][0],
							configuration['multicoreAnalysis']["beta"][1],
							configuration['multicoreAnalysis']["beta"][2])

		workersCountMax = 36
		workersList = []
		for lamb in lambdas:
			for beta in betas:
					
					algorithmParameters = {
						"sampleSkip": 39,
						"lambda": lamb,
						"epsilon": "auto",
						"beta": beta,
						"mu": "auto",
						"Kmax": 5
					}

					configuration['algorithmParameters'] = algorithmParameters

					p = Process(target=main, args=(copy.deepcopy(configuration),))

					workersList.append(p)

					if len(workersList) == workersCountMax:

						for p in workersList:
							p.start()

						for p in workersList:
							p.join()

						workersList=[]

	else:
		"""start the script"""
		aden, truth, df, times, dfNorm = main(configuration)

#"""Plot results for each node"""
#from visualization import Visualization
#v = Visualization()
#v.plotResult(df, times, truth)