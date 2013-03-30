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

from wx.lib.pubsub import Publisher as pub

#import matplotlib
#import matplotlib
#matplotlib.use('WXAgg')

from matplotlib.figure import Figure
from matplotlib.collections import LineCollection
from mpl_toolkits.axes_grid.axislines import Subplot
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg
from matplotlib.font_manager import fontManager, FontProperties

from mpl_toolkits.axes_grid import make_axes_locatable
import  matplotlib.axes as maxes

from matplotlib.patches import Wedge
from matplotlib.patches import Circle
from matplotlib.patches import Arc
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon
from matplotlib.patches import FancyArrowPatch
from matplotlib.patches import FancyArrow
from matplotlib.lines import Line2D
from matplotlib.text import Text

import numpy as np

import ContourDefs as cont
import PlotDefs as pd

# import i18n
import i18n
_ = i18n.language.ugettext #use ugettext instead of getttext to avoid unicode errors

#custom matplotlib navigation toolbar
#from: http://www.nabble.com/Re%3A-Navigation-toolbar-w-o-subplot-configuration-button-p18754379.html
class VMToolbar(NavigationToolbar2WxAgg):

    def __init__(self, plotCanvas):
        NavigationToolbar2WxAgg.__init__(self, plotCanvas)
        
#        self.SetToolBitmapSize(wx.Size(10,10))
        # delete unwanted tools
        self.DeleteToolByPos(6) # Configure subplots
#        self.DeleteToolByPos(3) # Pan

        self.Realize()

class StereoPanel(wx.Panel):
    """class for the second page of the notebook """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.BORDER_SUNKEN)

        self.mainframe = wx.GetTopLevelParent(self)

# default variables
        self.fontSize = 'x-small'

#initialize the figure and canvas
#        self.dpi = 100
        self.stereoFigure = Figure(figsize=(4,4),facecolor='white')#, dpi=self.dpi)
        self.stereoCanvas = FigureCanvas(self, -1, self.stereoFigure)
        self.toolbar = VMToolbar(self.stereoCanvas)
        self.stereoCanvas.mpl_connect("motion_notify_event", self.OnMove)

#initialize the plot area
        self.plotaxes = self.stereoFigure.add_axes([0.01, 0.01, 0.6, 0.98], clip_on='True',xlim=(-1.1,1.2), ylim=(-1.15,1.15), adjustable='box',autoscale_on='False',label='stereo')
        self.plotaxes.set_axis_off()
        self.plotaxes.set_aspect(aspect='equal', adjustable=None, anchor='W')

#axes for colorbar
        self.caxes = self.stereoFigure.add_axes([0.603, 0.09, 0.025, 0.38],anchor='SW')
        self.caxes.set_axis_off()

# create draw/clear buttons 
        self.clearNet_Button = wx.Button(self, -1, _('Clear'), size=(60, 30))
        self.plotNet_Button = wx.Button(self, -1, _('Plot'), size=(60, 30))

        hboxTB = wx.BoxSizer(wx.HORIZONTAL)
        hboxTB.Add(self.plotNet_Button,0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,3)
        hboxTB.Add(self.clearNet_Button,0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,3)
        hboxTB.Add(self.toolbar, 1, wx.EXPAND|wx.ALL, 1)

        self.Bind(wx.EVT_BUTTON, self.PlotStereonett, self.clearNet_Button)
        self.Bind(wx.EVT_BUTTON, self.PlotChecked, self.plotNet_Button)

#layout of canvas
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(self.stereoCanvas, 1, wx.EXPAND)
        vbox2.Add(hboxTB,0, wx.EXPAND|wx.ALL, 1)
#        vbox2.Add(self.toolbar, 0, wx.EXPAND|wx.ALL, 1)
        self.SetSizer(vbox2)

#retrieve data from pubsub
        pub.subscribe(self.__onReceivePlanarData, 'object.Plan_added_DDD') # from MainForm
        pub.subscribe(self.__onReceivePlanarData, 'object.Plan_added_RH') # from MainForm
        pub.subscribe(self.__onReceiveLinearData, 'object.Lin_added') # from MainForm
        pub.subscribe(self.__onReceiveSmallData, 'object.Sc_added') # from MainForm
        pub.subscribe(self.__onReceiveFaultData, 'object.Fault_added') # from MainForm
        pub.subscribe(self.__onReceiveFontSize, 'object.FontSize') # from MainForm

        pub.subscribe(self.__onReceiveSelection, 'object.selected') # from TreePanel
        pub.subscribe(self.__onReceiveChecked, 'object.checked') # from TreePanel (namesList)
        pub.subscribe(self.__onReceivePropsPlan, 'object.PropsPlanReceiv') # from TreePanel, OnProps_childPlanar
        pub.subscribe(self.__onReceivePropsLin, 'object.PropsLinReceiv')# from TreePanel, OnProps_childLinear
        pub.subscribe(self.__onReceivePropsSc, 'object.PropsScReceiv')# from TreePanel, OnProps_childSmall
        pub.subscribe(self.__onReceivePropsF, 'object.PropsFReceiv')# from TreePanel, OnProps_childSmall
        pub.subscribe(self.__onReceiveAxes, 'object.axes_added') # from MainForm
        pub.subscribe(self.__onReceiveGrid, 'object.grid') # from TreePanel
        pub.subscribe(self.__onReceiveItemDel, 'object.ItemDelete') # from TreePanel
        pub.subscribe(self.__onReceiveContour, 'object.contour') # from ContourDefs


# font size
    def __onReceiveFontSize(self, message):
        self.fontSize = message.data

# status of contouring, to avoid re-calculations
    def __onReceiveContour(self, message):
        self.ContourStatus = message.data

# When an item is deleted from the Tree
    def __onReceiveItemDel(self, message):
        if self.checkedList: # there are other opened files
            self.PlotStereonett(message)
            self.PlotChecked(message)
        else: # no more files in tree
            self.PlotStereonett(message)

# stereonet grid interval and type (Schmidt/Wulff)
    def __onReceiveGrid(self, message):
        self.gridstep = message.data[0] # floatSpin
        self.gridtype = message.data[1] # Schimdt or Wulff (combobox)
#        print self.gridtype

# plot stereonet when program starts
    def __onReceiveAxes(self, message): 
        try:
            self.stereogrid = 0
            self.gridtype = 'schmidt'
            self.gridstep = 10
            self.PlotStereonett(wx.EVT_SHOW)
        except wx.PyDeadObjectError:
            pass

# which file is selected
    def __onReceiveSelection(self, message): 
        self.file_i = message.data


# planar data file(s) opened
    def __onReceivePlanarData(self, message): 

        try:
            len(self.Pname) # dummy action just to see if self.Pname exists
        except:
            self.Ptype=[]
            self.Pname=[]
            self.Pndata=[]
            self.Pazim=[]
            self.Pdip=[]
            self.Pstrike=[]
            self.PeigenDict=[]
            self.PidxList=[]
            self.PProps=[]

        for i in range(len(message.data)):
            self.Ptype.append(message.data[i][0])       # filetype
