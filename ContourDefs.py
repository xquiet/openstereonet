#==============================================================================#
#        OpenStereo - Open-source, Multiplatform Stereonet Analysis            #
#                                                                              #
#    Copyright (c)  2009-2011 Carlos H. Grohmann & Ginaldo A.C. Campanha.      #
#                                                                              #
#                                                                              #
#    This file is part of OpenStereo.                                          #
#                                                                              #
#    OpenStereo is free software: you can redistribute it and/or modify        #
#    it under the terms of the GNU General Public License as published by      #
#    the Free Software Foundation, either version 3 of the License, or         #
#    (at your option) any later version.                                       #
#                                                                              #
#    OpenStereo is distributed in the hope that it will be useful,             #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#    GNU General Public License for more details.                              #
#                                                                              #
#    You should have received a copy of the GNU General Public License         #
#    along with OpenStereo.  If not, see <http://www.gnu.org/licenses/>.       #
#                                                                              #
#                                                                              #
#                                                                              #
#  Developed by: Carlos H. Grohmann & Ginaldo A.C. Campanha                    #
#                Institute of Geosciences - University of Sao Paulo - Brazil   #
#                Rua do Lago, 562 - Sao Paulo - SP - Brazil - 05508-080        #
#                guano@usp.br, ginaldo@usp.br                                  #
#                http://www.igc.usp.br/openstereo                              #
#                                                                              #
#      Requirements:                                                           #
#         Python version 2.4 or higher                                         #
#         wxPython version 2.8.10 or higher                                    #
#         Matplotlib version 0.98 or higher                                    #
#         NumPy version 1.1 or higher                                          #
#==============================================================================#

import wx

import matplotlib.pyplot as plt

from matplotlib.patches import Circle
from matplotlib.mlab import griddata
from matplotlib import cm
from matplotlib.path import Path

#import matplotlib.pyplot as plt


from wx.lib.pubsub import Publisher as pub

# this is necessary as a workaround on py2exe's issues with scipy
#import scipy.misc 
#import scipy
#scipy.factorial = scipy.misc.factorial
#from scipy.interpolate import Rbf

from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection

from numpy.ma import masked_where

import MiscDefs as md
import PlotDefs as pd

import numpy as np


##function for calculating density for Shmidt nets
def CalcContourSchmidt(grdtype, azim, dip, dtype, nodes, counting, kSpin, expSpin, areaSpin, angleSpin, name):
    """function for calculate density of poles (of planes or lines) for Shmidt nets """

## create grid of counting nodes
    grid_crowns = [10.0, 15.0, 20.0, 30.0] # number of concentric circles of nodes
    grid_nodes = [331, 721, 1261, 2791] #  number of nodes for each grid_crows
    grid_outer = [60, 90, 120, 180] # number of nodes in outer circle

    gid = grid_nodes.index(nodes)
    crowns = int(grid_crowns[gid])
    grdCircs = grid_crowns[gid]
    grdNodes = grid_nodes[gid]
    grdOuter = grid_outer[gid]

    # define counting nodes grid (concentric circles)
    az = np.zeros(grdNodes) # empty array for 'azimuth' of mesh nodes
    dp = np.zeros(grdNodes) # empty array for 'dip' of mesh nodes
    node_x = np.zeros(grdNodes) # empty array for x-coordinate of mesh nodes
    node_y = np.zeros(grdNodes) # empty array for y-coordinate of mesh nodes
    n = 0  # counter
    az[0] = 0.0 # central point
    dp[0] = 90.0 # central point
    sqrt2 = np.sqrt(2)

    for i in np.arange(1,crowns+1): # concentric circles, i=grid_crowns
        m = 6*i # each circle has 'm' nodes, m=grid_nodes
        radius = i/grdCircs
        DeltaPhi = 360.0/m # np.degrees(np.pi/(3*i)) 
        for j in xrange(1,m+1):
            n = n+1 
            phi = j*DeltaPhi
            az[n] = phi # 'azimuth' of mesh nodes
            theta = 2.0 * np.arcsin(radius/sqrt2)
            dp[n] = 90.0 - np.degrees(theta) # 'dip' of mesh nodes
        dip_rad_half = [np.radians(i)/2 for i in dp] #converts dip to radians and divide by 2
        ds = [1 * sqrt2 * np.sin(np.pi/4 - i) for i in dip_rad_half] # calculates radii on stereonett - schmidt
        dw = [1 * np.tan(np.pi/4 - i) for i in dip_rad_half] # calculates radii on stereonett - wulff
        az2 = np.radians(az)
        dp2 = np.radians(dp)


