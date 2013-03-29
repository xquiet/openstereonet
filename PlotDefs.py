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

#import matplotlib
#matplotlib.use('WXAgg')

from matplotlib.patches import Arc
import MiscDefs as md

import numpy as np


##function for ploting poles to planes 
def PolesPlanes(gridtype,azim,dip):
    """function to plot poles to planes"""
    if gridtype == 'schmidt':
        sqrt2 = np.sqrt(2)
        azimRad_pi = [np.radians(i) + np.pi for i in azim] # convert azimuth to radians and adds pi
        dip_rad_half = [np.radians(i)/2 for i in dip] # converts dip to radians and divide by 2
        rad_circ = [1 * sqrt2 * np.sin(i) for i in dip_rad_half] # calculates radii on stereonet
    elif gridtype == 'wulff':
        azimRad_pi = [np.radians(i) + np.pi for i in azim] # convert azimuth to radians and adds pi
        dip_rad_half = [np.radians(i)/2 for i in dip] # converts dip to radians and divide by 2
        rad_circ = [1 * np.tan(i) for i in dip_rad_half] # calculates radii on stereonet

    x_pole = []
    y_pole = []
    for i in range(len(azim)):
        x_pole.append(rad_circ[i] * np.sin(azimRad_pi[i]))
        y_pole.append(rad_circ[i] * np.cos(azimRad_pi[i]))

    return x_pole, y_pole


##function for ploting poles to lines 
def PolesLines(gridtype,azim,dip):
    """function to plot poles to lineations"""

    if gridtype == 'schmidt':
        sqrt2 = np.sqrt(2)
        azimRad = [np.radians(i) for i in azim] # convert azimuth to radians
        dip_rad_half = [np.radians(i)/2 for i in dip] # converts dip to radians and divide by 2
        rad_circ = [1 * sqrt2 * np.sin(np.pi/4 - i) for i in dip_rad_half] # calculates radii on stereonet
    elif gridtype == 'wulff':
        azimRad = [np.radians(i) for i in azim] # convert azimuth to radians
        dip_rad_half = [np.radians(i)/2 for i in dip] # converts dip to radians and divide by 2
        rad_circ = [1 * np.tan(np.pi/4 - i) for i in dip_rad_half] # calculates radii on stereonet

    x_line = []
    y_line = []
    for i in range(len(azim)):
        x_line.append(rad_circ[i] * np.sin(azimRad[i]))
        y_line.append(rad_circ[i] * np.cos(azimRad[i]))

    return x_line, y_line


#function for ploting great circles (Wulff) - from Richter & Krejci 1994 - CAGEO v.20(1)
def GreatCircleWulff(azim,dip):
    """Function to plot great circles of planes in stereonet (Wulff) 
        from Richter & Krejci 1994 - CAGEO v.20(1) and from 
        Langtangen (2009) - A Primer on Scientific Programming with Python (Springer) """

    listXY = []
    for i in range(len(azim)):
        if dip[i] == 90: dip[i] = 89.99
        ddir = azim[i] - 90
        dist = np.tan(np.radians(dip[i]))
        rad = np.tan(np.radians((90-dip[i])/2))
        R = dist + rad
        h = 0 + dist * np.cos(np.radians(ddir-180))
        k = 0 - dist * np.sin(np.radians(ddir-180))
        start = np.radians(270 - ddir + dip[i])
        opening = np.radians(2*(90-dip[i]))
        t = np.linspace(start, start + opening, 181)
        x = h + R*np.cos(t)
        y = k + R*np.sin(t)
        listXY.append(zip(x,y))

    return listXY

#function for ploting great circles (Wulff) - from Richter & Krejci 1994 - CAGEO v.20(1)
#for plotting using Line2D instead of LineCollection
#used for grid plotting (StereoPanel:PlotStereoNetGridWulff)
def GreatCircleWulffLine2D(azim,dip):
    """Function to plot great circles of planes in stereonet (Wulff) - for plotting using Line2D instead of LineCollection
        from Richter & Krejci 1994 - CAGEO v.20(1) and from 
        Langtangen (2009) - A Primer on Scientific Programming with Python (Springer) """