#            self.Pname.append(message.data[i][1])       # filename
            self.Pndata.append(message.data[i][2])      # n_data
            self.Pazim.append(message.data[i][3])       # dipdir
            self.Pdip.append(message.data[i][4])        # dip
            self.Pstrike.append(message.data[i][5])     # strike
            self.PeigenDict.append(message.data[i][6])  # eigenList
            self.PidxList.append(message.data[i][7])    # DDD_idx
            self.PProps.append(message.data[i][8])      # pplist - default properties set in MainForm.py  

            if message.data[i][7].startswith('D'): # dip-dir data
                self.Pname.append('[P(dd)] %s' % message.data[i][1])
            else: # right-hand data
                self.Pname.append('[P(rh)] %s' % message.data[i][1])

        for i in range(len(self.PProps)):
            self.PProps[i]["itemName"] = self.Pname[i] 

#            self.az_v1 = eigenList[0]
#            self.dp_v1 = eigenList[1]
#            self.az_v2 = eigenList[2]
#            self.dp_v2 = eigenList[3]
#            self.az_v3 = eigenList[4]
#            self.dp_v3 = eigenList[5]
#            self.S1 = eigenList[6]
#            self.S2 = eigenList[7]
#            self.S3 = eigenList[8]
#            self.K_x = eigenList[9]
#            self.K_y = eigenList[10]
#            self.K = eigenList[11]
#            self.C = eigenList[12]
#            self.P = eigenList[13]
#            self.G = eigenList[14]
#            self.R = eigenList[15]

# linear data file(s) opened
    def __onReceiveLinearData(self, message): 

        try:
            len(self.Lname) # dummy action just to see if self.Lname exists
        except:
            self.Ltype=[]
            self.Lname=[]
            self.Lndata=[]
            self.Lazim=[]
            self.Ldip=[]
            self.Lstrike=[]
            self.LeigenDict=[]
            self.LidxList=[]
            self.LProps=[]

        for i in range(len(message.data)):
            self.Ltype.append(message.data[i][0])       # filetype
            self.Lname.append(message.data[i][1])       # filename
            self.Lndata.append(message.data[i][2])      # n_data
            self.Lazim.append(message.data[i][3])       # dipdir
            self.Ldip.append(message.data[i][4])        # dip
            self.Lstrike.append(message.data[i][5])     # strike
            self.LeigenDict.append(message.data[i][6])  # eigenList
            self.LidxList.append(message.data[i][7])    # Lin_idx
            self.LProps.append(message.data[i][8])      # lplist - default properties set in MainForm.py

        for i in range(len(self.LProps)):
            self.LProps[i]["itemName"] = self.Lname[i] 


# fault data file(s) opened
    def __onReceiveFaultData(self, message): 

        try:
            len(self.Fname) # dummy action just to see if self.Lname exists
        except:
            self.Ftype=[]
            self.Fname=[]
            self.Fndata=[]
            self.Fazim=[]
            self.Fdip=[]
            self.Fstrike=[]
            self.FeigenList=[]
            self.Ftrend=[]
            self.Fplunge=[]
            self.Fsense=[]
            self.FidxList=[]
            self.FProps=[]

        for i in range(len(message.data)):
            self.Ftype.append(message.data[i][0])       # filetype
            self.Fname.append(message.data[i][1])       # filename
            self.Fndata.append(message.data[i][2])      # n_data
            self.Fazim.append(message.data[i][3])       # dipdir
            self.Fdip.append(message.data[i][4])        # dip
            self.Fstrike.append(message.data[i][5])     # strike
            self.FeigenList.append(message.data[i][6])  # eigenList
            self.Ftrend.append(message.data[i][7])      # trend
            self.Fplunge.append(message.data[i][8])     # plunge
            self.Fsense.append(message.data[i][9])      # sense
            self.FidxList.append(message.data[i][10])   # F_idx
            self.FProps.append(message.data[i][11])     # fplist - default properties set in MainForm.py

#                    self.faultData.append([filetype,filename,n_data,dipdir,dip,strike,eigenList,trend,plunge,sense,F_idx,self.fplist])

        for i in range(len(self.FProps)):
            self.FProps[i]["itemName"] = self.Fname[i] 


# small circle data file(s) opened
    def __onReceiveSmallData(self, message): 

        try:
            len(self.Scname) # dummy action just to see if self.Scname exists
        except:
            self.Sctype=[]
            self.Scname=[]
            self.Scndata=[]
            self.Scazim=[]
            self.Scdip=[]
            self.Scalpha=[]
            self.ScidxList=[]
            self.ScProps=[]

        for i in range(len(message.data)):
            self.Sctype.append(message.data[i][0])       # filetype
            self.Scname.append(message.data[i][1])       # filename
            self.Scndata.append(message.data[i][2])      # n_data
            self.Scazim.append(message.data[i][3])       # azim
            self.Scdip.append(message.data[i][4])        # dip
            self.Scalpha.append(message.data[i][5])     # alpha (radius)
            self.ScidxList.append(message.data[i][6])    # Sc_idx
            self.ScProps.append(message.data[i][7])      # scplist - default properties set in MainForm.py

        for i in range(len(self.ScProps)):
#            self.ScProps[i][1] = self.Scname[i] #
            self.ScProps[i]["itemName"] = self.Scname[i] # default properties set in MainForm.py


# which files are checked to plot
    def __onReceiveChecked(self, message): 
        self.checkedList = message.data
#        print checkedList
        self.idxPlan = []
        self.idxLin = []
        self.idxSmall = []
        self.idxFault = []

        self.p_polesList = [] # list of the files selected to be ploted as poles to planes
        self.p_girdList = [] # to be ploted as girdles (to planes)
        self.p_gcList = [] # to be ploted as great circles
        self.p_contList = [] # to be ploted as contours (of planes)

        self.l_polesList = [] # list of the files selected to be ploted as poles to lines
        self.l_girdList = [] # to be ploted as girdles (to lines)
        self.l_contList = [] # to be ploted as contours (of lines)

        self.f_circList = [] # list of fault planes to be ploted as great circles
        self.f_slickenList = [] # list of fault slickensides to be ploted as dots or arrows
        self.f_hoeppenerList = [] # list of fault slickensides to be ploted as displacement vectors (Hoeppener plot)

        self.sc_list = [] # list of the files selected to be ploted as small circles

        self.stereogrid = 0 # don't plot grid by default

        for checked in self.checkedList:

            if checked[1] == 0 and checked[0] == 'grid': # checked[1] = 0: stereo net grid
                self.stereogrid = 1

            elif checked[1] == 1 and checked[0] in self.PidxList: # checked[1] = 1: planar data
                self.idxPlan.append(self.PidxList.index(checked[0]))
                for val in checked:
                    if val == 10: # poles to planes
                        self.p_polesList.append(self.PidxList.index(checked[0]))
                    if val == 11: # eigenvectors
                        self.p_girdList.append(self.PidxList.index(checked[0])) 
                    if val == 12: # great circles
                        self.p_gcList.append(self.PidxList.index(checked[0]))
                    if val == 13: # contours
                        self.p_contList.append(self.PidxList.index(checked[0]))

            elif checked[1] == 2 and checked[0] in self.LidxList: # checked[1] = 2: linear data
                self.idxLin.append(self.LidxList.index(checked[0]))
                for val in checked:
                    if val == 10: # poles to lines
                        self.l_polesList.append(self.LidxList.index(checked[0]))
                    if val == 11: # eigenvectors
                        self.l_girdList.append(self.LidxList.index(checked[0]))
                    if val == 12: # contours
                        self.l_contList.append(self.LidxList.index(checked[0]))

            elif checked[1] == 3 and checked[0] in self.ScidxList: # checked[1] = 3: small circle data
                self.idxSmall.append(self.ScidxList.index(checked[0]))
                self.sc_list.append(self.ScidxList.index(checked[0]))

            elif checked[1] == 4 and checked[0] in self.FidxList: # checked[1] = 4: fault data
                self.idxFault.append(self.FidxList.index(checked[0]))
                for val in checked:
                    if val == 10: # great circles
                        self.f_circList.append(self.FidxList.index(checked[0]))
                    if val == 11: # slickensides
                        self.f_slickenList.append(self.FidxList.index(checked[0]))
                    if val == 12: # displacement
                        self.f_hoeppenerList.append(self.FidxList.index(checked[0]))




 # graphic properties of planar data
    def __onReceivePropsPlan(self, message): # object.PropsPlanRec
        PropsPlan = message.data
