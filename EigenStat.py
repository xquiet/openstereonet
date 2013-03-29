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

import numpy.linalg as linalg

import MiscDefs as md

import numpy as np



def CalcEigenPlane(azim,dip):
    """function to calculate eigenvectors and eigenvalues from poles to planes """
    # direction cosines
    # phi = azimuth (dip direction)
    # theta = dip
    # Tmat = orientation matrix T
    # Tmat = sum(xi2)    sum(xi.yi)    sum(xi.zi)
    #        sum(yi.xi)  sum(yi2)      sum(yi.zi)
    #        sum(zi.xi)  sum(zi.yi)    sum(zi2)

    ndata = float(len(azim))

    l,m,n = md.DirCosinePlane(azim,dip)

    l = np.array(l)
    m = np.array(m)
    n = np.array(n)

    Tmat = np.empty((3,3), dtype=float)
    Tmat[0,0] = np.sum(np.power(l,2))
    Tmat[0,1] = np.sum(l * m)
    Tmat[0,2] = np.sum(l * n)
    Tmat[1,0] = np.sum(m * l)
    Tmat[1,1] = np.sum(np.power(m,2))
    Tmat[1,2] = np.sum(m * n)
    Tmat[2,0] = np.sum(n * l)
    Tmat[2,1] = np.sum(n * m)
    Tmat[2,2] = np.sum(np.power(n,2))

#    print Tmat
#    print
#    print Tmat[0,0]+Tmat[1,1]+Tmat[2,2] # this should be about the same as the number of values in the file

    eigen = linalg.eig(Tmat)
    eigenVals = eigen[0]
    eigenVect = eigen[1]

    listv = [0,1,2]
    v1 = np.where(eigenVals==eigenVals.max())[0][0] # maximum value of eingenVals
    listv.remove(v1)
    v3 = np.where(eigenVals==eigenVals.min())[0][0] # minimum value of eingenVals
    listv.remove(v3)
    v2 = listv[0] # intermediate value of eingenVals

    S1 = eigenVals[v1]/len(azim)
    S2 = eigenVals[v2]/len(azim)
    S3 = eigenVals[v3]/len(azim)

    L1 = eigenVect[0,v1]
    M1 = eigenVect[1,v1]
    N1 = eigenVect[2,v1]
#    R1 = np.sqrt(np.power(L1,2)+np.power(N1,2)+np.power(N1,2))

    L2 = eigenVect[0,v2]
    M2 = eigenVect[1,v2]
    N2 = eigenVect[2,v2]
#    R2 = np.sqrt(np.power(L2,2)+np.power(M2,2)+np.power(N2,2))

    L3 = eigenVect[0,v3]
    M3 = eigenVect[1,v3]
    N3 = eigenVect[2,v3]
#    R3 = np.sqrt(np.power(L3,2)+np.power(M3,2)+np.power(N3,2))

    K_x = np.log(S2/S3)
    K_y = np.log(S1/S2)
    K = K_y / K_x

    C = np.log(S1/S3)

    az_v1, dp_v1 = md.CalcSphere(L1,M1,N1)
    az_v2, dp_v2 = md.CalcSphere(L2,M2,N2)
    az_v3, dp_v3 = md.CalcSphere(L3,M3,N3)

#   triangular fabric diagram end points (quick plot)
#   actually, all expressions should be divided by ndata, but 
#   we don't need, since they are normalized already

    P = S1 - S2 # point
    G = 2 * (S2 - S3) # girdle
    R = 3 * S3 # random

# resultant vector 

    T1 = np.sum(l)
    T2 = np.sum(m)
    T3 = np.sum(n)

    Vect = np.sqrt(T1*T1 + T2*T2 + T3*T3)

    N = ndata - Vect

# confidence cone (from QuickPlot)
# original routine is based on Fisher's 1953 paper "Dispersion on a Sphere'
# Royal Society of London, V217, p295-305.

    T4 = T1 / Vect
    T5 = T2 / Vect
    T6 = T3 / Vect

    a = np.power(1.0/0.05, 1.0/(ndata - 1.0))
    confC = 1.0 - N * (a - 1.0) / Vect
    
    confCone = np.degrees(np.arctan2(np.sqrt(1- confC*confC),(confC+0.00000000001)))
    confK = (ndata - 1) / N

    return az_v1, dp_v1, az_v2, dp_v2, az_v3, dp_v3, S1, S2, S3, K_x, K_y, K , C, P, G, R, Vect, confCone, confK    # goes to Data Defs