#    for i in range(len(azim)):
    if dip == 90: dip = 89.99
    ddir = azim - 90
    dist = np.tan(np.radians(dip))
    rad = np.tan(np.radians((90-dip)/2))
    R = dist + rad
    h = 0 + dist * np.cos(np.radians(ddir-180))
    k = 0 - dist * np.sin(np.radians(ddir-180))
    start = np.radians(270 - ddir + dip)
    opening = np.radians(2*(90-dip))
    t = np.linspace(start, start + opening, 181)
    x = h + R*np.cos(t)
    y = k + R*np.sin(t)

    return x,y


#function for ploting great circles (Schmidt) - From RFOC - FAST!!
def GreatCircleSchmidt(strike,dip):
    """FROM RFOC - function to plot great circles of planes in stereonet using STRIKE/dip"""

    listXY = []
    sqrt2 = np.sqrt(2)
    for i in range(len(strike)):
        beta = np.radians(strike[i])
        phi = np.radians(np.arange(-90,92,2)) # * np.pi/180 # steps to draw each great circle (in radians)
        lamb = np.radians((90 - dip[i]))
        alpha = np.arccos(np.cos(phi) * np.cos(lamb))       
        tq = sqrt2 * np.sin(alpha/2)
        sint = np.sin(phi) / np.sin(alpha)
        temps = 1 - (sint * sint)
        x = tq * np.sqrt(temps)
        y = tq * sint
        x1 = np.cos(beta) * x + np.sin(beta) * y
        y1 = -np.sin(beta) * x + np.cos(beta) * y
        listXY.append(zip(x1,y1))

    return listXY


#function for ploting small circles (Schmidt) - From RFOC
def SmallCircleSchmidt(az,iang,alpha,full):#,circcol,circsty,circwdt):
    """FROM RFOC - function to plot small circles of planes in stereonet"""
    #az: azimuh of cone axis
    #iang: dip of cone axis
    #alpha: width of cone, in degrees

    listXY =[]
    for i in range(len(az)):
        N = 200
        phi = np.linspace(0,2*np.pi,N)
        theta = np.radians(alpha[i])
        x = 1 * np.sin(theta) * np.cos(phi)
        y = 1 * np.sin(theta) * np.sin(phi)
        z = [1 * np.cos(theta)] * len(phi)
        d = np.mat([x,y,z])
        D = np.transpose(d)
        ry = md.roty3(90.0-iang[i])
        rz = md.rotz3(az[i])
        Rmat = ry * rz # matrix multiplication
        g = D * Rmat
        r2 = [np.sqrt(g[i,0]**2 + g[i,1]**2 + g[i,2]**2) for i in range(N)]
        phi2 = [np.arctan2(g[i,1],g[i,0]) for i in range(N)]
        theta2 = [np.arccos(g[i,2]/r2[i]) for i in range(N)]

        if full == 0: # plot just the part of the circle inside the stereonet
            xsc, ysc = md.takeoff(np.degrees(phi2), np.degrees(theta2))
            diss = np.sqrt((xsc[0:len(xsc)-1] - xsc[1:len(xsc)])**2 + (ysc[0:len(xsc)-1] - ysc[1:len(xsc)])**2)
            ww=np.where(diss>0.999)[0]
            if len(ww) > 0:
                for i in ww:
                    xsc[i] = None
                    ysc[i] = None
        elif full == 1: # plot full small circle, including areas outside stereonet
            xsc, ysc = md.takeoff2(np.degrees(phi2), np.degrees(theta2))

        listXY.append(zip(xsc,ysc))

    return listXY