#        print PropsPlan
        idx = self.PidxList.index(PropsPlan["pdata"])
        self.PProps[idx] = PropsPlan # replace default props by user-defined ones
        pub.sendMessage('object.PProps', self.PProps) # send back to TreePanel

#            propsPList = {"pdata":pdata[1], "itemName":itemName, \
#                "PolColor":PolColor, "PoleSymb":symbPoles, "polespin":polespin, \
#                "CircColor":CircColor, "CircSty":styleCirc, "circspin":circspin, \
#                "cb_eigen_gc1":cb_eigen_gc1, "CircGirdColor1":CircGirdColor1, "styleGirdCirc1":styleGirdCirc1, "circGirdspin1":circGirdspin1, \
#                "cb_eigen_p1":cb_eigen_p1, "PolGirdColor1":PolGirdColor1, "symbGirdPoles1":symbGirdPoles1, "poleGirdspin1":poleGirdspin1, \
#                "cb_eigen_gc2":cb_eigen_gc2, "CircGirdColor2":CircGirdColor2, "styleGirdCirc2":styleGirdCirc2, "circGirdspin2":circGirdspin2, \
#                "cb_eigen_p2":cb_eigen_p2, "PolGirdColor2":PolGirdColor2, "symbGirdPoles2":symbGirdPoles2, "poleGirdspin2":poleGirdspin2, \
#                "cb_eigen_gc3":cb_eigen_gc3, "CircGirdColor3":CircGirdColor3, "styleGirdCirc3":styleGirdCirc3, "circGirdspin3":circGirdspin3, \
#                "cb_eigen_p3":cb_eigen_p3, "PolGirdColor3":PolGirdColor3, "symbGirdPoles3":symbGirdPoles3, "poleGirdspin3":poleGirdspin3, \
#                "count_nodes":cntNodes, "percent":percent, "interpolation":interpol, "gridSpin":gridSpin, "epsilon":epsilSpin, \
#                "smoothing":smootSpin, "contStyle":contStyle, "contColor":contColor, "contFill":contFill, "contLws":contLws, "colormap":colormap, \
#                "contcolormap":contcolormap, "addedges":addedges, "rbsc":rbsc, "rbcm":rbcm, "antiAliased":antial, "minmax":minmax, "zeromax":zeromax, \
#                "numcontours":numcontours, "custom":custom, "customcont":customcont, "rbcossum":rbcossum, "expSpin":expSpin, "rbfisher":rbfisher, \
#                "kSpin":kSpin, "rbscarea":rbscarea, "areaSpin":areaSpin, "rbscangle":rbscangle, "angleSpin":angleSpin}




# graphic properties of linear data
    def __onReceivePropsLin(self, message): # object.PropsLinRec
        PropsLin = message.data
        idx = self.LidxList.index(PropsLin["pdata"])
        self.LProps[idx] = PropsLin # replace default props by user-defined ones
        pub.sendMessage('object.LProps', self.LProps) # send back to TreePanel

#            propsLList = {"pdata":pdata[1], "itemName":itemName, \
#                    "LinColor":LinColor, "LineSymb":LineSymb, "linespin":linespin,\
#                    "cb_eigen_gc1":cb_eigen_gc1, "CircGirdColor1":CircGirdColor1, "styleGirdCirc1":styleGirdCirc1, "circGirdspin1":circGirdspin1, \
#                    "cb_eigen_p1":cb_eigen_p1, "PolGirdColor1":PolGirdColor1, "symbGirdPoles1":symbGirdPoles1, "poleGirdspin1":poleGirdspin1, \
#                    "cb_eigen_gc2":cb_eigen_gc2, "CircGirdColor2":CircGirdColor2, "styleGirdCirc2":styleGirdCirc2, "circGirdspin2":circGirdspin2, \
#                    "cb_eigen_p2":cb_eigen_p2, "PolGirdColor2":PolGirdColor2, "symbGirdPoles2":symbGirdPoles2, "poleGirdspin2":poleGirdspin2, \
#                    "cb_eigen_gc3":cb_eigen_gc3, "CircGirdColor3":CircGirdColor3, "styleGirdCirc3":styleGirdCirc3, "circGirdspin3":circGirdspin3, \
#                    "cb_eigen_p3":cb_eigen_p3, "PolGirdColor3":PolGirdColor3, "symbGirdPoles3":symbGirdPoles3, "poleGirdspin3":poleGirdspin3, \
#                    "count_nodes":cntNodes, "percent":percent, "interpolation":interpol, "gridSpin":gridSpin, "epsilon":epsilSpin, \
#                    "smoothing":smootSpin, "contStyle":contStyle, "contColor":contColor, "contFill":contFill, "contLws":contLws, "colormap":colormap, \
#                    "contcolormap":contcolormap, "addedges":addedges, "rbsc":rbsc, "rbcm":rbcm, "antiAliased":antial, "minmax":minmax, "zeromax":zeromax, \
#                    "numcontours":numcontours, "custom":custom, "customcont":customcont, "rbcossum":rbcossum, "expSpin":expSpin, "rbfisher":rbfisher, \
#                    "kSpin":kSpin, "rbscarea":rbscarea, "areaSpin":areaSpin, "rbscangle":rbscangle, "angleSpin":angleSpin}

# graphic properties of small circle data
    def __onReceivePropsSc(self, message): 
        PropsSc = message.data
        idx = self.ScidxList.index(PropsSc["pdata"])
        self.ScProps[idx] = PropsSc # replace default props by user-defined ones
        pub.sendMessage('object.ScProps', self.ScProps) # send back to TreePanel

#       propsScList = {"pdata":pdata[1],"itemName":itemName,"ScColor":ScColor,"ScSty":ScSty,"ScSpin":ScSpin, "ScFull":ScFull}





