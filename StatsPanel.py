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
import os, sys
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub


#import matplotlib
#import matplotlib
#matplotlib.use('WXAgg')

from matplotlib.figure import Figure
from matplotlib.collections import LineCollection

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg
#from matplotlib.axes import Subplot 
from mpl_toolkits.axes_grid.axislines import Subplot
from matplotlib.font_manager import fontManager, FontProperties

#from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
from matplotlib.text import Text

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
        self.DeleteToolByPos(3) # Pan

        self.Realize()

class StatsPanel(wx.Panel): 
    """class for the first page of the notebook """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

# default variables
        self.fontSize = 'x-small'

#split the notebook page in two and create panels
        panelsizer = wx.BoxSizer(wx.HORIZONTAL) # sizer
        splitter = wx.SplitterWindow(self, -1) 
        self.left_panel = wx.Panel(splitter, -1, style=wx.BORDER_SUNKEN)
        self.right_panel = wx.Panel(splitter, -1, style=wx.BORDER_SUNKEN)
        splitter.SetMinimumPaneSize(180) # cannot shrink panel to less than this

#initialize the figure and canvas
        self.dataFigure = Figure(figsize=(4,4),facecolor='white')
        self.dataCanvas = FigureCanvas(self.right_panel, -1, self.dataFigure)
        self.toolbar = VMToolbar(self.dataCanvas)

