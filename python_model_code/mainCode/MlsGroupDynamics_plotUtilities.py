
"""
CreateD on Oct 23 2019
Last Update Oct 23 2019

@author: simonvanvliet
Department of Zoology
University of Britisch Columbia
vanvliet@zoology.ubc.ca

Contains varies functions used in MLS model code and in figure code

"""
import numpy as np
import math
import matplotlib

# %% Set figure size in cm
def set_fig_size_cm(fig, w, h):
    cmToInch = 0.393701
    wInch = w * cmToInch
    hInch = h * cmToInch
    fig.set_size_inches(wInch, hInch)
    return None

#convert list of results to 2D matrix of offspring frac. size vs fraction of parent to offspring
def create_2d_matrix(offspr_sizeVec, offspr_fracVec, statData, fieldName):
    #get size of matrix
    numX = offspr_sizeVec.size
    numY = offspr_fracVec.size
    #init matrix to NaN
    dataMatrix = np.full((numY, numX), np.nan)

    #fill matrix
    for xx in range(numX):
        for yy in range(numY):
            #find items in list that have correct fissioning parameters for current location in matrix
            currXId = statData['offspr_size'] == offspr_sizeVec[xx]
            currYId = statData['offspr_frac'] == offspr_fracVec[yy]
            currId = np.logical_and(currXId, currYId)
            #extract output value and assign to matrix
            if currId.sum() == 1:
                dataMatrix[yy, xx] = np.asscalar(statData[fieldName][currId])
    return dataMatrix

def plot_heatmap_sub(fig, ax, xAxis, yAxis, dataMatrix, settings):
    
    dataName = settings['dataName'] if 'dataName' in settings else ''
    xstep    = settings['xstep']    if 'xstep'    in settings else 3
    ystep    = settings['ystep']    if 'ystep'    in settings else 3
    cstep    = settings['cstep']    if 'cstep'    in settings else 3
    xlabel   = settings['xlabel']   if 'xlabel'   in settings else ''
    ylabel   = settings['ylabel']   if 'ylabel'   in settings else ''
    cmap     = settings['cmap']     if 'cmap'     in settings else 'plasma'
    cmap_bad = settings['cmap_bad'] if 'cmap_bad' in settings else 'black'
    xmin     = settings['xmin']     if 'xmin'     in settings else xAxis.min()
    xmax     = settings['xmax']     if 'xmax'     in settings else xAxis.max()
    ymin     = settings['ymin']     if 'ymin'     in settings else yAxis.min()
    ymax     = settings['ymax']     if 'ymax'     in settings else yAxis.max()
    alpha    = settings['alpha']    if 'alpha'    in settings else 1

    
    
    #find max value 
    if 'roundTo' in settings:
        nanMax = max(0, np.nanmax(dataMatrix))
        nanMin = min(0, np.nanmin(dataMatrix))
        maxData = math.ceil(nanMax / settings['roundTo']) * settings['roundTo']
        minData = math.floor(nanMin / settings['roundTo']) * settings['roundTo']
    else:
        maxData = np.nanmax(dataMatrix)
        minData = np.nanmin(dataMatrix)
    
    vmax = settings['vmax'] if 'vmax' in settings else maxData
    vmin = settings['vmin'] if 'vmin' in settings else minData

    current_cmap = matplotlib.cm.get_cmap(cmap)
    current_cmap.set_bad(color=cmap_bad)
    
    #plot heatmap
    im = ax.pcolormesh(xAxis, yAxis, dataMatrix, alpha=alpha,
                       cmap=current_cmap, vmin=vmin, vmax=vmax)
    
    #add colorbar
    fig.colorbar(im, ax=ax, orientation='vertical',
                 label=dataName,
                 ticks=np.linspace(vmin, vmax, cstep), 
                 fraction=0.5, pad=0.1)

    #make axis nice
    xRange = (xmin, xmax)
    yRange = (ymin, ymax)
    ax.set_xlim(xRange)
    ax.set_ylim(yRange)
    ax.set_xticks(np.linspace(*xRange, xstep))
    ax.set_yticks(np.linspace(*yRange, ystep))

    # set labels
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    if 'title' in settings:
        ax.set_title(settings['title'])
    
    return None

#make heatmap of 2D matrix
def plot_heatmap(fig, ax, offspr_sizeVec, offspr_fracVec, statData, dataName, roundTo):
    #convert 1D list to 2D matrix
    data2D = create_2d_matrix(
        offspr_sizeVec, offspr_fracVec, statData, dataName)
    
    plotSettings = {
      'roundTo' :   roundTo,
      'dataName':   dataName,
      'vmin':       0,
      'xlabel'  :   'offspring size (frac.)',
      'ylabel'  :   'offspring frac. to parent',
    }
    
    plot_heatmap_sub(fig, ax, offspr_sizeVec, offspr_fracVec, 
                     data2D, plotSettings)

    return None

    #make heatmap of 2D matrix