# graphic properties of fault data
    def __onReceivePropsF(self, message): 
        PropsF = message.data
        idx = self.FidxList.index(PropsF["pdata"])
        self.FProps[idx] = PropsF # replace default props by user-defined ones
        pub.sendMessage('object.FProps', self.FProps) # send back to TreePanel

#        propsFList = {"pdata":pdata[1],"itemName":itemName, \
#            "FaultCircColor":FaultCircColor, "FaultCircSty":FaultCircSty, "FaultCircSpin":FaultCircSpin, \
#            "SlickPlotPoles":SlickPlotPoles, "SlickPoleColor":SlickPoleColor, "SlickPoleSymb":SlickPoleSymb, "SlickPoleSpin":SlickPoleSpin, \
#            "SlickArrowSpin":SlickArrowSpin, "SlickArrowColor":SlickArrowColor, "SlickArrowWidthSpin":SlickArrowWidthSpin, \
#            "DisplacePlotPoles":DisplacePlotPoles, "DisplacePoleColor":DisplacePoleColor, "DisplacePoleSymb":DisplacePoleSpin, "DisplacePoleSpin":DisplacePoleSpin}                    


#get coordinates of plot and show in statusbar
    def OnMove(self, event):
        np.seterr(all='ignore')
        if event.inaxes:
            x, y = event.xdata, event.ydata
            sqrt2 = np.sqrt(2)
            az = np.degrees(np.arctan2(y,x))
            if 0.0 <= az < 90.0:
                az = -(az - 90.0)
            elif 90.0 <= az <= 180.0:
                az = 540.0 + (-az - 90.0)
            else:
                az = -az + 90.0
            dr = np.sqrt(x*x + y*y) 

            if self.gridtype == 'schmidt':
                dp = 2 * (np.arcsin(dr/sqrt2))
                dip = - (np.degrees(dp) - 90.0)
            elif self.gridtype == 'wulff':
                dp = 2 * (np.arctan(dr))
                dip = 90.0 - np.degrees(dp)

            if dip >= 0:
                self.mainframe.sb.SetStatusText('Dip direction: %3.1f' % az + ', Dip: %2.1f' % dip)
            else:
                self.mainframe.sb.SetStatusText('')



#creates / redraws the stereonet
    def PlotStereonett(self, event): 
        """Create the Stereonet """

        axes = self.plotaxes
        caxes = self.caxes
        fontsize = self.fontSize
        PlotStereoNetCircle(axes, caxes, fontsize)

        if self.stereogrid == 1:
            if self.gridtype == 'schmidt':
                PlotStereoNetGridSchmidt(axes,self.gridstep)
            elif self.gridtype == 'wulff':
                PlotStereoNetGridWulff(axes,self.gridstep)

        if self.gridtype == 'schmidt':
            axes.text(-0.95,-1.08,'Equal-area\nLower hemisphere',family='sans-serif',size=fontsize, horizontalalignment='left')
        elif self.gridtype == 'wulff':
            axes.text(-0.95,-1.08,'Equal-angle\nLower hemisphere',family='sans-serif',size=fontsize, horizontalalignment='left')

        axes.set_xlim(-1.1,1.2)
        axes.set_ylim(-1.15,1.15)
        self.stereoCanvas.draw()
    
        self.mainframe.sb.SetStatusText('New stereonet created')

# plot everything that is checked
    def PlotChecked(self, event): 
        """ Plot everything that is checked in stereonet """
        axes = self.plotaxes
        caxes = self.caxes

        legendEntries=[]  # list of plots that are going to be in the legend
        legendText=[]   # list of text messages for the legend

#        try:

        #refresh stereonet circle
        PlotStereoNetCircle(axes, caxes, self.fontSize)

        #plot grid
        if self.stereogrid == 1:
            if self.gridtype == 'schmidt':
                PlotStereoNetGridSchmidt(axes,self.gridstep)
            elif self.gridtype == 'wulff':
                PlotStereoNetGridWulff(axes,self.gridstep)

        # plot fault data -- great circles
        for i in self.f_circList:
            linwidth = self.FProps[i]["FaultCircSpin"]
            CircSty = self.FProps[i]["FaultCircSty"]
            CircColor = self.FProps[i]["FaultCircColor"]
            col = PlotGreatCircle(self.gridtype,axes,self.Fazim[i],self.Fstrike[i],self.Fdip[i],CircColor,CircSty,linwidth)
            legendEntries.append(col) 
            legendText.append('[F] %s (great circle) n=%d' % (self.Fname[i],self.Fndata[i]))


        # plot fault data -- slickensides
        for i in self.f_slickenList:
            SlickArrowSize = self.FProps[i]["SlickArrowSpin"]
            SlickArrowColor = self.FProps[i]["SlickArrowColor"]
            SlickArrowWidth = self.FProps[i]["SlickArrowWidthSpin"]
            SlickPlotPoles = self.FProps[i]["SlickPlotPoles"]
            SlickPoleSize = self.FProps[i]["SlickPoleSpin"]
            SlickPoleSymb = self.FProps[i]["SlickPoleSymb"]
            SlickPoleColor = self.FProps[i]["SlickPoleColor"]
            col = PlotSlickensides(self.gridtype,False,axes,self.Fazim[i],self.Fdip[i],self.Ftrend[i],self.Fplunge[i],self.Fsense[i], SlickArrowSize,SlickArrowColor,SlickArrowWidth,SlickPlotPoles,SlickPoleSize,SlickPoleSymb,SlickPoleColor,False)
            legendEntries.append(col) 
            legendText.append('[F] %s (slickensides) n=%d' % (self.Fname[i],self.Fndata[i]))


        # plot fault data -- slip-linear (Hoeppener plot)
        for i in self.f_hoeppenerList:
            DisplaceArrowSize = self.FProps[i]["DisplaceArrowSpin"]
            DisplaceArrowColor = self.FProps[i]["DisplaceArrowColor"]
            DisplaceArrowWidth = self.FProps[i]["DisplaceArrowWidthSpin"]
            DisplacePlotPoles = self.FProps[i]["DisplacePlotPoles"]
            DisplacePoleSize = self.FProps[i]["DisplacePoleSpin"]
            DisplacePoleSymb = self.FProps[i]["DisplacePoleSymb"]
            DisplacePoleColor = self.FProps[i]["DisplacePoleColor"]
            footwall = self.FProps[i]["footwall"]
            col1 = PlotSlickensides(self.gridtype,True,axes,self.Fazim[i],self.Fdip[i],self.Ftrend[i],self.Fplunge[i],self.Fsense[i], DisplaceArrowSize,DisplaceArrowColor,DisplaceArrowWidth,DisplacePlotPoles,DisplacePoleSize,DisplacePoleSymb,DisplacePoleColor,footwall)
            legendEntries.append(col1) 
            legendText.append('[F] %s (slip-linear) n=%d' % (self.Fname[i],self.Fndata[i]))


        #plot contours of planar data
        for i in self.p_contList:

            try:
                len(self.ContourStatus) # dummy action just to see if self.ContourStatus exists
            except:
                self.ContourStatus = ['dummy', 0, 0, 0, [1], [1], [1], [1]]

            nodes = self.PProps[i]["count_nodes"]
            percent = self.PProps[i]["percent"]
            interp = self.PProps[i]["interpolation"]
            grid = self.PProps[i]["gridSpin"]
