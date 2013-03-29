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

import os, sys, csv, re
import wx
import numpy as np

import EigenStat as eigen # eigenvectors stats for girdle/cluster analysis


# the original CommentedFile is from here: (I included "or not line.strip()", to deal with blank lines)
# http://www.mfasold.net/blog/2010/02/python-recipe-read-csvtsv-textfiles-and-ignore-comment-lines/

class CommentedFile:
    def __init__(self, f, commentstring=('#',';')):
        self.f = f
        self.commentstring = commentstring
    def next(self):
        line = self.f.next()
        while line.startswith(self.commentstring) or not line.strip():
            line = self.f.next()
        return line
    def __iter__(self):
        return self


def getData(filename):
    """get data from file and create lists with values and column names."""

    csvfile = open(filename,'rU') # Open the file and read the contents
    sample = csvfile.read( 1024 )# Grab a sample
    csvfile.seek( 0 )
    # fix sample for sniffer
    split = sample.splitlines()
    split = [i for i in split if not i.startswith(('#',';'))] # remove commented lines
    split = [i for i in split if not i==''] # remove blank lines
    sampleClean = '\n'.join(split)

    try:
        dialect = csv.Sniffer().sniff(sampleClean) # Check for file format with sniffer.
    except csv.Error: # in case csv cannot guess the dialect, we default to space delimited.
        csv.register_dialect('space', delimiter=' ', quoting=csv.QUOTE_NONE)
        dialect='space'

    csvfile = csv.reader(CommentedFile(open(filename, 'rU')),dialect=dialect)
    datalist = list( csvfile ) # append data to a list

    return datalist


def getDataTectonicsFP(filename):
    """import data from TectonicsFP. comma-separated, must drop first column"""

    csv.register_dialect('comma', delimiter=',', quoting=csv.QUOTE_NONE)
    dialect='comma'

    csvfile = csv.reader(CommentedFile(open(filename, 'rU')),dialect=dialect)
    datalist = list( csvfile ) # append data to a list
    datalist = [[i[1]]+[i[2]]+[i[3]]+[i[4]]+[int(i[0])/10] for i in datalist]

    return datalist


#Open file, planar data (dipdir / dip)
def doPlanarDDD(datalist):
    """get planar data"""    

    azimList = [float(val[0]) for val in datalist]
    dipdir = np.array(azimList)
    n_data = len(azimList)

    dipList=[float(val[1]) for val in datalist]
    dip1=[dp-0.01 if dp==90 else dp for dp in dipList]
    dip = np.array(dip1)

    strike1=[az+270 if 0<=az<=90 else az-90 for az in azimList]
    strike = np.array(strike1)

    if n_data > 3: # must have at least three points for eigen analysis
        az_v1,dp_v1,az_v2,dp_v2,az_v3,dp_v3,S1,S2,S3,K_x,K_y,K,C,P,G,R,Vect,confCone,confK = eigen.CalcEigenPlane(dipdir,dip)
        eigenDict = {"az_v1":az_v1,"dp_v1":dp_v1,"az_v2":az_v2,"dp_v2":dp_v2,"az_v3":az_v3,"dp_v3":dp_v3,"S1":S1,"S2":S2,"S3":S3,"K_x":K_x,"K_y":K_y,"K":K,"C":C,"P":P,"G":G,"R":R,"Vect":Vect,"confCone":confCone,"confK":confK}
    else:
        eigenDict = {"az_v1":0,"dp_v1":0,"az_v2":0,"dp_v2":0,"az_v3":0,"dp_v3":0,"S1":0,"S2":0,"S3":0,"K_x":0,"K_y":0,"K":0,"C":0,"P":0,"G":0,"R":0,"Vect":0,"confCone":0,"confK":0}

    return n_data,dipdir,dip,strike,eigenDict