#function for ploting small circles (Wulff)
def SmallCircleWulff(azim,dip,alpha,full):#,circcol,circsty,circwdt):
    """function to plot small circles of planes in stereonet"""
    #az: azimuh of cone axis
    #dp: dip of cone axis
    #alpha: width of cone, in degrees

    # first we make arrays with duplicated data (on the opposite hemisphere)
    # so we can have both parts of the circle, then we eliminate the segments outside the stereonet

    listXY =[]

    az1 = np.radians(azim)
    azz = np.append(az1, [i + np.pi for i in az1]) # make array with azimuth and back-azimuths
    dpp = np.append(dip, [-i for i in dip]) # make array with dips and inverted dips
    alpha1 = np.append(alpha,alpha)

    for i in range(len(azz)):
        az = azz[i]
        dp = np.radians(dpp[i])
        theta = np.radians(alpha1[i])
        N = 541

        dpl = dp+theta
        dpm = dp-theta
        L = 1 * np.tan(np.pi/4 - (dpl/2))
        M = 1 * np.tan(np.pi/4 - (dpm/2))
        R = (M-L) / 2 # radius of small circle (projected)
        rad = L + R # radius of axis of small circle (projected)

        h = rad * np.sin(az) # center of Small Circle
        k = rad * np.cos(az) # center of Small Circle
        t = np.linspace(0, 2*np.pi, N)

        if full == 0: # plot just the part of the circle inside the stereonet
            xsc = h + R*np.cos(t)
            ysc = k + R*np.sin(t)
            diss = np.sqrt(xsc**2 + ysc**2)
            ww=np.where(diss>0.999)[0]
            if len(ww) > 0:
                for i in ww:
                    xsc[i] = None
                    ysc[i] = None
        elif full == 1: # plot full small circle, including areas outside stereonet
            xsc = h + R*np.cos(t)
            ysc = k + R*np.sin(t)

        listXY.append(zip(xsc,ysc))

    return listXY


##function for ploting slickensides
# this is too big IMO, but I can't see a shorter version for now.
def PolesSlickensides(gridtype,slip,azim,dip,trend,plunge,sense,size,footwall):
    """function to plot slickensides - returns (xy) base and tip points for arrows"""

    if gridtype == 'schmidt':
        sqrt2 = np.sqrt(2)
        if slip: # use pole of fault PLANE as reference
            azimRad = [np.radians(i) + np.pi for i in azim] # convert azimuth to radians and adds pi
            dip_rad_half = [np.radians(i)/2 for i in dip] # converts dip to radians and divide by 2
            rad_circ = [1 * sqrt2 * np.sin(i) for i in dip_rad_half] # calculates radii on stereonet
        else: # use pole of SLICKENSIDE as reference
            azimRad = [np.radians(i) for i in trend] # convert trend to radians
            dip_rad_half = [np.radians(i)/2 for i in plunge] # converts plunge to radians and divide by 2
            rad_circ = [1 * sqrt2 * np.sin(np.pi/4 - i) for i in dip_rad_half] # calculates radii on stereonet
    elif gridtype == 'wulff':
        if slip:
            azimRad = [np.radians(i) + np.pi for i in azim] 
            dip_rad_half = [np.radians(i)/2 for i in dip] 
            rad_circ = [1 * np.tan(i) for i in dip_rad_half] 
        else: 
            azimRad = [np.radians(i) for i in trend] 
            dip_rad_half = [np.radians(i)/2 for i in plunge] 
            rad_circ = [1 * np.tan(np.pi/4 - i) for i in dip_rad_half] 

    listXY = []
    undef = ['U','u','F','f','0','5',0,5] # undefined faults (or fractures)
    normal = ['N','n','2','-',2]
    inverse = ['I','i','1','+',1]
    dextral = ['D','d','3',3]
    sinistral = ['S','s','4',4]