#layout of widgets, left panel
        self.control1 = wx.TextCtrl(self.left_panel, -1, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        self.copyBtn = wx.Button(self.left_panel, -1, _('Copy'), size=(60, 30))
        self.saveBtn = wx.Button(self.left_panel, -1, _('Save as'), size=(60, 30))

        hboxbt = wx.BoxSizer(wx.HORIZONTAL)
        hboxbt.Add(self.saveBtn,0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,3)
        hboxbt.Add(self.copyBtn,0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,3)

        self.Bind(wx.EVT_BUTTON, self.saveStats, self.saveBtn)
        self.Bind(wx.EVT_BUTTON, self.copyStats, self.copyBtn)

        box3 = wx.BoxSizer(wx.VERTICAL)
        box3.Add(self.control1, 1, wx.EXPAND)
        box3.Add(hboxbt,0,wx.ALIGN_CENTER)
        self.left_panel.SetSizer(box3)

#layout of canvas, right panel
# create draw/clear buttons 
        self.clearPlot_Button = wx.Button(self.right_panel, -1, _('Clear'), size=(55, 30))
        self.plotFlinn_Button = wx.Button(self.right_panel, -1, _('2-axis'), size=(55, 30))
        self.plotVollmer_Button = wx.Button(self.right_panel, -1, _('Triang.'), size=(55, 30))

        hboxTB = wx.BoxSizer(wx.HORIZONTAL)
        hboxTB.Add(self.plotFlinn_Button,0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,3)
        hboxTB.Add(self.plotVollmer_Button,0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,3)
        hboxTB.Add(self.clearPlot_Button,0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,3)
        hboxTB.Add(self.toolbar, 1, wx.EXPAND|wx.ALL, 1)

        self.Bind(wx.EVT_BUTTON, self.ClearPlot, self.clearPlot_Button)
        self.Bind(wx.EVT_BUTTON, self.PlotFlinn, self.plotFlinn_Button)
        self.Bind(wx.EVT_BUTTON, self.PlotVollmer, self.plotVollmer_Button)

#layout of canvas
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(self.dataCanvas, 1, wx.EXPAND)
        vbox2.Add(hboxTB,0, wx.EXPAND|wx.ALL, 1)
#        vbox2.Add(self.toolbar, 0, wx.EXPAND|wx.ALL, 1)
        self.right_panel.SetSizer(vbox2)

#splitter
        splitter.SplitVertically(self.left_panel,self.right_panel,190) 
        panelsizer.Add(splitter,1, wx.EXPAND|wx.ALL, 2) # the panels are inside this sizer with 2px border

        self.SetSizer(panelsizer)
#        panelsizer.Fit(self)

# subscriptions to pubsub  
        pub.subscribe(self.__onReceivePlanarData, 'object.Plan_added_DDD') # from MainForm
        pub.subscribe(self.__onReceivePlanarData, 'object.Plan_added_RH') # from MainForm
        pub.subscribe(self.__onReceiveLinearData, 'object.Lin_added') # from MainForm
        pub.subscribe(self.__onReceiveFontSize, 'object.FontSize') # from MainForm

        pub.subscribe(self.__onReceiveChecked, 'object.checked') # from TreePanel (namesList)

        pub.subscribe(self.__onReceiveNameSel, 'object.selected_vals') # from TreePanel
        pub.subscribe(self.__onReceiveSelection, 'object.selected') # from TreePanel

        pub.subscribe(self.__onReceivePropsPlan, 'object.PropsPlanReceiv') # from TreePanel, OnPopup_childPlanar, OnDClick_childPlanar
        pub.subscribe(self.__onReceivePropsLin, 'object.PropsLinReceiv')# from TreePanel, OnPopup_childLinear, OnDClick_childLinear



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
            self.PeigenList=[]
            self.PidxList=[]
            self.PProps=[]

        for i in range(len(message.data)):
            self.Ptype.append(message.data[i][0])       # filetype
#            self.Pname.append(message.data[i][1])       # filename
            self.Pndata.append(message.data[i][2])      # n_data
            self.Pazim.append(message.data[i][3])       # azim
            self.Pdip.append(message.data[i][4])        # dip
            self.PeigenList.append(message.data[i][6])  # eigenDict
            self.PidxList.append(message.data[i][7])    # DDD_idx
            self.PProps.append(message.data[i][8])      # pplist

            if message.data[i][7].startswith('D'): # dip-dir data
                self.Pname.append('[P(dd)] %s' % message.data[i][1])
            else: # right-hand data
                self.Pname.append('[P(rh)] %s' % message.data[i][1])


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
            self.LeigenList=[]
            self.LidxList=[]
            self.LProps=[]

        for i in range(len(message.data)):
            self.Ltype.append(message.data[i][0])       # filetype
            self.Lname.append('[L] %s' % message.data[i][1])       # filename
            self.Lndata.append(message.data[i][2])      # n_data
            self.Lazim.append(message.data[i][3])       # azim
            self.Ldip.append(message.data[i][4])        # dip
            self.LeigenList.append(message.data[i][6])  # eigenDict
            self.LidxList.append(message.data[i][7])    # Lin_idx
            self.LProps.append(message.data[i][8])      # lplist

# graphic properties of planar data - same as in StereoPanel, but doesn't send data to TreePanel
    def __onReceivePropsPlan(self, message): # object.PropsPlanRec
        PropsPlan = message.data
        idx = self.PidxList.index(PropsPlan["pdata"])
        self.PProps[idx] = PropsPlan # replace default props by user-defined ones


# graphic properties of linear data - same as in StereoPanel, but doesn't send data to TreePanel
    def __onReceivePropsLin(self, message): 
        PropsLin = message.data
        idx = self.LidxList.index(PropsLin["pdata"])
        self.LProps[idx] = PropsLin # replace default props by user-defined ones


# which files are checked to plot
    def __onReceiveChecked(self, message): 
        checkedList = message.data
        self.idxPlan = []
        self.idxLin = []

        for checked in checkedList:
            if checked[1] == 1 and checked[0] in self.PidxList: # checked[1] = 1: planar data
                self.idxPlan.append(self.PidxList.index(checked[0]))
            elif checked[1] == 2 and checked[0] in self.LidxList: # checked[1] = 2: linear data
                self.idxLin.append(self.LidxList.index(checked[0]))

# which file is selected
    def __onReceiveSelection(self, message): 
        self.file_i = message.data

# font size
    def __onReceiveFontSize(self, message):
        self.fontSize = message.data


# which kind of file is selected
    def __onReceiveNameSel(self, message):
        self.name = message.data["itemName"]
        self.nametype = message.data["dtype"]

        if message.data["dtype"] == 1 or message.data["dtype"] == 2:        # 1 == Planar, 2 == Linear

            if message.data["dtype"] == 1:
                nametype = str(message.data["itemName"])#[3:len(message.data["itemName"])]) + ' (planar)'
            else:
                nametype = str(message.data["itemName"])#[3:len(message.data["itemName"])]) + ' (linear)'


            if message.data["ndata"] <= 3: # must have at least three values for eigen analysis
                args = (nametype, message.data["ndata"])
#os.linesep 
                showdata =''' file: %s

 n = %d

 There are too
 few points in file.

 Must have at least 
 three points for
 statistical analysis.

''' % args

            else: # there are more than three values in file

                # uniformity test(from QuickPlot)
                # original comments from QuickPlot source code:
                # van Everdingen et al., 1992, Computers and Geosciences v18 n2/3, p183-287.
                # ------------------------------------
                # rv95 contains critical values for the Rayleigh test of uniformity at the
                # 0.05 level. Values range from N = 5 to 100+ and model a Chi squared
                # distribution 0 degres of freedom) at N > 100. Based on Table Appendix 3.5
                # Mardia, 1972 - in Griffis et al.; 1985; Computers and Geosciences v4 n4, p369-408.

                rv95 =[0.7, 0.642, 0.597, 0.56, 0.529, 0.503, 0.48, 0.46, 0.442, 0.427, 0.413, 0.4, 0.388, 0.377, 0.367, \
                        0.358, 0.35, 0.342, 0.334, 0.328, 0.321, 0.29, 0.27, 0.26, 0.24, 0.23, 0.16, 7.185]

                ndata = message.data["ndata"]
                vector = message.data["Vect"]
                RB = vector / ndata
                if ndata < 5:
                    IV = 0
                elif ndata >= 5 and ndata <= 25:
                    IV = ndata - 5
                elif ndata > 25 and ndata <= 50:
                    IV = ((ndata-25) / 5) + 20
                elif ndata > 50 and ndata <= 100:
                    IV = 26
                elif ndata > 100:
                    IV = 27
                ISIG = 2

                if IV == 0:
                    uniformtxt = ''' There are too
 few points to test 
 significance '''

                if IV != 0:
                    ISIG = 0
                    if RB > rv95[IV]:
                        ISIG = 1

                if ISIG == 0:
                    uniformtxt = ''' Data do not differ
 significantly from
 uniform at the 0.95 level '''

                if ISIG ==1:
                    uniformtxt = ''' Data differ
 significantly from 
 uniform at the 0.95 level '''

                # check if distribution is cluster or girdle (from QuickPlot)
                if message.data["K"] >= 1.1:
                    dist = 'Cluster'
                    if message.data["az_v1"] + 180.0 <= 360: 
                        dipdir = message.data["az_v1"] + 180.0
                    else:
                        dipdir = message.data["az_v1"] + 180.0 - 360.0
                    meanclstr = (dipdir,90-message.data["dp_v1"],message.data["az_v1"],message.data["dp_v1"])
                    disttxt =''' Mean Plane:
 dipdir/dip = %3.1f/%2.1f

 Axis:
 azim/plunge = %3.1f/%2.1f''' % meanclstr

                elif message.data["K"] >= 0.9 and message.data["K"] < 1.1:
                    dist = 'Cluster or Glirdle'
                    disttxt =''
                else:
                    dist = 'Girdle'
                    if message.data["az_v3"] + 180.0 <= 360:  
                        dipdir = message.data["az_v3"] + 180.0
                    else:
                        dipdir = message.data["az_v3"] + 180.0 - 360.0
                    girdl = (message.data["az_v3"],message.data["dp_v3"],dipdir,90-message.data["dp_v3"]) 
                    disttxt =''' Fold Axis:
 azim/plunge = %3.1f/%2.1f

 Best-fit Girdle:
 dipdir/dip = %3.1f/%2.1f''' % girdl

                # check the force of the preferential orientation (from QuickPlot)
                if message.data["C"] >= 6.0:
                    force = 'Strong'
                elif message.data["C"] >= 4.0 and message.data["C"] < 6.0:
                    force = 'Moderate'
                elif message.data["C"] >= 2.0 and message.data["C"] < 4.0:
                    force = 'Weak'
                else:
                    force = 'None'

                args = (nametype, message.data["ndata"], uniformtxt, dist, force, disttxt, \
                        message.data["confCone"], message.data["confK"], \
                        message.data["az_v1"], message.data["dp_v1"], \
                        message.data["az_v2"], message.data["dp_v2"], \
                        message.data["az_v3"], message.data["dp_v3"], \
                        message.data["K"], message.data["C"], \
                        message.data["S1"], message.data["S2"], message.data["S3"],\
                        message.data["P"], message.data["G"], message.data["R"])

                showdata =''' file: %s

 n = %d 

%s

 Expected Distribution:
 %s

 Preferential Orientation:
 %s

%s

 Radius of confidence
 at 5%%:
 %3.2f degrees
 K = %3.2f
 
 Eigenvectors: 
 1: %3.1f / %2.1f
 2: %3.1f / %2.1f
 3: %3.1f / %2.1f

 Shape parameter
 K = %3.2f

 Strength parameter
 C = %3.2f

 Normalized Eigenvalues:
 S1: %3.3f
 S2: %3.3f
 S3: %3.3f

 Fabric (triangular diag.): 
 Point  = %3.3f
 Girdle = %3.3f
 Random = %3.3f
''' % args

        else:
            
            
        
            if message.data["dtype"] == 3:
                showdata = '''
 Sorry, no stats
 for Small Circles.

'''
            else:
                showdata = '''
 Sorry, no stats
 for Faults/Slickensides.
 
 If you need stats, you
 can open only the Planar
 or Linear (slickensides)
 data from faults.
 (menu File -> Fault Data)


'''
        self.control1.SetValue(showdata) # show the stats

#save stats to txt file
    def saveStats(self, event):
        dlg = wx.FileDialog ( None, message='Save stats as', \
        wildcard='Text files (*.txt)|*.txt', style = wx.SAVE | wx.OVERWRITE_PROMPT )
        if self.nametype == 1: # planar data
            savename = 'stats_%s_%s' % (self.name[:7],self.name[8:len(self.name)])
        elif self.nametype == 2: # linear data
            savename = 'stats_%s_%s' % (self.name[:3],self.name[4:len(self.name)])

        dlg.SetFilename(savename)
        if dlg.ShowModal() == wx.ID_OK:
            statstxt = self.control1.GetValue()
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            filehandle=open(os.path.join(self.dirname, self.filename),'wt')
            filehandle.write(statstxt)
            filehandle.close()
        else:
           pass

        dlg.Destroy()

# copy stats to clipboard
    def copyStats(self, event):
        self.control1.SelectAll()
        self.control1.Copy()
        self.control1.SetSelection(0,0) #clear selection


# plot two-axis diagram (modfied Flinn by Woodcock) - from QuickPlot
    def PlotFlinn(self, event): 

        #initialize the plot areas
        self.dataFigure.clf()
        axes = Subplot(self.dataFigure, 111, clip_on='True',xlim=(-0.2,7.2), ylim=(-0.2,7.2),autoscale_on='True',xlabel='ln(S2/S3)',ylabel='ln(S1/S2)',label='flinn',aspect='equal', adjustable='box',anchor='W')
        self.dataFigure.add_subplot(axes)
        axes.axis["right"].set_visible(False)
        axes.axis["top"].set_visible(False)

        try:
            # plot lines of K
            for i in [0.2, 0.5, 1.0, 2.0, 5.0]:
                if i <= 1.0:
                    diag = Line2D((0,7.0),(0,(i*7.0)),c='grey',lw=0.5)
                    axes.add_line(diag)
                else:
                    diag = Line2D((0,(7.0/i)),(0,7.0),c='grey',lw=0.5)
                    axes.add_line(diag)

            # plot lines of C
            for j in [2,4,6]:
                diag2 = Line2D((0,j),(j,0),c='grey',lw=0.5)
                axes.add_line(diag2)

            # texts
            axes.text(6.25,0.05,'K = 0',family='sans-serif',size=self.fontSize,horizontalalignment='left',color='grey')
            axes.text(0.15,6.1,'K = inf.',family='sans-serif',size=self.fontSize,horizontalalignment='left',color='grey',rotation='vertical')
            axes.text(6.45,6.4,'K = 1',family='sans-serif',size=self.fontSize,horizontalalignment='center',color='grey',rotation='45')
            axes.text(3.2,6.4,'K = 2',family='sans-serif',size=self.fontSize,horizontalalignment='center',color='grey',rotation='63.5')
            axes.text(1.2,6.4,'K = 5',family='sans-serif',size=self.fontSize,horizontalalignment='center',color='grey',rotation='78.7')
            axes.text(6.4,3.1,'K = 0.5',family='sans-serif',size=self.fontSize,horizontalalignment='center',color='grey',rotation='26.6')
            axes.text(6.5,1.3,'K = 0.2',family='sans-serif',size=self.fontSize,horizontalalignment='center',color='grey',rotation='11.3')
            axes.text(2.6,3.35,'C = 6',family='sans-serif',size=self.fontSize,horizontalalignment='center',color='grey',rotation='-45')
            axes.text(1.75,2.2,'C = 4',family='sans-serif',size=self.fontSize,horizontalalignment='center',color='grey',rotation='-45')

            axes.text(3.5,3.75,'Girdle/Cluster Transition',family='sans-serif',size=self.fontSize,horizontalalignment='left',verticalalignment='bottom',color='grey',rotation='45')
            axes.text(6.5,7.2,'CLUSTERS',family='sans-serif',size=self.fontSize,horizontalalignment='right',verticalalignment='bottom',color='grey')
            axes.text(7.2,6.5,'GIRDLES',family='sans-serif',size=self.fontSize,horizontalalignment='left',verticalalignment='top',color='grey',rotation='-90')


            # plot the selected (checked) files
            # propsPList = [pdata, itemName, PolColor, symbPoles, polespin,...
            # propsLList = [pdata, itemName, LinColor, LineSymb, linespin,...

            if len(self.idxPlan) == 0 and len(self.idxLin) == 0: # in case we have only one one opened file but it is not checked
                raise AttributeError
            else:
                for i in range(len(self.idxPlan)):
                    axes.plot(self.PeigenList[i]["K_x"],self.PeigenList[i]["K_y"], self.PProps[i]["PoleSymb"], c=self.PProps[i]["PolColor"], ms=self.PProps[i]["polespin"], label='%s n=%d' % (self.Pname[i],self.Pndata[i]))

                for j in range(len(self.idxLin)):
                    axes.plot(self.LeigenList[j]["K_x"],self.LeigenList[j]["K_y"], self.LProps[j]["LineSymb"], c=self.LProps[j]["LinColor"], ms=self.LProps[j]["linespin"], label='%s n=%d' % (self.Lname[j],self.Lndata[j]))

            axes.legend(bbox_to_anchor=(1.1, 1), loc=2, prop=FontProperties(size='small'),numpoints=1)

            #set the axes limits and draws the stuff
            axes.set_xlim(0.0,7.2)
            axes.set_ylim(0.0,7.2)
            self.dataCanvas.draw()

        except AttributeError:
            self.dataFigure.clf()
            dlg = wx.MessageDialog(None, 'No file(s) selected (checked).\n\n', 'Oooops!', wx.OK|wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            pass


# plot triangular fabric diagram (Vollmer) - from QuickPlot
    def PlotVollmer(self, event): 

        #initialize the plot areas
        self.dataFigure.clf()
        axes = Subplot(self.dataFigure, 111, clip_on='True',xlim=(-0.1,1.05), ylim=(-0.1,1.05),autoscale_on='True',label='vollmer',aspect='equal', adjustable='box',anchor='SW')
        self.dataFigure.add_subplot(axes)
        axes.axis["right"].set_visible(False)
        axes.axis["top"].set_visible(False)
        axes.axis["bottom"].set_visible(False)
        axes.axis["left"].set_visible(False)



        try:
            sqrt3_2 = 0.866025  #m_sqrt(3)/2

            tr1 = Line2D((0,1),(0,0),c='black')
            axes.add_line(tr1)
            tr2 = Line2D((0,0.5),(0,sqrt3_2),c='black')
            axes.add_line(tr2)
            tr3 = Line2D((1,0.5),(0,sqrt3_2),c='black')
            axes.add_line(tr3)



            for i in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:
                diag = Line2D((i/2,1.0-i/2),(sqrt3_2*i,sqrt3_2*i),c='grey',lw=0.5)
                axes.add_line(diag)
                diag2 = Line2D((i/2,i),(sqrt3_2*i,0),c='grey',lw=0.5)
                axes.add_line(diag2)
                diag3 = Line2D((i,i+(1-i)/2),(0,sqrt3_2-sqrt3_2*i),c='grey',lw=0.5)
                axes.add_line(diag3)


            axes.text(-0.08,-0.05,'Point',family='sans-serif',size=self.fontSize,horizontalalignment='left' )
            axes.text(0.97,-0.05,'Girdle',family='sans-serif',size=self.fontSize,horizontalalignment='left' )
            axes.text(0.5,0.88,'Random',family='sans-serif',size=self.fontSize,horizontalalignment='center' )

            # label axes values
            for i in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:
                axes.text((1-i)/2, sqrt3_2*(1-i)-0.01, '%d' % (i*100), family='sans-serif', size=self.fontSize, horizontalalignment='right', color='grey', rotation='60')
                axes.text(i, -0.02,'%d' % (i*100), family='sans-serif', size=self.fontSize, horizontalalignment='center', verticalalignment='top', color='grey')
                axes.text(1.0-i/2, sqrt3_2*i-0.01,'%d' % (i*100) , family='sans-serif', size=self.fontSize, horizontalalignment='left', color='grey', rotation='-60')


            # ternary plot (from wikipedia)
            # P = (0,0)
            # G = (1,0)
            # R = (1/2, sqrt(3)/2)
            # given (P,G,R):
            # x = G + R/2
            # y = (sqrt(3)/2) * R

            if len(self.idxPlan) == 0 and len(self.idxLin) == 0: # in case we have only one one opened file but it is not checked
                raise AttributeError
            else:
                for i in range(len(self.idxPlan)):
                    x = self.PeigenList[i]["G"] + (self.PeigenList[i]["R"] / 2)
                    y = self.PeigenList[i]["R"] * sqrt3_2
                    axes.plot(x,y, self.PProps[i]["PoleSymb"], c=self.PProps[i]["PolColor"], ms=self.PProps[i]["polespin"],label='%s n=%d' % (self.Pname[i],self.Pndata[i]))

                for j in range(len(self.idxLin)):
                    x = self.LeigenList[j]["G"] + (self.LeigenList[j]["R"] / 2)
                    y = self.LeigenList[j]["R"] * sqrt3_2
                    axes.plot(x,y, self.LProps[j]["LineSymb"], c=self.LProps[j]["LinColor"], ms=self.LProps[j]["linespin"],label='%s n=%d' % (self.Lname[j],self.Lndata[j]))


            axes.legend(bbox_to_anchor=(0.97, 0.8), loc=2, prop=FontProperties(size=self.fontSize),numpoints=1)

            axes.set_xlim(-0.1,1.05)
            axes.set_ylim(-0.1,1.05)
            self.dataCanvas.draw()

        except AttributeError:
            self.dataFigure.clf()
            dlg = wx.MessageDialog(None, _('No file(s) selected (checked).\n\n'), _('Oooops!'), wx.OK|wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            pass


# clear plot area
    def ClearPlot(self, event):
        self.dataFigure.clf()
        self.dataCanvas.draw()