#                epsilon = self.PProps[i]["epsilon"]
#                smoothing = self.PProps[i]["smoothing"]
            cstyle = self.PProps[i]["contStyle"]
            ccol = self.PProps[i]["contColor"]
            cfill = self.PProps[i]["contFill"]
            cedges = self.PProps[i]["addedges"]
            clwd = self.PProps[i]["contLws"]
            ccmap = self.PProps[i]["colormap"] 
            contccmap = self.PProps[i]["contcolormap"] 
            rbsc = self.PProps[i]["rbsc"] # single color
            cedges = self.PProps[i]["addedges"]
            antial = self.PProps[i]["antiAliased"]
            minmax = self.PProps[i]["minmax"]
            zeromax = self.PProps[i]["zeromax"]
            ncont = self.PProps[i]["numcontours"]
            custom = self.PProps[i]["custom"]
            customList = self.PProps[i]["customcont"]
            rbcossum = self.PProps[i]["rbcossum"]
            expSpin = self.PProps[i]["expSpin"]
            rbfisher = self.PProps[i]["rbfisher"]
            kSpin = self.PProps[i]["kSpin"]
            rbscarea = self.PProps[i]["rbscarea"]
            areaSpin = self.PProps[i]["areaSpin"]
            rbscangle = self.PProps[i]["rbscangle"]
            angleSpin = self.PProps[i]["angleSpin"]

            caxes.set_axis_on()
            cont.PlotContourSchmidt(self.gridtype, axes, caxes, self.Pazim[i], self.Pdip[i], 1, nodes, percent, interp, grid, cstyle, ccol, cfill, clwd, ccmap, contccmap, rbsc, cedges, antial, minmax, zeromax, ncont, custom, customList, rbcossum, expSpin, rbfisher, kSpin, rbscarea, areaSpin, rbscangle, angleSpin, '[Density] %s, n=%d' % (self.Pname[i],self.Pndata[i]), self.ContourStatus, self.Pname[i], self.fontSize)   # 1: planar data
#epsilon, smoothing, 

        #plot contours of linear data
        for i in self.l_contList:

            try:
                len(self.ContourStatus) # dummy action just to see if self.ContourStatus exists
            except:
                self.ContourStatus = ['dummy', 0, 0, 0, [1], [1], [1], [1]]

            nodes = self.LProps[i]["count_nodes"]
            percent = self.LProps[i]["percent"]
            interp = self.LProps[i]["interpolation"]
            grid = self.LProps[i]["gridSpin"]
#                epsilon = self.LProps[i]["epsilon"]
#                smoothing = self.LProps[i]["smoothing"]
            cstyle = self.LProps[i]["contStyle"]
            ccol = self.LProps[i]["contColor"]
            cfill = self.LProps[i]["contFill"]
            cedges = self.LProps[i]["addedges"]
            clwd = self.LProps[i]["contLws"]
            ccmap = self.LProps[i]["colormap"] 
            contccmap = self.LProps[i]["contcolormap"] 
            rbsc = self.LProps[i]["rbsc"] # single color
            cedges = self.LProps[i]["addedges"]
            antial = self.LProps[i]["antiAliased"]
            minmax = self.LProps[i]["minmax"]
            zeromax = self.LProps[i]["zeromax"]
            ncont = self.LProps[i]["numcontours"]
            custom = self.LProps[i]["custom"]
            customList = self.LProps[i]["customcont"]
            rbcossum = self.LProps[i]["rbcossum"]
            expSpin = self.LProps[i]["expSpin"]
            rbfisher = self.LProps[i]["rbfisher"]
            kSpin = self.LProps[i]["kSpin"]
            rbscarea = self.LProps[i]["rbscarea"]
            areaSpin = self.LProps[i]["areaSpin"]
            rbscangle = self.LProps[i]["rbscangle"]
            angleSpin = self.LProps[i]["angleSpin"]

            caxes.set_axis_on()
            cont.PlotContourSchmidt(self.gridtype, axes, caxes, self.Lazim[i], self.Ldip[i], 2, nodes, percent, interp, grid, cstyle, ccol, cfill, clwd, ccmap, contccmap, rbsc, cedges, antial, minmax, zeromax, ncont, custom, customList, rbcossum, expSpin, rbfisher, kSpin, rbscarea, areaSpin, rbscangle, angleSpin, '[Density] %s, n=%d' % (self.Lname[i],self.Lndata[i]), self.ContourStatus, self.Lname[i], self.fontSize)   # 2: linear data