#Open file, planar data (strike / dip - right hand rule)
def doPlanarRH(datalist):
    """get planar data"""    

    strikeList = [float(val[0]) for val in datalist]
    strike = np.array(strikeList)
    n_data = len(strikeList)

    dipList=[float(val[1]) for val in datalist]
    dip1=[dp-0.01 if dp==90 else dp for dp in dipList]
    dip = np.array(dip1)

    strike1=[90.0-(450.0-(st+90.0)) if (st+90.0)>360.0 else st+90.0 for st in strikeList]
    dipdir = np.array(strike1)

    if n_data > 3: # must have at least three points for eigen analysis
        az_v1,dp_v1,az_v2,dp_v2,az_v3,dp_v3,S1,S2,S3,K_x,K_y,K,C,P,G,R,Vect,confCone,confK = eigen.CalcEigenPlane(dipdir,dip)
        eigenDict = {"az_v1":az_v1,"dp_v1":dp_v1,"az_v2":az_v2,"dp_v2":dp_v2,"az_v3":az_v3,"dp_v3":dp_v3,"S1":S1,"S2":S2,"S3":S3,"K_x":K_x,"K_y":K_y,"K":K,"C":C,"P":P,"G":G,"R":R,"Vect":Vect,"confCone":confCone,"confK":confK}
    else:
        eigenDict = {"az_v1":0,"dp_v1":0,"az_v2":0,"dp_v2":0,"az_v3":0,"dp_v3":0,"S1":0,"S2":0,"S3":0,"K_x":0,"K_y":0,"K":0,"C":0,"P":0,"G":0,"R":0,"Vect":0,"confCone":0,"confK":0}

    return n_data,dipdir,dip,strike,eigenDict


#Open file, linear data
def doLinear(datalist):
    """get linear data"""    

    azimList = [float(val[0]) for val in datalist]
    dipdir = np.array(azimList)
    n_data = len(azimList)

    ncols = len(datalist[0])

    if ncols > 1: # 'normal' file, with two or more columns
        dipList=[float(val[1]) for val in datalist]
        dip1=[dp-0.01 if dp==90 else dp for dp in dipList]
        dip = np.array(dip1)

        strike = [0] # empty list for compatibility with doPlanar()

        if n_data > 3: # must have at least three points for eigen analysis
            az_v1,dp_v1,az_v2,dp_v2,az_v3,dp_v3,S1,S2,S3,K_x,K_y,K,C,P,G,R,Vect,confCone,confK = eigen.CalcEigenLine(dipdir,dip)
            eigenDict = {"az_v1":az_v1,"dp_v1":dp_v1,"az_v2":az_v2,"dp_v2":dp_v2,"az_v3":az_v3,"dp_v3":dp_v3,"S1":S1,"S2":S2,"S3":S3,"K_x":K_x,"K_y":K_y,"K":K,"C":C,"P":P,"G":G,"R":R,"Vect":Vect,"confCone":confCone,"confK":confK}
        else:
            eigenDict = {"az_v1":0,"dp_v1":0,"az_v2":0,"dp_v2":0,"az_v3":0,"dp_v3":0,"S1":0,"S2":0,"S3":0,"K_x":0,"K_y":0,"K":0,"C":0,"P":0,"G":0,"R":0,"Vect":0,"confCone":0,"confK":0}

    else: # file with only one column (usually lineaments)
        dip = np.zeros(n_data)
        strike = [0]
        eigenDict = {"az_v1":0,"dp_v1":0,"az_v2":0,"dp_v2":0,"az_v3":0,"dp_v3":0,"S1":0,"S2":0,"S3":0,"K_x":0,"K_y":0,"K":0,"C":0,"P":0,"G":0,"R":0,"Vect":0,"confCone":0,"confK":0}

    return n_data,dipdir,dip,strike,eigenDict


#Open file, small circle data (az, dip, radius)
def doSmall(datalist):
    """get small circle data"""    

    azimList = [float(val[0]) for val in datalist]
    azim = np.array(azimList)
    n_data = len(azimList)

    dipList=[float(val[1]) for val in datalist]
    dip1=[dp-0.01 if dp==90 else dp for dp in dipList]
    dip = np.array(dip1)

    alphaList=[float(val[2]) for val in datalist]
    alpha = np.array(alphaList)

    return n_data,azim,dip,alpha