# calculate node_x and node_y according to the stereonet projection
    if grdtype == 'schmidt':
        grdprj = 1
        node_x = ds * np.sin(az2)  # x-coordinate of mesh nodes
        node_y = ds * np.cos(az2)  # y-coordinate of mesh nodes
    else: # wulff
        grdprj = 2
        node_x = dw * np.sin(az2)  # x-coordinate of mesh nodes
        node_y = dw * np.cos(az2)  # y-coordinate of mesh nodes


# define limit for low-dip data and counting cone
  # counting cone (in radians): 0.14153650606311793 = np.radians(8.1094444444444438)
  # = 1% area of hemisphere (Kalkani & von Frese, 1979)
    if counting == 4:   # counting by small circle, angle
        limit = angleSpin
        count_cone = np.radians(angleSpin) 
    else:           # counting by fischer, cossine sums or small circle (% area)
        limit = 8.1095 * areaSpin
        count_cone = 0.141536 * areaSpin

    ndata = len(azim) # original data
# copy data point near primitive into upper hemisphere
    if dtype == 1: # planar data
        for i in xrange(len(azim)):
            if 90.0 - dip[i] <= limit:
                azz = azim[i] + 180.0
                if azz > 360.0:
                    azz = azim[i] + 180.0 - 360.0
                dip = np.append(dip, dip[i])
                azim = np.append(azim, azz)
    elif dtype == 2:  # linear data
        for i in xrange(len(azim)):
            if dip[i] <= limit:
                azz = azim[i] + 180.0
                if azz > 360.0:
                    azz = azim[i] + 180.0 - 360.0
                dip = np.append(dip, dip[i])
                azim = np.append(azim, azz)  

# calculate direction cosines for orientation data (include data duplicated to upper hemisphere)
    if dtype == 1: # planar data - convert to poles to planes (treat poles as lineations)
        phi_az = np.zeros(len(azim))
        az180 = np.zeros(len(azim))
        az180 = [i+180.0 if i+180.0 < 360.0 else i+180.0-360.0 for i in azim]
        theta = [90.0 - i for i in dip]  # invert dip
        Lpole,Mpole,Npole = md.DirCosineLine(az180,theta)
    elif dtype == 2: # linear data
        Lpole,Mpole,Npole = md.DirCosineLine(azim,dip)

    # calculate direction cosines for counting nodes
    Lmesh,Mmesh,Nmesh = md.DirCosineLine(az,dp)


##-------------------
## Density counting
    # this array will store the countings
    z = np.zeros(grdNodes)

    # array of cosines between grid nodes and data poles
    cosine = np.array([[(Lmesh[i]*Lpole[j]) + (Mmesh[i]*Mpole[j]) + (Nmesh[i]*Npole[j]) for j in xrange(len(azim))] for i in xrange(grdNodes)])
    arccos = np.arccos(cosine)

    # counting 
    if counting == 1: # counting by Gaussian fischer distribution (from QuickPlot)
        z = [np.sum(np.exp(kSpin*i)) for i in cosine - 1]
    elif counting == 2:  # counting by cossine sums (from Stereo32 help file)
        z = [np.sum(np.power(i,expSpin)) for i in cosine]
    else: # rbscarea or rbscangle - counting by small circle count, % area or angle
        for i in xrange(grdNodes): 
            contsum = 0
            for j in xrange(len(azim)):
                if arccos[i][j] <= count_cone:
                    contsum = contsum + 1
            z[i] = contsum

    # NOT NEEDED - THIS WAS A BUG - Thanks to Dr. Steffen Abe, Geologie-Endogene Dynamik, RWTH Aachen University
    # for finding this bug.