def CalcEigenLine(azim,dip):
    """function to calculate eigenvectors and eigenvalues from lineations """
    # direction cosines
    # phi = azimuth (dip direction)
    # theta = dip
    # Tmat = orientation matrix T
    # Tmat = sum(xi2)    sum(xi.yi)    sum(xi.zi)
    #        sum(yi.xi)  sum(yi2)      sum(yi.zi)
    #        sum(zi.xi)  sum(zi.yi)    sum(zi2)

    ndata = float(len(azim))

    l,m,n = md.DirCosineLine(azim,dip)

    l = np.array(l)
    m = np.array(m)
    n = np.array(n)

    Tmat = np.empty((3,3), dtype=float)
    Tmat[0,0] = np.sum(np.power(l,2))
    Tmat[0,1] = np.sum(l * m)
    Tmat[0,2] = np.sum(l * n)
    Tmat[1,0] = np.sum(m * l)
    Tmat[1,1] = np.sum(np.power(m,2))
    Tmat[1,2] = np.sum(m * n)
    Tmat[2,0] = np.sum(n * l)
    Tmat[2,1] = np.sum(n * m)
    Tmat[2,2] = np.sum(np.power(n,2))

#    print Tmat
#    print
#    print Tmat[0,0]+Tmat[1,1]+Tmat[2,2] # this should be about the same as the number of values in the file

    eigen = linalg.eig(Tmat)
    eigenVals = eigen[0]
    eigenVect = eigen[1]

    listv = [0,1,2]
    v1 = np.where(eigenVals==eigenVals.max())[0][0] # maximum value of eingenVals
    listv.remove(v1)
    v3 = np.where(eigenVals==eigenVals.min())[0][0] # minimum value of eingenVals
    listv.remove(v3)
    v2 = listv[0] # intermediate value of eingenVals

    S1 = eigenVals[v1]/len(azim)
    S2 = eigenVals[v2]/len(azim)
    S3 = eigenVals[v3]/len(azim)

    L1 = eigenVect[0,v1]
    M1 = eigenVect[1,v1]
    N1 = eigenVect[2,v1]
#    R1 = np.sqrt(np.power(L1,2)+np.power(N1,2)+np.power(N1,2))

    L2 = eigenVect[0,v2]
    M2 = eigenVect[1,v2]
    N2 = eigenVect[2,v2]
#    R2 = np.sqrt(np.power(L2,2)+np.power(M2,2)+np.power(N2,2))

    L3 = eigenVect[0,v3]
    M3 = eigenVect[1,v3]
    N3 = eigenVect[2,v3]
#    R3 = np.sqrt(np.power(L3,2)+np.power(M3,2)+np.power(N3,2))

    K_x = np.log(S2/S3)
    K_y = np.log(S1/S2)
    K = K_y / K_x

    C = np.log(S1/S3)

    az_v1, dp_v1 = md.CalcSphere(L1,M1,N1)
    az_v2, dp_v2 = md.CalcSphere(L2,M2,N2)
    az_v3, dp_v3 = md.CalcSphere(L3,M3,N3)

#   triangular fabric diagram end points (qplot)
#   actually, all expressions should be divided by ndata, but 
#   we don't need, since they are normalized already

    P = S1 - S2 # point
    G = 2 * (S2 - S3) # girdle
    R = 3 * S3 # random

# resultant vector 

    T1 = np.sum(l)
    T2 = np.sum(m)
    T3 = np.sum(n)

    Vect = np.sqrt(T1*T1 + T2*T2 + T3*T3)

    N = ndata - Vect

# confidence cone (from QuickPlot)
# original routine is based on Fisher's 1953 paper "Dispersion on a Sphere'
# Royal Society of London, V217, p295-305.

    T4 = T1 / Vect
    T5 = T2 / Vect
    T6 = T3 / Vect

    a = np.power(1.0/0.05, 1.0/(ndata - 1.0))
    confC = 1.0 - N * (a - 1.0) / Vect
    
    confCone = np.degrees(np.arctan2(np.sqrt(1- confC*confC),(confC+0.00000000001)))
    confK = (ndata - 1) / N

    return az_v1, dp_v1, az_v2, dp_v2, az_v3, dp_v3, S1, S2, S3, K_x, K_y, K , C, P, G, R, Vect, confCone, confK    # goes to Data Defs