#Open file, fault data (dipdir/dip // trend/plunge // sense)
def doFault(datalist):
    """get fault data"""    

    # planes data
    azimList = [float(val[0]) for val in datalist]
    dipdir = np.array(azimList)
    n_data = len(azimList)

    dipList=[float(val[1]) for val in datalist]
    dip1=[dp-0.01 if dp==90 else dp for dp in dipList]
    dip = np.array(dip1)

    strike1=[az+270 if 0<=az<=90 else az-90 for az in azimList]
    strike = np.array(strike1)

    if n_data > 3: # must have at least three points for eigen analysis
        az_v1,dp_v1,az_v2,dp_v2,az_v3,dp_v3,S1,S2,S3,K_x,K_y,K,C,P,G,R,Vect,confCone,confK = eigen.CalcEigenPlane(dipdir,dip)
        eigenDict = {"az_v1":az_v1,"dp_v1":dp_v1,"az_v2":az_v2,"dp_v2":dp_v2,"az_v3":az_v3,"dp_v3":dp_v3,"S1":S1,"S2":S2,"S3":S3,"K_x":K_x,"K_y":K_y,"K":K,"C":C,"P":P,"G":G,"R":R,"Vect":Vect,"confCone":confCone,"confK":confK}
    else:
        eigenDict = {"az_v1":0,"dp_v1":0,"az_v2":0,"dp_v2":0,"az_v3":0,"dp_v3":0,"S1":0,"S2":0,"S3":0,"K_x":0,"K_y":0,"K":0,"C":0,"P":0,"G":0,"R":0,"Vect":0,"confCone":0,"confK":0}

    # slickenside data
    trendList = [float(val[2]) for val in datalist]
    trend = np.array(trendList)

    plungeList=[float(val[3]) for val in datalist]
    plng=[dp-0.01 if dp==90 else dp for dp in plungeList]
    plunge = np.array(plng)

    # sense data
    try:
        senseList = [val[4] for val in datalist]
    except:
        senseList = ['u'] * n_data

    sense = np.array(senseList)
    return n_data,dipdir,dip,strike,eigenDict,trend,plunge,sense




#Open file, PLANES from fault data (dipdir/dip // trend/plunge // sense)
def doFaultPlanar(datalist):
    """get planes from fault data"""    

    azimList = [float(val[0]) for val in datalist]
    dipdir = np.array(azimList)
    n_data = len(azimList)

    dipList=[float(val[1]) for val in datalist]
    dip1=[dp-0.01 if dp==90 else dp for dp in dipList]
    dip = np.array(dip1)

    strike1=[az+270 if 0<=az<=90 else az-90 for az in azimList]
    strike = np.array(strike1)

    if n_data > 3: # must have at least three points for eigen analysis
        az_v1,dp_v1,az_v2,dp_v2,az_v3,dp_v3,S1,S2,S3,K_x,K_y,K,C,P,G,R,Vect,confCone,confK = eigen.CalcEigenPlane(dipdir,dip)
        eigenDict = {"az_v1":az_v1,"dp_v1":dp_v1,"az_v2":az_v2,"dp_v2":dp_v2,"az_v3":az_v3,"dp_v3":dp_v3,"S1":S1,"S2":S2,"S3":S3,"K_x":K_x,"K_y":K_y,"K":K,"C":C,"P":P,"G":G,"R":R,"Vect":Vect,"confCone":confCone,"confK":confK}
    else:
        eigenDict = {"az_v1":0,"dp_v1":0,"az_v2":0,"dp_v2":0,"az_v3":0,"dp_v3":0,"S1":0,"S2":0,"S3":0,"K_x":0,"K_y":0,"K":0,"C":0,"P":0,"G":0,"R":0,"Vect":0,"confCone":0,"confK":0}

    return n_data,dipdir,dip,strike,eigenDict


#Open file, LINES from fault data (dipdir/dip // trend/plunge // sense)
def doFaultLinear(datalist):
    """get linear data"""    

    azimList = [float(val[2]) for val in datalist]
    dipdir = np.array(azimList)
    n_data = len(azimList)

    dipList=[float(val[3]) for val in datalist]
    dip1=[dp-0.01 if dp==90 else dp for dp in dipList]
    dip = np.array(dip1)

    strike = [0] # empty list for compatibility with doPlanar()

    if n_data > 3: # must have at least three points for eigen analysis
        az_v1,dp_v1,az_v2,dp_v2,az_v3,dp_v3,S1,S2,S3,K_x,K_y,K,C,P,G,R,Vect,confCone,confK = eigen.CalcEigenLine(dipdir,dip)
        eigenDict = {"az_v1":az_v1,"dp_v1":dp_v1,"az_v2":az_v2,"dp_v2":dp_v2,"az_v3":az_v3,"dp_v3":dp_v3,"S1":S1,"S2":S2,"S3":S3,"K_x":K_x,"K_y":K_y,"K":K,"C":C,"P":P,"G":G,"R":R,"Vect":Vect,"confCone":confCone,"confK":confK}
    else:
        eigenDict = {"az_v1":0,"dp_v1":0,"az_v2":0,"dp_v2":0,"az_v3":0,"dp_v3":0,"S1":0,"S2":0,"S3":0,"K_x":0,"K_y":0,"K":0,"C":0,"P":0,"G":0,"R":0,"Vect":0,"confCone":0,"confK":0}

    return n_data,dipdir,dip,strike,eigenDict


