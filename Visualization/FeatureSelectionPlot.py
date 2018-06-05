#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 15:13:36 2018

@author: andrian
"""

import json
import numpy as np
import matplotlib.pyplot as plt

"""
Plot the results which compares the subset of features
Note: Need to run the scripts which create the results.
"""

N = 2
index = np.arange(N)
width = 0.2

### PRECISION ###
PrecisionData = np.array(json.loads(open('resultsKT_DataPlane.json').read())['Precision'][1:3])
PrecisionComplete = np.array(json.loads(open('resultsKT_CompleteFeatures.json').read())['Precision'][1:3])
PrecisionControl = np.array(json.loads(open('resultsKT_ControlPlane.json').read())['Precision'][1:3])

PrecisionComplete = PrecisionComplete - PrecisionData
PrecisionControl = PrecisionControl - PrecisionComplete - PrecisionData
#### END PRECISION STRUCTURE####

### RECALL ###
RecallData = np.array(json.loads(open('resultsKT_DataPlane.json').read())['Recall'][1:3])
RecallControl = np.array(json.loads(open('resultsKT_ControlPlane.json').read())['Recall'][1:3])
RecallComplete = np.array(json.loads(open('resultsKT_CompleteFeatures.json').read())['Recall'][1:3])

RecallControl = RecallControl - RecallData
RecallComplete = RecallComplete - RecallControl - RecallData
### END RECALL ###

### FALSE ALARMS ###
FalseControl = np.array(json.loads(open('resultsKT_ControlPlane.json').read())['FalseRate'][1:3])
FalseComplete = np.array(json.loads(open('resultsKT_CompleteFeatures.json').read())['FalseRate'][1:3])
FalseData = np.array(json.loads(open('resultsKT_DataPlane.json').read())['FalseRate'][1:3])

FalseComplete = FalseComplete - FalseControl
FalseData = FalseData - FalseComplete
### END FALSE ALARMS ###

colorData = 'goldenrod'
colorComplete = 'firebrick'
colorControl = 'gray'

alphaCP = 0.2
alphaCPDP = 0.5
alphaDP = 1

colorPrecision = 'goldenrod'
colorRecall = 'darkorange'
colorFalse = 'firebrick'

hatchData = '\\\\'
hatchComplete = 'xx'
hatchControl = '//'

# # ### SINGLE PLOT KT### 

# fig, ax = plt.subplots(figsize=(13,6))

# bar = ax.bar(index, PrecisionData, hatch=hatchData, color=colorData, width=width, edgecolor='black', label='DataPlane')
# bar2 = ax.bar(index, PrecisionComplete, bottom=PrecisionData, color=colorComplete, width=width, edgecolor='black', hatch=hatchComplete, label='Complete')
# bar3 = ax.bar(index, PrecisionControl, bottom=PrecisionData+PrecisionComplete, hatch=hatchControl, color=colorControl, width=width, edgecolor='black', label='ControlPlane') 

# ax.bar(index+width, RecallData, hatch=hatchData, width=width, color=colorData, edgecolor='black')
# ax.bar(index+width, RecallControl, bottom=RecallData, hatch=hatchControl, width=width, color=colorControl, edgecolor='black')
# ax.bar(index+width, RecallComplete, bottom=RecallData+RecallControl, hatch=hatchComplete, width=width, color=colorComplete, edgecolor='black') 

# ax.bar(index+width*2, FalseControl, hatch=hatchControl, width=width, color=colorControl, edgecolor='black')
# ax.bar(index+width*2, FalseComplete, bottom=FalseControl, hatch=hatchComplete, width=width, color=colorComplete, edgecolor='black')
# ax.bar(index+width*2, FalseData, bottom=FalseComplete+FalseControl, hatch=hatchData, width=width, color=colorData, edgecolor='black') 


# ax.set_xticks(index+width)
# ax.set_xticklabels(['$K_{t}=2$', '$K_{t}=3$'])
# ax.tick_params(axis='x', which='major', pad=100)


# ax.text(-0.1, -0.05, 'Precision', fontsize=20, rotation=45)
# ax.text(0.1, -0.05, 'Recall', fontsize=20, rotation=45)
# ax.text(+0.25, -0.05, 'False Rate', fontsize=20, rotation=45)

# ax.text(1 - 0.1, -0.05, 'Precision', fontsize=20, rotation=45)
# ax.text(1.1, -0.05, 'Recall', fontsize=20, rotation=45)
# ax.text(1 +0.25, -0.05, 'False Rate', fontsize=20, rotation=45)

# ax.grid(c='grey', linestyle='--')

# plt.legend(bbox_to_anchor=(0, 1.2), fontsize=25,
#            fancybox=False, shadow=False, ncol=3, frameon=False, loc="upper left")

# # # fig.savefig('ComparisonCompleteCPDP.pdf', bbox_inches='tight', pad_inches=0)

# ###################
# ### SINGLE PLOT KS
# ###################


PrecisionDataKS = np.array(json.loads(open('resultsKS_DataPlane.json').read())['Precision'][1:3])
PrecisionCompleteKS = np.array(json.loads(open('resultsKS_CompleteFeatures.json').read())['Precision'][1:3])
PrecisionControlKS = np.array(json.loads(open('resultsKS_ControlPlane.json').read())['Precision'][1:3])

PrecisionCompleteKS = PrecisionCompleteKS - PrecisionDataKS
PrecisionControlKS = PrecisionControlKS - PrecisionCompleteKS - PrecisionDataKS

### RECALL ###
RecallDataKS = np.array(json.loads(open('resultsKS_DataPlane.json').read())['Recall'][1:3])
RecallControlKS = np.array(json.loads(open('resultsKS_ControlPlane.json').read())['Recall'][1:3])
RecallCompleteKS = np.array(json.loads(open('resultsKS_CompleteFeatures.json').read())['Recall'][1:3])

RecallControlKS = RecallControlKS - RecallDataKS
RecallCompleteKS = RecallCompleteKS - RecallControlKS - RecallDataKS
### END RECALL ###

### FALSE ALARMS ###
FalseControlKS = np.array(json.loads(open('resultsKS_ControlPlane.json').read())['FalseRate'][1:3])
FalseCompleteKS = np.array(json.loads(open('resultsKS_CompleteFeatures.json').read())['FalseRate'][1:3])
FalseDataKS = np.array(json.loads(open('resultsKS_DataPlane.json').read())['FalseRate'][1:3])

FalseCompleteKS = FalseCompleteKS - FalseControlKS
FalseDataKS = FalseDataKS - FalseCompleteKS
### END FALSE ALARMS ###


########################################
###### PLOT BOTH #######################
########################################

fig, ax = plt.subplots(1, 2, sharey=True, figsize=(13,4))  

bar = ax[0].bar(index, PrecisionData, hatch=hatchData, color=colorPrecision, width=width, edgecolor='black', label='DataPlane', alpha=alphaDP)
bar2 = ax[0].bar(index, PrecisionComplete, bottom=PrecisionData, color=colorPrecision, width=width, edgecolor='black', hatch=hatchComplete, label='CP+DP', alpha=alphaCPDP)
bar3 = ax[0].bar(index, PrecisionControl, bottom=PrecisionData+PrecisionComplete, hatch=hatchControl, color=colorPrecision, width=width, edgecolor='black', label='ControlPlane', alpha=alphaCP) 

ax[0].bar(index+width, RecallData, hatch=hatchData, width=width, color=colorRecall, edgecolor='black', alpha=alphaDP)
ax[0].bar(index+width, RecallControl, bottom=RecallData, hatch=hatchControl, width=width, color=colorRecall, edgecolor='black', alpha=alphaCP)
ax[0].bar(index+width, RecallComplete, bottom=RecallData+RecallControl, hatch=hatchComplete, width=width, color=colorRecall, edgecolor='black', alpha=alphaCPDP) 

ax[0].bar(index+width*2, FalseControl, hatch=hatchControl, width=width, color=colorFalse, edgecolor='black', alpha=alphaCP)
ax[0].bar(index+width*2, FalseComplete, bottom=FalseControl, hatch=hatchComplete, width=width, color=colorFalse, edgecolor='black', alpha=alphaCPDP)
ax[0].bar(index+width*2, FalseData, bottom=FalseComplete+FalseControl, hatch=hatchData, width=width, color=colorFalse, edgecolor='black', alpha=alphaDP) 


ax[0].set_xticks(index+width)
ax[0].set_xticklabels(['$K_{T}=2$', '$K_{T}=3$'])
ax[0].tick_params(axis='x', which='major', pad=100)

shiftDown = -0.08

ax[0].text(-0.35, shiftDown, 'Precision', fontsize=20, rotation=45)
ax[0].text(-0.05, shiftDown, 'Recall', fontsize=20, rotation=45)
ax[0].text(0, shiftDown, 'False Rate', fontsize=20, rotation=45)

ax[0].text(0.65, shiftDown, 'Precision', fontsize=20, rotation=45)
ax[0].text(0.95, shiftDown, 'Recall', fontsize=20, rotation=45)
ax[0].text(1, shiftDown, 'False Rate', fontsize=20, rotation=45)

ax[0].grid(c='grey', linestyle='--')


bar = ax[1].bar(index, PrecisionDataKS, hatch=hatchData, color=colorPrecision, width=width, edgecolor='black', alpha=alphaDP)
bar2 = ax[1].bar(index, PrecisionCompleteKS, bottom=PrecisionDataKS, color=colorPrecision, width=width, edgecolor='black', hatch=hatchComplete, alpha=alphaCPDP)
bar3 = ax[1].bar(index, PrecisionControlKS, bottom=PrecisionDataKS+PrecisionCompleteKS, hatch=hatchControl, color=colorPrecision, width=width, edgecolor='black', alpha=alphaCP) 

ax[1].bar(index+width, RecallDataKS, hatch=hatchData, width=width, color=colorRecall, edgecolor='black', alpha=alphaDP)
ax[1].bar(index+width, RecallControlKS, bottom=RecallDataKS, hatch=hatchControl, width=width, color=colorRecall, edgecolor='black', alpha=alphaCP)
ax[1].bar(index+width, RecallCompleteKS, bottom=RecallDataKS+RecallControlKS, hatch=hatchComplete, width=width, color=colorRecall, edgecolor='black', alpha=alphaCPDP) 

ax[1].bar(index+width*2, FalseControlKS, hatch=hatchControl, width=width, color=colorFalse, edgecolor='black', alpha=alphaCP)
ax[1].bar(index+width*2, FalseCompleteKS, bottom=FalseControlKS, hatch=hatchComplete, width=width, color=colorFalse, edgecolor='black', alpha=alphaCPDP)
ax[1].bar(index+width*2, FalseDataKS, bottom=FalseCompleteKS+FalseControlKS, hatch=hatchData, width=width, color=colorFalse, edgecolor='black', alpha=alphaDP) 

fakeLegendPlots = [0,0]

ax[1].bar(index, fakeLegendPlots, hatch=hatchControl, width=width, color=colorFalse, edgecolor='black', alpha=alphaCP, facecolor = 'none', label='CP')
ax[1].bar(index, fakeLegendPlots, hatch=hatchComplete, width=width, color=colorComplete, edgecolor='black', alpha=alphaCPDP, facecolor = 'none', label='CP+DP')
ax[1].bar(index, fakeLegendPlots, hatch=hatchData, width=width, color=colorData, edgecolor='black', alpha=alphaDP, facecolor = 'none', label='DP')

ax[1].set_xticks(index+width)
ax[1].set_xticklabels(['$K_{S}=2$', '$K_{S}=3$'])
ax[1].tick_params(axis='x', which='major', pad=100)


ax[1].text(-0.35, shiftDown, 'Precision', fontsize=20, rotation=45)
ax[1].text(-0.05, shiftDown, 'Recall', fontsize=20, rotation=45)
ax[1].text(+0, shiftDown, 'False Rate', fontsize=20, rotation=45)

ax[1].text(0.65, shiftDown, 'Precision', fontsize=20, rotation=45)
ax[1].text(0.95, shiftDown, 'Recall', fontsize=20, rotation=45)
ax[1].text(1, shiftDown, 'False Rate', fontsize=20, rotation=45)

ax[1].grid(c='grey', linestyle='--')

plt.legend(bbox_to_anchor=(-0.8, 1.25), fontsize=25,
           fancybox=False, shadow=False, ncol=3, frameon=False, loc="upper left")

fig.savefig('ComparisonCompleteCPDP.pdf', bbox_inches='tight', pad_inches=0)