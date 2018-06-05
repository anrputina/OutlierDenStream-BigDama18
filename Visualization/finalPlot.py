#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 11:10:11 2018

@author: andrian
"""

import json, sys
import numpy as np
import matplotlib.pyplot as plt

"""
Plot the results choosing the subset of features
Note: Need to run the scripts which create the results.
If you want to plot ControlPlane but you didn't run the
main in ControlPlane mode this script is not going to find the results
"""

detection = 'Temporal'
detection = 'Spatial'

featuresToPlot = 'CompleteFeatures'
#featuresToPlot = 'ControlPlane'
#featuresToPlot = 'DataPlane'


""""""


if detection == 'Temporal':    
    data = json.loads(open('resultsKT_'+featuresToPlot+'.json').read())
elif detection == 'Spatial':
    data = json.loads(open('resultsKS_'+featuresToPlot+'.json').read())
else:
    sys.exit('ERROR detection')    

figsize=(13,4)
fontlabel=25

def barRecallPrecisionFalseDelay(recall, falseRate, precision, errorsRecall, errorprecision, errorFalse, delay, errordelay):
            
        n_groups = len(recall)

        fig, ax = plt.subplots(figsize=figsize)
        index = np.arange(n_groups)
        bar_width = 0.2
        opacity = 0.7
        
        ax.bar(index-bar_width, precision, bar_width,
                 alpha=opacity,
                 color='goldenrod',
                 yerr = errorprecision,
                 ecolor = 'black',
                 edgecolor='black',
                 label='Precision',
                 hatch="//")
        
        ax.bar(index, recall, bar_width,
                 alpha=opacity,
                 color='darkorange',
                 edgecolor='black',
                 yerr = errorsRecall,
                 ecolor = 'black',
                 label='Recall',
                 hatch="xx")
        
        ax.bar(index + bar_width, falseRate, bar_width,
                 alpha=opacity,
                 yerr = errorFalse,
                 ecolor = 'black',
                 edgecolor='black',
                 color='firebrick',
                 label='False Alarms',
                 hatch="--")
            
        if detection == 'Temporal':
            ax.set_xlabel('$K_{T}$', fontsize=fontlabel)
        elif detection == 'Spatial':
            ax.set_xlabel('$K_{S}$', fontsize=fontlabel)
        else:
            pass
#        plt.ylabel('Scores', fontsize=fontlabel)
#        plt.xticks(index + bar_width/2, ('1', '2', '3', '4', '5'))
        ax.set_xticks(index + bar_width/2)
        ax.set_xticklabels(['1', '2', '3', '4', '5'])
        ax.set_xlim((-2*bar_width, index[len(index)-1]+3*bar_width))
        ax.set_ylim((0,1))
        ticks = ax.get_yticks()
        ax.set_yticks([0, 0.5, 1.0])
        ax.grid(c='gray', linestyle='--')
        
        
        delay1 = np.array(delay)
        delay2 = np.array(delay)
                    
        errordelay1 = np.array(errordelay)
        errordelay2 = np.array(errordelay)

#        delay1[1] = 0
        delay1[2] = 0
        delay1[3] = 0
        delay1[4] = 0

#        errordelay1[1] = 0
        errordelay1[2] = 0
        errordelay1[3] = 0
        errordelay1[4] = 0
        
        delay2[0] = 0
        delay2[1] = 0
       
        errordelay2[0] = 0
        errordelay2[1] = 0
        
        coloraxis2 = 'royalblue'
        ax2 = ax.twinx()
        ax2.bar(index+bar_width*2, delay1,
                bar_width, color=coloraxis2, edgecolor='black',
                yerr=errordelay1, label='Delay')

        ax2.bar(index+bar_width, delay2,
                bar_width, color=coloraxis2, edgecolor='black',
                yerr=errordelay2)
        
        ax2.tick_params('y', colors=coloraxis2)
        ax2.set_xticks(index + bar_width/2)
        ax2.set_ylabel('Delay [s]', color=coloraxis2, fontsize=fontlabel)
        ax2.set_ylim((0,60))
        ticks = ax2.get_yticks()
        ax2.set_yticks([0, 30, 60])
#        ax2.grid(c=coloraxis2, linestyle='--')
        
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.1,
                         box.width, box.height * 0.9])
        
        # Put a legend below current axis
        ax.legend(loc='upper center', bbox_to_anchor=(0.35, +1.4),
                  fancybox=False, shadow=False, ncol=3, fontsize=fontlabel, frameon=False)
        

        box = ax2.get_position()
        ax2.set_position([box.x0, box.y0 + box.height * 0.1,
                         box.width, box.height * 0.9])
        
        # Put a legend below current axis
        ax2.legend(loc='upper center', bbox_to_anchor=(1.01, +1.4),
                  fancybox=False, shadow=False, ncol=5, fontsize=fontlabel, frameon=False)
#        
##        fig.tight_layout()

        
        fig.savefig(detection+'.pdf', bbox_inches='tight', pad_inches=0)

def barRecallPrecisionDelay(recall, falseRate, precision, errorsRecall, errorprecision, errorFalse, delay, errordelay):
            

        n_groups = len(recall)

        fig, ax = plt.subplots(figsize=figsize)
        index = np.arange(n_groups)
        bar_width = 0.2
        opacity = 0.7
        
        ax.bar(index-bar_width, precision, bar_width,
                 alpha=opacity,
                 color='goldenrod',
                 yerr = errorprecision,
                 ecolor = 'black',
                 edgecolor='black',
                 label='Precision',
                 hatch="//")
        
        ax.bar(index, recall, bar_width,
                 alpha=opacity,
                 color='darkorange',
                 edgecolor='black',
                 yerr = errorsRecall,
                 ecolor = 'black',
                 label='Recall',
                 hatch="xx")
        
            
        if detection == 'Temporal':
            ax.set_xlabel('$K_{T}$', fontsize=fontlabel)
        elif detection == 'Spatial':
            ax.set_xlabel('$K_{S}$', fontsize=fontlabel)
        else:
            pass
#        plt.ylabel('Scores', fontsize=fontlabel)
#        plt.xticks(index + bar_width/2, ('1', '2', '3', '4', '5'))
        ax.set_xticks(index + bar_width/2)
        ax.set_xticklabels(['1', '2', '3', '4', '5'])
        ax.set_xlim((-2*bar_width, index[len(index)-1]+3*bar_width))
        ax.set_ylim((0,1))
        ticks = ax.get_yticks()
        ax.set_yticks([0, 0.5, 1.0])
        ax.grid(c='gray', linestyle='--')
        
        
        delay1 = np.array(delay)
        delay2 = np.array(delay)
                    
        errordelay1 = np.array(errordelay)
        errordelay2 = np.array(errordelay)

        if detection == 'Temporal':
            delay1 = delay1*5
            delay2 = delay2*5 
            errordelay1 = np.array(errordelay)*5
            errordelay2 = np.array(errordelay)*5
        
        coloraxis2 = 'royalblue'
        ax2 = ax.twinx()
        ax2.bar(index+bar_width, delay1,
                bar_width, color=coloraxis2, edgecolor='black',
                yerr=errordelay1, label='Delay')

        ax2.bar(index+bar_width, delay2,
                bar_width, color=coloraxis2, edgecolor='black',
                yerr=errordelay2)
        
        ax2.tick_params('y', colors=coloraxis2)
        ax2.set_xticks(index + bar_width/2)
        ax2.set_ylabel('Delay [s]', color=coloraxis2, fontsize=fontlabel)
        ax2.set_ylim((0,60))
        ticks = ax2.get_yticks()
        ax2.set_yticks([0, 30, 60])
#        ax2.grid(c=coloraxis2, linestyle='--')
        
#        box = ax.get_position()
#        ax.set_position([box.x0, box.y0 + box.height * 0.1,
#                         box.width, box.height * 0.9])
#        
#        # Put a legend below current axis
#        ax.legend(loc='upper center', bbox_to_anchor=(0.15, +1.4),
#                  fancybox=False, shadow=False, ncol=3, fontsize=fontlabel, frameon=False)
#        
#
#        box = ax2.get_position()
#        ax2.set_position([box.x0, box.y0 + box.height * 0.1,
#                         box.width, box.height * 0.9])
#        
#        # Put a legend below current axis
#        ax2.legend(loc='upper center', bbox_to_anchor=(1.01, +1.4),
#                  fancybox=False, shadow=False, ncol=5, fontsize=fontlabel, frameon=False)
##        
###        fig.tight_layout()

        
#        fig.savefig(detection+'.pdf', bbox_inches='tight', pad_inches=0)
        
barRecallPrecisionFalseDelay(data['Recall'], data['FalseRate'], data['Precision'], data['errRecall'], data['errPrecision'], data['errFalseRate'], data['Delay'], data['errDelay'])
#barRecallPrecisionDelay(data['Recall'], data['FalseRate'], data['Precision'], data['errRecall'], data['errPrecision'], data['errFalseRate'], data['Delay'], data['errDelay'])