#epsilon, smoothing, 

        #plot great circles of planes
        for i in self.p_gcList:
            linwidth = self.PProps[i]["circspin"]
            CircSty = self.PProps[i]["CircSty"]
            CircColor = self.PProps[i]["CircColor"]
            col = PlotGreatCircle(self.gridtype,axes,self.Pazim[i],self.Pstrike[i],self.Pdip[i],CircColor,CircSty,linwidth)
            legendEntries.append(col) 
            legendText.append(' %s (great circle) n=%d' % (self.Pname[i],self.Pndata[i]))


        #plot poles to planes
        for i in self.p_polesList:
            Ppolesize = self.PProps[i]["polespin"]
            PoleSymb = self.PProps[i]["PoleSymb"]
            PolColor = self.PProps[i]["PolColor"]
            plot = PlotPolesPlanes(self.gridtype,axes,self.Pazim[i],self.Pdip[i],Ppolesize,PoleSymb,PolColor)
            legendEntries.append(plot) 
            legendText.append(' %s (poles to planes) n=%d' % (self.Pname[i],self.Pndata[i]))


        #plot poles to lines
        for i in self.l_polesList:
            Plinesize = self.LProps[i]["linespin"]
            LineSymb = self.LProps[i]["LineSymb"]
            LinColor = self.LProps[i]["LinColor"]
            plot =  PlotPolesLines(self.gridtype,axes,self.Lazim[i],self.Ldip[i],Plinesize,LineSymb,LinColor)
            legendEntries.append(plot) 
            legendText.append('[L] %s (poles to lines) n=%d' % (self.Lname[i],self.Lndata[i]))


        #plot eigenvectors (pole and great circle) of PLANES
        for i in self.p_girdList:

            if self.PProps[i]["cb_eigen_gc1"] == True: # plot great circle for eigenvector 1
                CircGirdColor = self.PProps[i]["CircGirdColor1"]
                CircGirdSty = self.PProps[i]["styleGirdCirc1"]
                circspin = self.PProps[i]["circGirdspin1"]
                azim = [self.PeigenDict[i]["az_v1"]]
                dip = [self.PeigenDict[i]["dp_v1"]]
                # we need the plane that has this EV as its pole, and also the strike
                azim = [az + 180.0 if az + 180.0 < 360.0 else az + 180.0 - 360.0 for az in azim] # pole azim
                dip = [90.0 - dp for dp in dip] # pole dip
                strike = [az+270 if 0<=az<=90 else az-90 for az in azim]
                col = PlotGreatCircle(self.gridtype,axes,azim,strike,dip,CircGirdColor,CircGirdSty,circspin)
                legendEntries.append(col) 
                legendText.append(' %s (g.circle EV 1)' % self.Pname[i])

            if self.PProps[i]["cb_eigen_p1"] == True: # plot pole for eigenvector 1
                PolGirdColor = self.PProps[i]["PolGirdColor1"]
                PoleGirdSymb = self.PProps[i]["symbGirdPoles1"]
                polespin = self.PProps[i]["poleGirdspin1"]
                azim = self.PeigenDict[i]["az_v1"]
                dip = self.PeigenDict[i]["dp_v1"]
                plot = PlotPolesLines(self.gridtype,axes,[azim],[dip],polespin,PoleGirdSymb,PolGirdColor)
                legendEntries.append(plot) 
                legendText.append(' %s (eigenvector 1)' % self.Pname[i])

            if self.PProps[i]["cb_eigen_gc2"] == True: # plot great circle for eigenvector 2
                CircGirdColor = self.PProps[i]["CircGirdColor2"]
                CircGirdSty = self.PProps[i]["styleGirdCirc2"]
                circspin = self.PProps[i]["circGirdspin2"]
                azim = [self.PeigenDict[i]["az_v2"]]
                dip = [self.PeigenDict[i]["dp_v2"]]
                azim = [az + 180.0 if az + 180.0 < 360.0 else az + 180.0 - 360.0 for az in azim] # pole azim
                dip = [90.0 - dp for dp in dip] # pole dip
                strike = [az+270 if 0<=az<=90 else az-90 for az in azim]
                col = PlotGreatCircle(self.gridtype,axes,azim,strike,dip,CircGirdColor,CircGirdSty,circspin)
                legendEntries.append(col) 
                legendText.append(' %s (g.circle EV 2)' % self.Pname[i])

            if self.PProps[i]["cb_eigen_p2"] == True: # plot pole for eigenvector 2
                PolGirdColor = self.PProps[i]["PolGirdColor2"]
                PoleGirdSymb = self.PProps[i]["symbGirdPoles2"]
                polespin = self.PProps[i]["poleGirdspin2"]
                azim = self.PeigenDict[i]["az_v2"]
                dip = self.PeigenDict[i]["dp_v2"]
                plot = PlotPolesLines(self.gridtype,axes,[azim],[dip],polespin,PoleGirdSymb,PolGirdColor)
                legendEntries.append(plot) 
                legendText.append(' %s (eigenvector 2)' % self.Pname[i])

            if self.PProps[i]["cb_eigen_gc3"] == True: # plot great circle for eigenvector 3
                CircGirdColor = self.PProps[i]["CircGirdColor3"]
                CircGirdSty = self.PProps[i]["styleGirdCirc3"]
                circspin = self.PProps[i]["circGirdspin3"]
                azim = [self.PeigenDict[i]["az_v3"]]
                dip = [self.PeigenDict[i]["dp_v3"]]
                azim = [az + 180.0 if az + 180.0 < 360.0 else az + 180.0 - 360.0 for az in azim] # pole azim
                dip = [90.0 - dp for dp in dip] # pole dip
                strike = [az+270 if 0<=az<=90 else az-90 for az in azim]
                col = PlotGreatCircle(self.gridtype,axes,azim,strike,dip,CircGirdColor,CircGirdSty,circspin)
                legendEntries.append(col) 
                legendText.append(' %s (g.circle EV 3)' % self.Pname[i])

            if self.PProps[i]["cb_eigen_p3"] == True: # plot pole for eigenvector 3
                PolGirdColor = self.PProps[i]["PolGirdColor3"]
                PoleGirdSymb = self.PProps[i]["symbGirdPoles3"]
                polespin = self.PProps[i]["poleGirdspin3"]
                azim = self.PeigenDict[i]["az_v3"]
                dip = self.PeigenDict[i]["dp_v3"]
                plot = PlotPolesLines(self.gridtype,axes,[azim],[dip],polespin,PoleGirdSymb,PolGirdColor)
                legendEntries.append(plot) 
                legendText.append(' %s (eigenvector 3)' % self.Pname[i])


        #plot eigenvectors (pole and great circle) of LINES
        for i in self.l_girdList:

            if self.LProps[i]["cb_eigen_gc1"] == True: # plot great circle for eigenvector 1
                CircGirdColor = self.LProps[i]["CircGirdColor1"]
                CircGirdSty = self.LProps[i]["styleGirdCirc1"]
                circspin = self.LProps[i]["circGirdspin1"]
                azim = [self.LeigenDict[i]["az_v1"]]
                dip = [self.LeigenDict[i]["dp_v1"]]
                azim = [az + 180.0 if az + 180.0 < 360.0 else az + 180.0 - 360.0 for az in azim] # pole azim
                dip = [90.0 - dp for dp in dip] # pole dip
                strike = [az+270 if 0<=az<=90 else az-90 for az in azim]
                col = PlotGreatCircle(self.gridtype,axes,azim,strike,dip,CircGirdColor,CircGirdSty,circspin)
                legendEntries.append(col) 
                legendText.append('[L] %s (g.circle EV 1)' % self.Lname[i])

            if self.LProps[i]["cb_eigen_p1"] == True: # plot pole for eigenvector 1
                PolGirdColor = self.LProps[i]["PolGirdColor1"]
                PoleGirdSymb = self.LProps[i]["symbGirdPoles1"]
                polespin = self.LProps[i]["poleGirdspin1"]
                azim = self.LeigenDict[i]["az_v1"]
                dip = self.LeigenDict[i]["dp_v1"]
                plot = PlotPolesLines(self.gridtype,axes,[azim],[dip],polespin,PoleGirdSymb,PolGirdColor)
                legendEntries.append(plot) 
                legendText.append('[L] %s (eigenvector 1)' % self.Lname[i])

            if self.LProps[i]["cb_eigen_gc2"] == True: # plot great circle for eigenvector 2
                CircGirdColor = self.LProps[i]["CircGirdColor2"]
                CircGirdSty = self.LProps[i]["styleGirdCirc2"]
                circspin = self.LProps[i]["circGirdspin2"]
                azim = [self.LeigenDict[i]["az_v2"]]
                dip = [self.LeigenDict[i]["dp_v2"]]
                azim = [az + 180.0 if az + 180.0 < 360.0 else az + 180.0 - 360.0 for az in azim] # pole azim
                dip = [90.0 - dp for dp in dip] # pole dip
                strike = [az+270 if 0<=az<=90 else az-90 for az in azim]
                col = PlotGreatCircle(self.gridtype,axes,azim,strike,dip,CircGirdColor,CircGirdSty,circspin)
                legendEntries.append(col) 
                legendText.append('[L] %s (g.circle EV 2)' % self.Lname[i])

            if self.LProps[i]["cb_eigen_p2"] == True: # plot pole for eigenvector 2
                PolGirdColor = self.LProps[i]["PolGirdColor2"]
                PoleGirdSymb = self.LProps[i]["symbGirdPoles2"]
                polespin = self.LProps[i]["poleGirdspin2"]
                azim = self.LeigenDict[i]["az_v2"]
                dip = self.LeigenDict[i]["dp_v2"]
                plot = PlotPolesLines(self.gridtype,axes,[azim],[dip],polespin,PoleGirdSymb,PolGirdColor)
                legendEntries.append(plot)
                legendText.append('[L] %s (eigenvector 2)' % self.Lname[i])

            if self.LProps[i]["cb_eigen_gc3"] == True: # plot great circle for eigenvector 3
                CircGirdColor = self.LProps[i]["CircGirdColor3"]
                CircGirdSty = self.LProps[i]["styleGirdCirc3"]
                circspin = self.LProps[i]["circGirdspin3"]
                azim = [self.LeigenDict[i]["az_v3"]]
                dip = [self.LeigenDict[i]["dp_v3"]]
                azim = [az + 180.0 if az + 180.0 < 360.0 else az + 180.0 - 360.0 for az in azim] # pole azim
                dip = [90.0 - dp for dp in dip] # pole dip
                strike = [az+270 if 0<=az<=90 else az-90 for az in azim]
                col = PlotGreatCircle(self.gridtype,axes,azim,strike,dip,CircGirdColor,CircGirdSty,circspin)
                legendEntries.append(col) 
                legendText.append('[L] %s (g.circle EV 3)' % self.Lname[i])

            if self.LProps[i]["cb_eigen_p3"] == True: # plot pole for eigenvector 3
                PolGirdColor = self.LProps[i]["PolGirdColor3"]
                PoleGirdSymb = self.LProps[i]["symbGirdPoles3"]
                polespin = self.LProps[i]["poleGirdspin3"]
                azim = self.LeigenDict[i]["az_v3"]
                dip = self.LeigenDict[i]["dp_v3"]
                plot = PlotPolesLines(self.gridtype,axes,[azim],[dip],polespin,PoleGirdSymb,PolGirdColor)
                legendEntries.append(plot) 
                legendText.append('[L] %s (eigenvector 3)' % self.Lname[i])

        #plot small circles
        for i in self.sc_list:
            ScColor = self.ScProps[i]["ScColor"]
            ScSty = self.ScProps[i]["ScSty"]
            ScSpin = self.ScProps[i]["ScSpin"]
            ScFull = self.ScProps[i]["ScFull"]
            col = PlotSmallCircle(self.gridtype,axes,self.Scazim[i],self.Scdip[i],self.Scalpha[i],ScFull,ScColor,ScSty,ScSpin)
            legendEntries.append(col) 
            legendText.append('[SC] %s (small circle) n=%d' % (self.Scname[i],self.Scndata[i]))

        # plot 95% confidence cone for PLANES
        for i in self.idxPlan:
            if self.PProps[i]["cb_conf"] == True: # plot confidence cone
                alpha = [self.PeigenDict[i]["confCone"]]
                ScColor = self.PProps[i]["conCircColor"]
                ScSty = self.PProps[i]["conCircSty"]
                ScSpin = self.PProps[i]["conspin"]
                ScFull = 0
                azim = [self.PeigenDict[i]["az_v1"]]
                iang = [self.PeigenDict[i]["dp_v1"]]
                col = PlotSmallCircle(self.gridtype,axes,azim,iang,alpha,ScFull,ScColor,ScSty,ScSpin)
                legendEntries.append(col) 
                legendText.append(' %s 95%% confidence cone' % self.Pname[i])

        # plot 95% confidence cone for LINES
        for i in self.idxLin:
            if self.LProps[i]["cb_conf"] == True: # plot confidence cone
                alpha = [self.LeigenDict[i]["confCone"]]
                ScColor = self.LProps[i]["conCircColor"]
                ScSty = self.LProps[i]["conCircSty"]
                ScSpin = self.LProps[i]["conspin"]
                ScFull = 0
                azim = [self.LeigenDict[i]["az_v1"]]
                iang = [self.LeigenDict[i]["dp_v1"]]
                col = PlotSmallCircle(self.gridtype,axes,azim,iang,alpha,ScFull,ScColor,ScSty,ScSpin)
                legendEntries.append(col) 
                legendText.append('[L] %s 95%% confidence cone' % self.Lname[i])


        # some texts
        if self.gridtype == 'schmidt':
            axes.text(-0.95,-1.08,'Equal-area\nLower hemisphere',family='sans-serif',size=self.fontSize,horizontalalignment='left')
        elif self.gridtype == 'wulff':
            axes.text(-0.95,-1.08,'Equal-angle\nLower hemisphere',family='sans-serif',size=self.fontSize,horizontalalignment='left')


        # legend
        try:
            leg = axes.legend(legendEntries,legendText,bbox_to_anchor=(0.95, 0.95), loc=2, prop=FontProperties(size=self.fontSize),numpoints=1, fancybox=True)
            leg.draw_frame(False) 
        except:
            pass


        # set the axes limits and draws the stuff
        axes.set_xlim(-1.1,1.2)
        axes.set_ylim(-1.15,1.15)
        self.stereoCanvas.draw()