#extract transect data for selected parameters
#returns vectors x and y that contain data.
# xName and yName specify field names of data to assign to x,y axis
# keyDict is dictionary specifying the desired value of all varying parameters 
def create_transect(statData, xName, yName, keyDict):
    #init logical vector
    dataIdx = np.ones_like(statData, dtype=np.int16)
    
    #filter for all keys provided in keyDict
    for key, value in keyDict.items():
        #find items in list that have correct fissioning parameters for current location in matrix
        currIdx = statData[key] == value
        dataIdx = np.logical_and(dataIdx, currIdx)
    
    #extract x,y data
    xData = statData[xName][dataIdx]
    yData = statData[yName][dataIdx]

    return (xData, yData)

#plots transect
def plot_transect(fig, ax, statData, xName, yName, keyDict, dataName):
    #convert 1D list to 2D matrix
    xData, yData = create_transect(statData, xName, yName, keyDict)

    #plot heatmap
    ax.plot(xData, yData, label=dataName)

    #make axis nice
    if xData.size > 0:
        xRange = (xData.min(), xData.max())
        yRange = (yData.min(), yData.max())
        steps = (3, 3)
        ax.set_xlim(xRange)
        #ax.set_ylim(yRange)
        ax.set_xticks(np.linspace(*xRange, steps[0]))
        #ax.set_yticks(np.linspace(*yRange, steps[1]))

    # set labels
    ax.set_xlabel(xName)
    ax.set_ylabel(yName)

    return None

#plots transect
def plot_transect_relative(fig, ax, statData, xName, yName, keyDict, keyDictBaseline, dataName):
    #convert 1D list to 2D matrix
    
    _, yDataBaseline = create_transect(statData, xName, yName, keyDictBaseline)
    nonZero = yDataBaseline != 0
    
    xData, yData = create_transect(statData, xName, yName, keyDict)
    
    yData_rel = yData[nonZero] / yDataBaseline[nonZero]

    #plot heatmap
    ax.plot(xData[nonZero], yData_rel, label=dataName)

    #make axis nice
    if xData.size > 0:
        xRange = (xData.min(), xData.max())
        yRange = (yData.min(), yData.max())
        steps = (3, 3)
        ax.set_xlim(xRange)
        #ax.set_ylim(yRange)
        ax.set_xticks(np.linspace(*xRange, steps[0]))
        #ax.set_yticks(np.linspace(*yRange, steps[1]))

    # set labels
    ax.set_xlabel(xName)
    ax.set_ylabel(yName)

    return None

def plot_mutational_meltdown(fig, ax, offSizeVec, offsFracVec, statData, plotData, keyDict, plotSettings):
    #get size of matrix
    numX = offSizeVec.size
    numY = offsFracVec.size
    #init matrix to NaN
    dataMatrix = np.full((numY, numX), np.nan)
        
    #init logical vector
    dataIdx = np.ones_like(statData, dtype=np.int16)
    
    #filter for all keys provided in keyDict
    for key, value in keyDict.items():
        #find items in list that have correct fissioning parameters for current location in matrix
        currIdx = statData[key] == value
        dataIdx = np.logical_and(dataIdx, currIdx)

    #fill matrix
    for xx in range(numX):
        for yy in range(numY):
            #find items in list that have correct fissioning parameters for current location in matrix
            currXIdx = statData['offspr_size'] == offSizeVec[xx]
            currYIdx = statData['offspr_frac'] == offsFracVec[yy]
            currId = np.logical_and.reduce((currXIdx, currYIdx, dataIdx))
            #extract output value and assign to matrix
            if currId.sum() == 1:
                dataMatrix[yy, xx] = np.asscalar(plotData[currId])
            elif currId.sum() == plotSettings['NRepeat']:
                dataMatrix[yy, xx] = np.nanmedian(plotData[currId])
            elif currId.sum()>0:
                print('error, no unique value found')

    
    plot_heatmap_sub(fig, ax, offSizeVec, offsFracVec, 
                     dataMatrix, plotSettings)            
                
    return dataMatrix

def plot_time_data(axs, dataStruc, FieldName, type='lin'):
    # linear plot
    if type == 'lin':
        axs.plot(dataStruc['time'], dataStruc[FieldName], label=FieldName)
    # log plot
    elif type == 'log':
        axs.semilogy(dataStruc['time'], dataStruc[FieldName], label=FieldName)
    # set x-label
    axs.set_xlabel("time")
    return None