#    print sense
    
    for i in range(len(trend)):
        if slip: # slip-linear slickensides (Hoeppner plot)
            x_base,y_base,x_tip,y_tip = arrowPointsSlip(listXY,rad_circ[i],azimRad[i],trend[i],size)

        else: # 'normal' slickensides
            x_base,y_base,x_tip,y_tip = arrowPointsSlick(listXY,rad_circ[i],azimRad[i],size)

        if sense[i] in undef :
            listXY.append([(x_base,y_base),(x_tip,y_tip)])  # undefined faults (or fractures)
        elif sense[i] in normal:
            listXY.append([(x_base,y_base),(x_tip,y_tip)])  # normal faults
        elif sense[i] in inverse:
            listXY.append([(x_tip,y_tip),(x_base,y_base)])  # inverse faults

        elif sense[i] in dextral:
            if azim[i] <= 90.0:                 # dipdir of fault plane on 1st quadrant
                if trend[i] >= azim[i] and trend[i] <= 180.0:
                    listXY.append([(x_base,y_base),(x_tip,y_tip)])
                else:
                    listXY.append([(x_tip,y_tip),(x_base,y_base)])
            elif 90.0 < azim[i] <= 270.0:       # dipdir of fault plane on 2nd and 3rd quadrants
                if trend[i] >= azim[i]:
                    listXY.append([(x_base,y_base),(x_tip,y_tip)])
                else:
                    listXY.append([(x_tip,y_tip),(x_base,y_base)])
            elif azim[i] > 270.0: 
                if trend[i] < azim[i] and trend[i] >= 180.0:
                    listXY.append([(x_tip,y_tip),(x_base,y_base)])
                else:
                    listXY.append([(x_base,y_base),(x_tip,y_tip)])

        elif sense[i] in sinistral:
            if azim[i] <= 90.0: 
                if trend[i] >= azim[i] and trend[i] <= 180.0:
                    listXY.append([(x_tip,y_tip),(x_base,y_base)])
                else:
                    listXY.append([(x_base,y_base),(x_tip,y_tip)])
            elif 90.0 < azim[i] <= 270.0:
                if trend[i] >= azim[i]:
                    listXY.append([(x_tip,y_tip),(x_base,y_base)])
                else:
                    listXY.append([(x_base,y_base),(x_tip,y_tip)])
            elif azim[i] > 270.0: 
                if trend[i] < azim[i] and trend[i] >= 180.0:
                    listXY.append([(x_base,y_base),(x_tip,y_tip)])
                else:
                    listXY.append([(x_tip,y_tip),(x_base,y_base)])
#        else: 
#            print 'fuuuuuuuu..'


    return listXY


## helper function to calculate end points of arrows for slickensides (x+dx, y+dy)(x-dx, y-dy)
def arrowPointsSlick(listXY,rad_circ,azimRad,size):
    """helper function to calculate end points of arrows for slickensides - returns (xy) base and tip points for arrows"""
    size = 0.75*size 
    x_tip=(rad_circ+size) * np.sin(azimRad)
    y_tip=(rad_circ+size) * np.cos(azimRad)
    x_base=(rad_circ-size) * np.sin(azimRad)
    y_base=(rad_circ-size) * np.cos(azimRad)
    return x_base,y_base,x_tip,y_tip


def arrowPointsSlip(listXY,rad_circ,azimRad,trend,size):
    """helper function to calculate end points of arrows for slickensides (slip-linear plot) - returns (xy) base and tip points for arrows"""
    size = 0.75*size 
    x = (rad_circ * np.sin(azimRad))
    y = (rad_circ * np.cos(azimRad))

    if trend == 0.0:
        x_tip = x
        y_tip = y + size
        x_base = x
        y_base = y - size
    elif trend == 180.0:
        x_tip = x
        y_tip = y - size
        x_base = x
        y_base = y + size
    elif trend == 90.0:
        x_tip = x + size
        y_tip = y
        x_base = x - size
        y_base = y
    elif trend == 270.0:
        x_tip = x - size
        y_tip = y
        x_base = x + size
        y_base = y
    elif trend < 90.0:
        trendRad = np.radians(trend)
        x_tip = x + (size * np.sin(trendRad))
        y_tip = y + (size * np.cos(trendRad))
        x_base = x - (size * np.sin(trendRad))
        y_base = y - (size * np.cos(trendRad))
    elif 90.0 < trend < 180.0:
        trend = 180.0 - trend
        trendRad = np.radians(trend)
        x_tip = x + (size * np.sin(trendRad))
        y_tip = y - (size * np.cos(trendRad))
        x_base = x - (size * np.sin(trendRad))
        y_base = y + (size * np.cos(trendRad))
    elif 180.0 < trend < 270.0:
        trend = trend - 180.0
        trendRad = np.radians(trend)
        x_tip = x - (size * np.sin(trendRad))
        y_tip = y - (size * np.cos(trendRad))
        x_base = x + (size * np.sin(trendRad))
        y_base = y + (size * np.cos(trendRad))
    elif trend > 270.0:
        trend = 360.0 - trend
        trendRad = np.radians(trend)
        x_tip = x - (size * np.sin(trendRad))
        y_tip = y + (size * np.cos(trendRad))
        x_base = x + (size * np.sin(trendRad))
        y_base = y - (size * np.cos(trendRad))

    return x_base,y_base,x_tip,y_tip