#        except AttributeError: # in case nothing was found, that is, no file has been opened
#            dlg = wx.MessageDialog(self, ' Data file not found\n or nothing checked for plotting', 'Oooops!', wx.OK|wx.ICON_ERROR)
#            dlg.ShowModal()
#            dlg.Destroy()
#            pass

#-----------------------------------------------------------------------------


#function for ploting the stereonet circle
def PlotStereoNetCircle(axes, caxes, fontsize):
    """Function to create the stereonet circle"""
    caxes.cla()
    caxes.set_axis_off()
    axes.cla()
    axes.set_axis_off()
    x_cross = [0,1,0,-1,0]
    y_cross = [0,0,1,0,-1]
    axes.plot(x_cross,y_cross,'k+',markersize=8,label='_nolegend_')
    axes.text(0.01,1.025,'N', family='sans-serif', size=fontsize, horizontalalignment='center' )
    circ = Circle( (0,0), radius=1, edgecolor='black', facecolor='none', clip_box='None',label='_nolegend_')
    axes.add_patch(circ)


#function for ploting the stereonet grid (Schmidt) - functions from RFOC
def PlotStereoNetGridSchmidt(axes,gridStep):
    """Function to create the grid inside the stereonet (equal-area Schimdt net)"""

    GridColor = 'grey'
    GridSty = '-'

    for j in range(-(90-gridStep),90,gridStep): #small circle spacing
        lam = np.pi * np.arange(0,185,5)/180 # steps to draw each small circle
        lam0 = np.pi / 2
        phi = np.radians(j)
        R = np.sqrt(2)/2
        kp = np.sqrt(2/(1+np.cos(phi) * np.cos(lam - lam0)))
        xj = R * kp * np.cos(phi) * np.sin(lam - lam0)
        yj = R * kp * np.sin(phi)
        s_circle = Line2D(xj,yj, c=GridColor, ls=GridSty, lw=0.25,label='_nolegend_')
        axes.add_line(s_circle)

    for j in range(gridStep,180,gridStep):#great circle spacing
        phi = np.arange(-90,95,5) * np.pi/180 # steps to draw each great circle
        lam = np.radians(j)
        R = np.sqrt(2)/2
        kp = np.sqrt(2/(1+np.cos(phi) * np.cos(lam - lam0)))
        xj = R * kp * np.cos(phi) * np.sin(lam - lam0)
        yj = R * kp * np.sin(phi)
        g_circle = Line2D(xj,yj, c=GridColor, ls=GridSty, lw=0.25,label='_nolegend_')
        axes.add_line(g_circle)


