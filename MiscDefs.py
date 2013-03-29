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


import numpy as np


def DirCosinePlane(azim,dip):
    """ direction cosines for poles to planes
        x==East, y==North, z==Up """
    n = len(azim)
    phi_az = np.radians(azim)
    theta = np.radians(dip) 
    l = [np.sin(theta[i]) * np.sin(phi_az[i]) for i in range(n)]
    m = [np.sin(theta[i]) * np.cos(phi_az[i]) for i in range(n)]
    n = [np.cos(theta[i]) for i in range(n)]
    return l,m,n

def DirCosineLine(azim,dip):
    """ direction cosines for lineations
        x==East, y==North, z==Up """
    n = len(azim)
    phi_az = np.radians(azim)
    theta = np.radians(dip) 
    l = [np.cos(theta[i]) * np.sin(phi_az[i]) for i in range(n)]
    m = [np.cos(theta[i]) * np.cos(phi_az[i]) for i in range(n)]
    n = [-np.sin(theta[i]) for i in range(n)]
    return l,m,n


def DirCosineRot(azim,dip):
    """ direction cosines for rotation functions (lineations)
        x==North, y==East, z==Down """
    n = len(azim)
    phi_az = np.radians(azim)
    theta = [np.radians(90.0 - dp) for dp in dip]
    l = [np.sin(theta[i]) * np.sin(phi_az[i]) for i in range(n)]
    m = [np.sin(theta[i]) * np.cos(phi_az[i]) for i in range(n)]
    n = [np.cos(theta[i]) for i in range(n)]
    return l,m,n


def CalcSphere(x,y,z):
    """calculate spherical coordinates from x,y,z (direction cosines) """
#    print x,y,z
    if z >= 0: # vector is pointing UP
        dp = np.degrees(np.arcsin(z))
        x = -x # invert because we want to plot
        y = -y # on the _lower_ hemisfere
    else:
        dp = np.degrees( - np.arcsin(z))
    if x > 0:
        if y > 0: az = np.degrees(np.arctan2(x,y)) # first quadrant
        else: az = np.degrees(np.arctan2(-y,x)) + 90 # second quadrant
    else:
        if y < 0: az = np.degrees(np.arctan2(-x,-y)) + 180 # third quadrant
        else: az = np.degrees(np.arctan2(y,-x)) + 270 # fourth quadrant
    #   particular cases
    if x == 0:
        if y > 0: az = 0 # north
        else: az = 180 # south
    if y == 0:
        if x > 0: az = 90 # east
        else: az = 270 # west
    return az,dp



def CalcSphereLow(x,y,z):
    """calculate spherical coordinates from x,y,z (direction cosines) - always lower hemisphere input"""
    dp = 90.0 - np.degrees(np.arccos(z))
    if x < 0 and y >= 0: 
        az = 450.0 - np.degrees(np.arctan2(y,x)) # fourth quadrant
    else:
        az = 90.0 - np.degrees(np.arctan2(y,x))
    #   particular cases
    if x == 0:
        if y > 0: az = 0 # north
        else: az = 180 # south
    if y == 0:
        if x > 0: az = 90 # east
        else: az = 270 # west
    return az,dp

# following functions from RFOC, used for small circle plotting
def rotx3(deg):
    """ 3x3 Rotation about the X axis -- from RFOC """
    rad1 = np.radians(deg)
    r = np.eye(3)
    r[1, 1] = np.cos(rad1)
    r[1, 2] = np.sin(rad1)
    r[2, 2] = r[1, 1]
    r[2, 1] = -r[1, 2]
    return np.mat(r)

def roty3(deg):
    """ 3x3 Rotation about the Y axis -- from RFOC """
    rad1 = np.radians(deg)
    r = np.eye(3)
    r[0, 0] = np.cos(rad1)
    r[2, 0] = np.sin(rad1)
    r[2, 2] = r[0, 0]
    r[0, 2] = -r[2, 0]
    return np.mat(r)

def rotz3(deg):
    """ 3x3 Rotation about the Z axis -- from RFOC """
    rad1 = np.radians(deg)
    r = np.eye(3)
    r[0, 0] = np.cos(rad1)
    r[0, 1] = np.sin(rad1)
    r[1, 1] = r[0, 0]
    r[1, 0] = -r[0, 1]
    return np.mat(r)

def fmod(k, m):
    """ extract remainder for floating point numbers -- from RFOC """
    j = np.floor(k/m)
    a = k-m*j
    return a

def FixDip(az,dip):
    """ fix quadrant of azimuth/dip -- from RFOC """
    tdip = [np.radians(fmod(i,360.0)) for i in dip]
    co = np.cos(tdip)
    si = np.sin(tdip)
    ang = np.degrees(np.arctan2(si,co))
    quad = [1] * len(dip)
    for i in range(len(dip)):
        if co[i] >= 0 and si[i] >= 0: quad[i] = 1
        elif co[i] < 0 and si[i] >= 0: quad[i] = 2
        elif co[i] < 0 and si[i] < 0: quad[i] = 3
        elif co[i] >= 0 and si[i] < 0: quad[i] = 4
    for i in range(len(dip)):
        if quad[i] == 1: dip[i] = ang[i]
        elif quad[i] == 2: dip[i] = 180.0 - ang[i]
        elif quad[i] == 3: dip[i] = 180.0 + ang[i]
        elif quad[i] == 4: dip[i] = - ang[i]
    for i in range(len(dip)):
        if quad[i] == 1: az[i] = az[i]
        elif quad[i] == 2: az[i] = 180.0 + az[i]
        elif quad[i] == 3: az[i] = az[i]
        elif quad[i] == 4: az[i] = 180.0 + az[i]
    azz = fmod(az, 360.0)
    dipp = dip
    return azz, dip

def takeoff(az,ang):
    """ Plot a set of (azimuth, takeoff) angle on a stereonet -- from RFOC """
#  az = angle from north (degrees)
#  ang = angle from Z-down (from nadir, not from horizontal)
    azf, angf = FixDip(az,ang)
    trot = np.radians(azf)
    tdip = np.radians(angf)
    tq = np.sqrt(2) * np.sin(tdip / 2.0)
    px = tq * np.sin(trot)
    py = tq * np.cos(trot)
    return px, py

def takeoff2(az,ang):
    """ to be used to plot the entire small circle, that is, including the parts outside the stereonet """
#  this function will NOT call FixDip
    trot = np.radians(az)
    tdip = np.radians(ang)
    tq = np.sqrt(2) * np.sin(tdip / 2.0)
    px = tq * np.sin(trot)
    py = tq * np.cos(trot)
    return px, py