# equate point density for nodes on outer circle
#    for i in xrange(grdNodes-1,grdNodes-1-grdOuter/2,-1):
#        zt = z[i] + z[i-grdOuter/2]
#        z[i] = zt
#        z[i-grdOuter/2] = zt  
    
    z = np.array(z)

    # get z in percent
    z_perc = [i*100.0/ndata for i in z]
    z_perc = np.array(z_perc)


#---------------
# send stuff to StereoPanel so we can check later if density is already calculated
    pub.sendMessage('object.contour', [grdprj, dtype, name, counting, kSpin, expSpin, areaSpin, angleSpin, grdNodes, node_x, node_y, z, z_perc]) # send to StereoPanel  



# confidence cone
#   alpha95 (180.0/np.pi)*np.arccos(1-((n-R/R)*((1/P)pow(1/n-1) -1)))

    return node_x, node_y, z, z_perc


# this will grid and contour the density
def PlotContourSchmidt(grdtype, axes, caxes, azim, dip, dtype, nodes, percent, interp, grid, cstyle, ccol, cfill, clwd, cmap, contcmap, rbsc, edges, antial, minmax, zeromax, numcontours, custom, customList, rbcossum, expSpin, rbfisher, kSpin, rbscarea, areaSpin, rbscangle, angleSpin, label, status, name, fontsize):#, meshsymb, meshcol, meshsymbsize): epsilon, smoothing, 
    """function for gridding and contouring density  """

# check if density was previously calculated
    # gridding method
    if rbfisher:
        counting = 1 #'Fisher Distribution'
    elif rbcossum:
        counting = 2 #'Cossine Sum'
    elif rbscarea:
        counting = 3 #'Small Circle Count' - area
    else: #rbscangle
        counting = 4 #'Small Circle Count' - angle

    # projection
    if grdtype == 'schmidt':
        grdprj = 1
    else: # wulff
        grdprj = 2

    params = [grdprj, dtype, name, counting, kSpin, expSpin, areaSpin, angleSpin, nodes] # from properties dialog

    for i in range(len(params)):
        if status[i] == params[i]: 
            if i == len(params) - 1: # if they are all the same, assign the old values
                node_x = status[len(status) - 4]
                node_y = status[len(status) - 3]
                zint = status[len(status) - 2]
                zperc = status[len(status) - 1]
        else: # if anyone has changed, calculate density again
            node_x, node_y, zint, zperc = CalcContourSchmidt(grdtype, azim, dip, dtype, nodes, counting, kSpin, expSpin, areaSpin, angleSpin, name)
            break

# in case data should be reported as percentage, instead of absolute counting
    if percent:
        z = zperc
    else:
        z = zint

# get min and max
    zmax = z.max() # uses numpy 'max'
    znozero = [i if i>0 else zmax for i in z] # new array without the zeros
    znozero=np.array(znozero)
    zmin = znozero.min() 

# azim/dip of maximum
    zmaxi = np.where(z==zmax)[0][0] # index of zmax value
    x = node_x[zmaxi]
    y = node_y[zmaxi]
    az = np.degrees(np.arctan2(y,x))
    if 0.0 <= az < 90.0:
        az = -(az - 90.0)
    elif 90.0 <= az <= 180.0:
        az = 540.0 + (-az - 90.0)
    else:
        az = -az + 90.0
    dr = np.sqrt(x*x + y*y)
    dp = 2 * (np.arcsin(dr/np.sqrt(2)))
    dp = - (np.degrees(dp) - 90.0)

    if dtype == 1: # planar
        azp = az + 180.0
        if azp > 360.0:
            azp = az + 180.0 - 360.0
        dpp = 90.0 - dp
        pole = '(pole)'
        plane = '(plane)'

# intervals
    if minmax: # contours from minimum to maximum
        intervals = np.linspace(zmin,zmax,numcontours)
    elif zeromax: # contours from zero to maximum
        intervals = np.linspace(0,zmax,numcontours)
    else:# custom list of contour values
        intervals = [float(i) for i in customList.split(',')]