#function for ploting the stereonet grid (Wulff)
def PlotStereoNetGridWulff(axes,gridStep):
    """Function to create the grid inside the stereonet (equal-angle Wulff net)"""

    GridColor = 'grey'
    GridSty = '-'

    # great circles 
    dip = np.arange(gridStep,90.5,gridStep)
    azim = len(dip) * [90]
    for i in range(len(azim)):
        x,y = pd.GreatCircleWulffLine2D(azim[i],dip[i])
        g_circle = Line2D(x,y, c=GridColor, ls=GridSty, lw=0.25,label='_nolegend_')
        axes.add_line(g_circle)
    dip = np.arange(gridStep,90.0,gridStep)
    azim = len(dip) * [270]
    for i in range(len(azim)):
        x,y = pd.GreatCircleWulffLine2D(azim[i],dip[i])
        g_circle = Line2D(x,y, c=GridColor, ls=GridSty, lw=0.25,label='_nolegend_')
        axes.add_line(g_circle)

    # small circles
    GridSty = 'solid'
    dp1 = np.arange(gridStep,90.5,gridStep)
    az1 = len(dp1) * [0]
    dp2 = np.arange(gridStep,90.0,gridStep)
    az2 = len(dp2) * [180]
    azim = np.append(az1,az2)
    dip = np.append(dp1,dp2)

    for i in range(len(azim)):
        if dip[i] == 90: dip[i] = 89.99
        beta = 90 - dip[i]
        ddir = azim[i] - 90
        dist = 1/np.sin(np.radians(beta))
        R = 1/np.tan(np.radians(beta))
        h = 0 + dist * np.cos(np.radians(ddir))
        k = 0 - dist * np.sin(np.radians(ddir))
        theta1 = ddir - beta 
        theta2 = ddir + beta 
        g_circ = Arc((h,k), width=2*R, height=2*R, angle=0.0, theta1=theta1, theta2=theta2, fc='none', ec=GridColor, ls=GridSty, lw=0.25,label='_nolegend_')
        axes.add_line(g_circ)


# great circles -- (Schmidt From RFOC - FAST!!)
def PlotGreatCircle(gridtype,axes,azim,strike,dip,circcol,circsty,circwdt):
    """Function for plot great circles of planes in stereonet """

    if circsty == '-':
        ccsty = 'solid'
    elif circsty == ':':
        ccsty = 'dotted'
    elif circsty == '--':
        ccsty = 'dashed'
    elif circsty == '-.':
        ccsty = 'dashdot'

    if gridtype == 'schmidt':
        listXY = pd.GreatCircleSchmidt(strike,dip)
    elif gridtype == 'wulff':
        listXY = pd.GreatCircleWulff(azim,dip)

    col = LineCollection(listXY, linewidths=circwdt, colors=circcol, linestyles=ccsty)
    axes.add_collection(col, autolim=True)
    return col


# poles to planes
def PlotPolesPlanes(gridtype,axes,azim,dip,polesize,polesymb,polecol):
    """function for plot poles to planes"""
    x_pole, y_pole = pd.PolesPlanes(gridtype,azim,dip)
    plot = axes.plot(x_pole,y_pole, polesymb, c=polecol, ms=polesize)
    return plot


# poles to lines
def PlotPolesLines(gridtype,axes,azim,dip,linesize,linesymb,linecol):
    """function for plot poles to lineations"""
    x_line, y_line = pd.PolesLines(gridtype,azim,dip)
    plot = axes.plot(x_line,y_line, linesymb, c=linecol, ms=linesize)
    return plot


#function for ploting small circles
def PlotSmallCircle(gridtype,axes,az,iang,alpha,full,ScColor,ScSty,ScSpin):#,smallName)
    """Function for plot small circles of planes in stereonet (Wulff)"""

    if type(az) is not list: # case where one single value was passed
        az = [az]
        iang = [iang]
        alpha = [alpha]

    if type(az[0]) is np.ndarray: # more than one value in file, comes as list of numpy arrays
        az = az[0]
        iang = iang[0]
        alpha = alpha[0]

    for i in range(len(az)):
        if ScSty == '-':
            SSty = 'solid'
        elif ScSty == ':':
            SSty = 'dotted'
        elif ScSty == '--':
            SSty = 'dashed'
        elif ScSty == '-.':
            SSty = 'dashdot'

        if gridtype == 'schmidt':
            listXY = pd.SmallCircleSchmidt(az,iang,alpha,full)
        elif gridtype == 'wulff':
            listXY = pd.SmallCircleWulff(az,iang,alpha,full)

    col = LineCollection(listXY, linewidths=ScSpin, colors=ScColor, linestyles=ScSty)
    axes.add_collection(col, autolim=True)

    return col


# slickensides 
def PlotSlickensides(gridtype,slip,axes,azim,dip,trend,plunge,sense,arrowsize,arrowcol,arrowwidth,plotpoles,linesize,linesymb,linecol,footwall):
    """function for plot slickensides"""

    listXY = pd.PolesSlickensides(gridtype,slip,azim,dip,trend,plunge,sense,arrowsize/10.0,footwall)

    for i in range(len(azim)):

        if footwall: # plot slip-linear for FOOTWALL movement (inverse of hangwall)
            dx = listXY[i][0][0]
            dy = listXY[i][0][1]
            x = listXY[i][1][0]
            y = listXY[i][1][1]
        else: # default, plot slickensides and slip-linear for HANGWALL movement
            x = listXY[i][0][0]
            y = listXY[i][0][1]
            dx = listXY[i][1][0]
            dy = listXY[i][1][1]

        if sense[i] in ['U','u','F','f']: # undefined faults (or fractures)
            und = Line2D((x,dx), (y,dy), c=arrowcol, ls='-', lw=arrowwidth,label='_nolegend_')
            axes.add_line(und)
        else:
            axes.add_patch(FancyArrowPatch((x,y), (dx,dy), shrinkA=0.0, shrinkB=0.0, arrowstyle='->,head_length=2.5,head_width=1',connectionstyle='arc3,rad=0.0',mutation_scale=2.0, lw=arrowwidth, ec=arrowcol))

    if plotpoles:
        if slip:
            x, y = pd.PolesPlanes(gridtype,azim,dip)
        else:
            x, y = pd.PolesLines(gridtype,trend,plunge)
        plot = axes.plot(x,y, linesymb, c=linecol, ms=linesize)

    col = LineCollection(listXY, linewidths=arrowwidth, colors=arrowcol, linestyles='solid')
#    axes.add_collection(col, autolim=True)#, width=0.01
    return col






