#------------------
# grid data 
    ngrid=grid
    funcs = {"Natural Neighbor":'nn', "Triangulation":'linear'}

    try:
        xi = yi = np.linspace(-1.1,1.1,ngrid)
        zi = griddata(node_x,node_y,z,xi,yi,interp=funcs[interp])
    except ValueError:
        dlg = wx.MessageDialog(None, 'Only Natural Neighbor interpolation is allowed\nif you have the \'natgrid\' toolkit installed.', 'Oooops!', wx.OK|wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        xi = yi = np.linspace(-1.1,1.1,ngrid)
        zi = griddata(node_x,node_y,z,xi,yi,interp='nn')
        pass

## grid data with RBF interpolation (SciPy)
#    ngrid=grid
#    funcs = {"Natural Neighbor":'nn', "Triangulation":'linear',"Multiquadric":'multiquadric',"Inverse Multiquadric":'inverse multiquadric',"Gaussian":'gaussian',"Linear RBF":'linear',"Cubic":'cubic',"Quintic":'quintic',"Thin-plate Spline":'thin-plate'}

## check what kind of interpolation are we using
#    if interp == 'Natural Neighbor' or interp == 'Triangulation': # Delaunay-based (mlab)
#        xi = yi = np.linspace(-1.1,1.1,ngrid)
#        zi = griddata(node_x,node_y,z,xi,yi,interp=funcs[interp])
#    else: # Radial basis functions (scipy)
#        ti = np.linspace(-1.1,1.1,ngrid)
#        xi, yi = np.meshgrid(ti, ti)
#        rbf = Rbf(node_x, node_y, z, function=funcs[interp],epsilon=epsilon,smooth=smoothing)
#        zi = rbf(xi, yi)

### we only want the points that lie inside the circle,
### so we have to create a polygon to select the interpolated values
#        polyXY = []
#        u = np.arange(0,361,1)
#        t = np.radians(u)
#        x = np.cos(t)
#        y = np.sin(t)
#        polyXY.append(zip(x,y))
#        verts = np.array(polyXY)
#        verts = verts[0]
#        xyflat = zip(xi.flat,yi.flat) 
#        pmask = points_inside_poly(xyflat, verts)
#        pmask2 = np.reshape(pmask,(ngrid,ngrid))
#        zmask = masked_where(pmask2==False,zi) # numpy.ma 
#        zi = zmask



# graphic properties
    antialiased = antial
    cmap = cm.get_cmap(cmap)
    contcmap = cm.get_cmap(contcmap)

    if cstyle == '-':
        csty = 'solid'
    elif cstyle == ':':
        csty = 'dotted'
    elif cstyle == '--':
        csty = 'dashed'
    elif cstyle == '-.':
        csty = 'dashdot'

    if cfill: # filled contours, with colormap
        c = axes.contourf(xi, yi, zi, intervals, cmap=cmap, linestyles=csty, antialiased=antialiased)
        cb = plt.colorbar(c, cax=caxes, format='%3.2f', spacing='proportional')
        for t in cb.ax.get_yticklabels():
             t.set_fontsize(9)
        if edges: # draw hollow contours over filled (possibly with some different colour)
            if rbsc: # single-color, hollow contours
                c = axes.contour(xi, yi, zi, intervals, colors=ccol, linewidths=clwd, linestyles=csty)
                cb = plt.colorbar(c, cax=caxes, format='%3.2f')
                for t in cb.ax.get_yticklabels():
                     t.set_fontsize(9)
            else: # gradient (colormap), hollow contours
                c = axes.contour(xi, yi, zi, intervals, cmap=contcmap, linewidths=clwd, linestyles=csty)
                cb = plt.colorbar(c, cax=caxes, format='%3.2f')
                for t in cb.ax.get_yticklabels():
                     t.set_fontsize(9)
    else:
        if rbsc: # single-color, hollow contours
            c = axes.contour(xi, yi, zi, intervals, colors=ccol, linewidths=clwd, linestyles=csty, label=label)
            cb = plt.colorbar(c, cax=caxes, format='%3.2f')
            for t in cb.ax.get_yticklabels():
                 t.set_fontsize(9)
        else: # gradient (colormap), hollow contours
            c = axes.contour(xi, yi, zi, intervals, cmap=contcmap, linewidths=clwd, linestyles=csty)
            cb = plt.colorbar(c, cax=caxes, format='%3.2f')
            for t in cb.ax.get_yticklabels():
                 t.set_fontsize(9)

# some texts...
    caxes.text(0.1,1.07,'Density',family='sans-serif',size=fontsize,horizontalalignment='left')

    # gridding method
    if rbfisher:
        interp_met = 'Fisher Distribution'
        spin_angle = ''
    elif rbcossum:
        interp_met = 'Cossine Sum'
        spin_angle = ''
    elif rbscarea:
        interp_met = 'Small Circle Count'
        spin_angle = '(%2.1f %% area)' % areaSpin
    else: #rbscangle
        interp_met = 'Small Circle Count'
        spin_angle = '(%2.1f degrees cone)' % angleSpin

    # grid density
    if nodes == 331:
        grd_dens = 'Crude'
    elif nodes == 721:
        grd_dens = 'Low'
    elif nodes == 1261:
        grd_dens = 'Medium'
    elif nodes == 2791:
        grd_dens = 'High'

    # percent or times counted
    if percent:
        counts = '%'
    else:
        counts = 'times'

    if dtype == 1: # planar
        denstext = '''
Poles to Planes
%s

Maximum density: %3.1f %s
    at %3.1f/%3.1f %s
        %3.1f/%3.1f %s

Grid detail: %s

Counting method: 
    %s 
    %s

''' % (name, zmax, counts, az, dp, pole, azp, dpp, plane, grd_dens, interp_met, spin_angle)

    else: # linear
        denstext = '''
Lineations 
%s

Maximum density: %3.1f %s
    at %3.1f/%3.1f

Grid detail: %s

Counting method: 
    %s
    %s

''' % (name, zmax, counts, az, dp, grd_dens, interp_met, spin_angle)



    caxes.text(4.5,1.05, denstext, family='sans-serif',size=fontsize,horizontalalignment='left', verticalalignment='top')




#    plt.clabel(c)
#--------------------------------------------------------------------------------------------
# Extra Stuff - mostly used for testing and debugging
#--------------------------------------------------------------------------------------------
## plot grid nodes
#    axes.plot(node_x,node_y, '+', c='red', ms=4)
#    for i in range(grdNodes):
#        axes.text(node_x[i],node_y[i],'%d' % i,family='sans-serif',size='x-small',horizontalalignment='right')

## plot z values
#    for i in range(grdNodes):
##        axes.text(node_x[i],node_y[i],'%d' % i,family='sans-serif',size='x-small',horizontalalignment='right')
#        if zi[i] > 0:
#           axes.text(node_x[i],node_y[i],'%d' % zi[i],family='sans-serif',size='x-small',horizontalalignment='right')

## plot small circles (cones) around each grid node
#    alpha = [np.degrees(cone)] * grdNodes
#    listXY = pd.SmallCircleSchmidt(az,dp,alpha,1)
#    col = LineCollection(listXY, linewidths=0.5, colors='grey', linestyles='solid')
#    axes.add_collection(col, autolim=True)

## plot small circles (cones) around each grid node where counting is greater than zero
#    azi=[]
#    dpi=[]
#    api=[]
#    for i in range(grdNodes):
#        if zi[i] > 0:
#            azi.append(az[i])
#            dpi.append(dp[i])
#            api.append(np.degrees(cone))
#    listXY = pd.SmallCircleSchmidt(azi,dpi,api,1)
#    col = LineCollection(listXY, linewidths=0.5, colors='grey', linestyles='solid')
#    axes.add_collection(col, autolim=True)

## plot all data points, icluding poles duplicated to upper hemisphere
#    if dtype == 1:
#        x_pole, y_pole = pd.PolesPlanesSchmidt(azim,dip)
#    elif dtype == 2:
#        x_pole, y_pole = pd.PolesLinesSchmidt(azim,dip)
#    axes.plot(x_pole,y_pole, 'o', c='red', ms=4.5)

#--------------------------------------------------------------------------------------------







