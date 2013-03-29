# Using the magic encoding
# -*- coding: utf-8 -*-


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
import scrolledpanel as scrolled
import floatspin as FS

from wx.lib.pubsub import Publisher as pub
import wx.lib.colourselect as csel

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg


from matplotlib.patches import Wedge
from matplotlib.patches import FancyArrowPatch
from matplotlib.patches import Circle
from matplotlib.patches import Arc
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
from matplotlib.text import Text

import numpy as np


#fonts = ['xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large']


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


class RosePanel(wx.Panel):
    """class for the third page of the notebook """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent

        self.mainframe = wx.GetTopLevelParent(self)

#split the notebook page in two and create panels
        panelsizer = wx.BoxSizer(wx.HORIZONTAL) # sizer
        splitter = wx.SplitterWindow(self, -1) 
        self.left_panel = scrolled.ScrolledPanel(splitter, -1, style=wx.BORDER_SUNKEN)
        self.left_panel.SetVirtualSizeWH(200, 200)
        self.left_panel.SetScrollRate(10,10)

        self.right_panel = wx.Panel(splitter, -1, style=wx.BORDER_SUNKEN)
        splitter.SetMinimumPaneSize(115) # cannot shrink panel to less than this

#initialize the figure and canvas
        self.roseFigure = Figure(figsize=(4,4),facecolor='white')
        self.roseCanvas = FigureCanvas(self.right_panel, -1, self.roseFigure)
        self.toolbar = VMToolbar(self.roseCanvas)

#initialize the plot areas
        self.plotaxes2 = self.roseFigure.add_axes([0.01, 0.01, 0.98, 0.98], clip_on='True',xlim=(-1.2,1.2), ylim=(-1.15,1.15), adjustable='box',autoscale_on='False',label='rose')
        self.plotaxes2.set_axis_off()
        self.plotaxes2.set_aspect(aspect='equal', adjustable=None, anchor='W')

#create the variables for color, or else the dialog crashes if one doesn't choose the colors
        self.fcolor = '#4D4D4D'#'#000000'
        self.lcolor = '#000000'
        self.mcolor = '#4D4D4D'
        self.fontSize = 'x-small'

#define the controls
        txt2 = wx.StaticText(self.left_panel, -1, 'Rose data')
        txtp = wx.StaticText(self.left_panel, -1, '(planes)')
        self.rbddir = wx.RadioButton(self.left_panel, -1, 'DipDir', style=wx.RB_GROUP)
        self.rbstrk = wx.RadioButton(self.left_panel, -1, 'Strike')
        txtl = wx.StaticText(self.left_panel, -1, '(lines)')
        self.rbtrd = wx.RadioButton(self.left_panel, -1, 'Trend')
        self.rbddir.SetValue(True)

        txt = wx.StaticText(self.left_panel, -1, 'Rose type')
        self.rb360 = wx.RadioButton(self.left_panel, -1, '360 deg', style=wx.RB_GROUP)
        self.rb180 = wx.RadioButton(self.left_panel, -1, '180 deg')
        self.rb360.SetValue(True)
        
        txt5 = wx.StaticText(self.left_panel, -1, 'Weighting')
        self.rbfreq = wx.RadioButton(self.left_panel, -1, 'Frequency', style=wx.RB_GROUP)
        self.rbwgt = wx.RadioButton(self.left_panel, -1, 'Weighted')#'Length/Dip')
        self.rbfreq.SetValue(True)

        grid1 = wx.GridSizer(12, 1)
        grid1.Add(txt2,0, wx.LEFT, 5)
        grid1.Add(txtp,0, wx.LEFT, 5)
        grid1.Add(self.rbddir,0, wx.LEFT, 5)
        grid1.Add(self.rbstrk,0, wx.LEFT, 5)
        grid1.Add(txtl,0, wx.LEFT, 5)
        grid1.Add(self.rbtrd,0, wx.LEFT, 5)
        
        grid1.Add(txt,0, wx.LEFT|wx.TOP, 5)
        grid1.Add(self.rb360,0, wx.LEFT, 5)
        grid1.Add(self.rb180,0, wx.LEFT, 5)
        
        grid1.Add(txt5,0, wx.LEFT|wx.TOP, 5)
        grid1.Add(self.rbfreq,0, wx.LEFT, 5)
        grid1.Add(self.rbwgt,0, wx.LEFT, 5)
        
        txt1 = wx.StaticText(self.left_panel, -1, 'Interval (deg)')
        self.spin = FS.FloatSpin(self.left_panel, -1, size=(60, -1), value=10, min_val=1, max_val=90, increment=1, digits=0)

        txt4 = wx.StaticText(self.left_panel, -1, 'Outer limit (%)')
        self.spin2 = FS.FloatSpin(self.left_panel, -1, size=(60, -1), value=10, min_val=1, max_val=100, increment=0.5, digits=1)

        txt5 = wx.StaticText(self.left_panel, -1, 'Inner rings (%)')
        self.spin3 = FS.FloatSpin(self.left_panel, -1, size=(60, -1), value=2.5, min_val=0.5, max_val=100, increment=0.5, digits=1)

        txt6 = wx.StaticText(self.left_panel, -1, 'Diagonals (deg)')
        self.spin4 = FS.FloatSpin(self.left_panel, -1, size=(60, -1), value=22.5, min_val=0.5, max_val=90, increment=0.5, digits=1)

        txt2 = wx.StaticText(self.left_panel, -1, 'Fill Colour')
        self.fcbtn = csel.ColourSelect(self.left_panel, pos=(0, 0), size=(60, 20))
        self.fcbtn.SetColour(self.fcolor)

        txt3 = wx.StaticText(self.left_panel, -1, 'Outline Colour')
        self.lcbtn = csel.ColourSelect(self.left_panel, pos=(0, 0), size=(60, 20))
        self.lcbtn.SetColour(self.lcolor)
        
#        txt11 = wx.StaticText(self.left_panel, -1, 'Font Size')
#        self.fontSizeCombo = wx.ComboBox(self.left_panel, -1, value=fonts[fonts.index(self.fontSize)], choices=fonts, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(80, -1))
#        self.fontSizeCombo.SetSelection(fonts.index(self.fontSize))
        
        self.cb_mean = wx.CheckBox(self.left_panel, -1, 'Show Mean')
        self.cb_mean.SetValue(True)

        txt8 = wx.StaticText(self.left_panel, -1, 'Line Colour')
        self.mcbtn = csel.ColourSelect(self.left_panel, pos=(0, 0), size=(60, 20))
        self.mcbtn.SetColour(self.mcolor)

        txt9 = wx.StaticText(self.left_panel, -1, 'Line Width')
        self.spin5 = FS.FloatSpin(self.left_panel, -1, size=(60, -1), value=1.5, min_val=0.5, max_val=10, increment=0.5, digits=1)


        grid2 = wx.FlexGridSizer(18, 1, 2, 2)
        grid2.Add(txt1,0, wx.LEFT|wx.TOP, 5)
        grid2.Add(self.spin,0, wx.LEFT, 5) # petal interval

        grid2.Add(txt4,0, wx.LEFT|wx.TOP, 5)
        grid2.Add(self.spin2,0, wx.LEFT, 5) # outer circle

        grid2.Add(txt5,0, wx.LEFT|wx.TOP, 5)
        grid2.Add(self.spin3,0, wx.LEFT, 5) # inner circles

        grid2.Add(txt6,0, wx.LEFT|wx.TOP, 5)
        grid2.Add(self.spin4,0, wx.LEFT, 5) # diagonal lines

        grid2.Add(txt2,0, wx.LEFT|wx.TOP, 5)
        grid2.Add(self.fcbtn,0, wx.LEFT, 5) # fill colour

        grid2.Add(txt3,0, wx.LEFT|wx.TOP, 5)
        grid2.Add(self.lcbtn,0, wx.LEFT, 5) # line colour
        
#        grid2.Add(txt11,0, wx.LEFT|wx.TOP, 5)
#        grid2.Add(self.fontSizeCombo,0, wx.LEFT, 5) # font size

        grid2.Add((2,2),0, wx.TOP, 20)
        grid2.Add(self.cb_mean,0, wx.LEFT|wx.TOP, 5) # Show Mean

        grid2.Add(txt8,0, wx.LEFT|wx.TOP, 5)
        grid2.Add(self.mcbtn,0, wx.LEFT, 5) # mean line colour

        grid2.Add(txt9,0, wx.LEFT|wx.TOP, 5)
        grid2.Add(self.spin5,0, wx.LEFT, 5) # petal interval


# create draw/clear buttons 
        self.drawButton = wx.Button(self.right_panel, -1, 'Plot', size=(60, 30))
        self.clearButton = wx.Button(self.right_panel, -1, 'Clear', size=(60, 30))
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(self.drawButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,3)
        hbox2.Add(self.clearButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,3)
        hbox2.Add(self.toolbar, 1, wx.EXPAND|wx.ALL, 1)

#bind buttons to events
        self.Bind(wx.EVT_BUTTON, self.onDrawRose, self.drawButton)
        self.Bind(wx.EVT_BUTTON, self.onClearRose, self.clearButton)
        self.fcbtn.Bind(csel.EVT_COLOURSELECT, self.chooseFColor)
        self.lcbtn.Bind(csel.EVT_COLOURSELECT, self.chooseLColor)
        self.mcbtn.Bind(csel.EVT_COLOURSELECT, self.chooseMColor)
#        self.Bind(wx.EVT_COMBOBOX, self.chooseFontSize, self.fontSizeCombo )


#layout of widgets, left panel
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(grid1, 0, wx.ALL, 5)
        vbox.Add(grid2, 0, wx.ALL, 5)
        self.left_panel.SetSizer(vbox)

#layout of canvas, right panel
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(self.roseCanvas, 1, wx.EXPAND)#|wx.SHAPED
        vbox2.Add(hbox2, 0, wx.EXPAND|wx.ALL, 1)
        self.right_panel.SetSizer(vbox2)

        splitter.SplitVertically(self.left_panel,self.right_panel,135) 
        panelsizer.Add(splitter,1, wx.EXPAND|wx.ALL, 2) # the panels are inside this sizer with 2px border

        self.SetSizer(panelsizer)
#        panelsizer.Fit(self)

#        self.mainframe.sb.SetStatusText('Plots rose diagrams for selected file (linear data)')


#retrieve data from pubsub
        pub.subscribe(self.__onReceivePlanarData, 'object.Plan_added_DDD') # from MainForm
        pub.subscribe(self.__onReceivePlanarData, 'object.Plan_added_RH') # from MainForm
        pub.subscribe(self.__onReceiveFaultData, 'object.Fault_added') # from MainForm
        pub.subscribe(self.__onReceiveLinearData, 'object.Lin_added') # from MainForm
        pub.subscribe(self.__onReceiveFontSize, 'object.FontSize') # from MainForm

        pub.subscribe(self.__onReceiveSelection, 'object.selected') # from TreePanel
        pub.subscribe(self.__onReceiveNameSel, 'object.selected_vals') # from TreePanel


# which file is selected
    def __onReceiveSelection(self, message):
        self.file_i = message.data

# font size
    def __onReceiveFontSize(self, message):
        self.fontSize = message.data

# planar data file(s) opened
    def __onReceivePlanarData(self, message): 

        try:
            len(self.Pname) # dummy action just to see if self.Pname exists
        except:
            self.Ptype=[]
            self.Pname=[]
            self.Pndata=[]
            self.Pazim=[]
            self.Pstrike=[]
            self.Pdip=[]
            self.Pidx = []

        for i in range(len(message.data)):
            self.Ptype.append(message.data[i][0])       # filetype
            self.Pname.append(message.data[i][1])       # filename
            self.Pndata.append(message.data[i][2])      # n_data
            self.Pazim.append(message.data[i][3])       # azim
            self.Pdip.append(message.data[i][4])        # dip
            self.Pstrike.append(message.data[i][5])     # strike
            self.Pidx.append(message.data[i][7])        # index (DD or RH)


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

        for i in range(len(message.data)):
            self.Ltype.append(message.data[i][0])
            self.Lname.append(message.data[i][1])
            self.Lndata.append(message.data[i][2])
            self.Lazim.append(message.data[i][3])
            self.Ldip.append(message.data[i][4])

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
            self.Ftrend=[]
            self.Fplunge=[]
            self.Fsense=[]
            self.FidxList=[]

        for i in range(len(message.data)):
            self.Ftype.append(message.data[i][0])       # filetype
            self.Fname.append(message.data[i][1])       # filename
            self.Fndata.append(message.data[i][2])      # n_data
            self.Fazim.append(message.data[i][3])       # dipdir
            self.Fdip.append(message.data[i][4])        # dip
            self.Fstrike.append(message.data[i][5])     # strike
            self.Ftrend.append(message.data[i][7])      # trend
            self.Fplunge.append(message.data[i][8])     # plunge
            self.Fsense.append(message.data[i][9])      # sense
            self.FidxList.append(message.data[i][10])   # F_idx


# which kind of file is selected
    def __onReceiveNameSel(self, message):
        self.name = message.data["itemName"]
        self.nametype = message.data["dtype"]

#choose fill color dialog. Get color datas as hex, for matplotlib
    def chooseFColor(self,event):
        """Colour dialog for Fill colour"""
        self.fcolor = self.fcbtn.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)        
       
#choose line color dialog
    def chooseLColor(self,event):
        """Colour dialog for Line colour"""
        self.lcolor = self.lcbtn.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)

#choose mean line color dialog
    def chooseMColor(self,event):
        """Colour dialog for Line colour"""
        self.mcolor = self.mcbtn.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)        
        
##choose font size
#    def chooseFontSize(self,event):
#        """Choose font size for texts"""
#        fsize = self.fontSizeCombo.GetValue()
#        self.fontSize = fonts[fonts.index(fsize)]
#        
        
#draws the rose diagram according to the user's options
    def onClearRose(self,event):
        """ Rose Diagram Options """
#        self.roseFigure.clf()
        self.plotaxes2.cla()
        self.plotaxes2.set_axis_off()
        self.roseCanvas.draw()

#draws the rose diagram according to the user's options
    def onDrawRose(self,event):
        """ Rose Diagram Options """

        try: # the 'except' for this 'try' is about 200 lines ahead!
            
            i = self.file_i

            ddirRb = self.rbddir.GetValue()
            strkRb = self.rbstrk.GetValue()
            trndRb = self.rbtrd.GetValue()
            r360 = self.rb360.GetValue()
            r180 = self.rb180.GetValue()
            frequency = self.rbfreq.GetValue()
            weighted = self.rbwgt.GetValue()
            petal = self.spin.GetValue()
            outer_circ = self.spin2.GetValue()
            inner_rings = self.spin3.GetValue()
            diagonals = self.spin4.GetValue()
            fillcolor = self.fcolor
            edgecolor = self.lcolor
            
            fontsize = self.fontSize

            showMean = self.cb_mean.GetValue()
            meancolor = self.mcolor
            meanwidth = self.spin5.GetValue()

            ring_steps = inner_rings / float(outer_circ)
            grid_col = 'grey'
            grid_width = 0.5

            self.plotaxes2.cla()
            axes = self.plotaxes2
            self.plotaxes2.set_axis_off()

            # create empty lists
            Azimuth = []
            Dip = []
            ddir = []
            dp = []
            strk = []
            trd = []
            plng = []
                
            # what kind of data was selected
            if self.nametype == 1:  # 1 == itemPlanar
                ddir = self.Pazim[i]
                dp = self.Pdip[i]
                strk = self.Pstrike[i]
                if self.Pidx[i].startswith('D'): # dip-dir data
                    name = '[P(dd)] %s' % self.Pname[i]
                else: # right-hand data
                    name = '[P(rh)] %s' % self.Pname[i]
            elif self.nametype == 2: # 2 == itemLinear
                trd = self.Lazim[i]
                plng = self.Ldip[i]
                name = '[L] %s' % self.Lname[i]
            elif self.nametype == 4: # 2 == itemFault
                ddir = self.Fazim[i]
                dp = self.Fdip[i]
                strk = self.Fstrike[i]
                trd = self.Ftrend[i]
                plng = self.Fplunge[i]
                name = '[F] %s' % self.Fname[i]
            else:
                pass
                
             # check if DipDir or Strike or Trend
            if ddirRb:
                #~ print 'ddier'
                Azimuth = ddir
                Dip = dp
            elif strkRb:
                #~ print 'strike'
                Azimuth = strk
                Dip = dp
            elif trndRb:
                #~ print 'trend'
                Azimuth = trd
                Dip = plng
                
            # nothing selected or wrong kind of data choosen
            if Azimuth == []: 
                raise AttributeError

    # convert azimuth to modulo 180 or modulo 360
            azimMod = [] 
            if r180: #test if 180deg rose was selected
                for az in Azimuth:
                    if 90.0 < az <= 180.0:
                        azimMod.append(az + 180.0)
                    elif 180.0 <= az <= 270.0:
                        azimMod.append(az - 180.0)
                    else:
                        azimMod.append(az)
            else:
                azimMod = Azimuth
                            
    # calculate mean direction and circular standar deviation
    # from Fisher 1993, Statistical Analyis of circular data, p.32-33
            ndata = len(azimMod)
            cosTheta = [np.cos(np.radians(az)) for az in azimMod]
            sinTheta = [np.sin(np.radians(az)) for az in azimMod]
            C = np.sum(cosTheta)
            S = np.sum(sinTheta)
            R = np.sqrt(C*C + S*S)
            Rbar = R / ndata
            V = 1.0 - Rbar

            ThetaBar = np.arctan2(C,S)
            ThetaBarDeg = np.degrees(ThetaBar)

            if 0.0 <= ThetaBarDeg < 90.0:
                ThetaBarDeg = -(ThetaBarDeg - 90.0)
            elif 90.0 <= ThetaBarDeg <= 180.0:
                ThetaBarDeg = 540.0 + (-ThetaBarDeg - 90.0)
            else:
                ThetaBarDeg = -ThetaBarDeg + 90.0

    # assuming a unimodal Von Mises distribution..
    # from Fisher 1993, Statistical Analyis of circular data, p.88-89

    # if data does not follows a unimodal distribution (or has only one value), skip

            plotConfidence = True
            try:
                if Rbar < 0.53:
                    khatml = 2.0 * Rbar + (Rbar **3.0) + (5 * (Rbar **5.0) / 6.0) 
                elif 0.53 <= Rbar <= 0.85:
                    khatml = -0.4 + 1.39 * Rbar + 0.43/V
                else: # Rbar > 0.85:
                    khatml = 1.0 / (Rbar **3.0 - 4.0 * (Rbar **2.0) + 3.0 * Rbar)

                if khatml < 2.0:
                    stuff = [khatml - 2.0 * ((ndata*khatml) **-1.0), 0.0]
                    khat = np.max(stuff)
                else: #khat_ml => 2
                    khat = ((ndata-1.0) **3.0) * khatml / (ndata **3.0 + ndata)

                sigma_vm = 1.0 / np.sqrt(ndata * Rbar * khat)
                confidenceUp = np.degrees(ThetaBar + np.arcsin(1.9604 * sigma_vm))
                confidenceDw = np.degrees(ThetaBar - np.arcsin(1.9604 * sigma_vm))
                confidence = np.degrees(np.arcsin(1.9604 * sigma_vm))
            except:
                plotConfidence = False
                pass
                
            if np.isnan(confidence):
                plotConfidence = False
                

    # convert azimuths from compass to polar
            azimPolar = [] 
            for az in azimMod:
                ang = 360.0 - az + 90.0
                if ang >= 360.0:
                    ang = ang - 360.0
                azimPolar.append(ang)

    # bins for the histogram
            nbins = np.arange(0.,360.1,petal)
            
    # test if weighted rose diagram was selected
            if weighted: 
                rose_hist = np.histogram(azimPolar,nbins,weights=Dip)#,normed=True,new=True)
                weights_sum = sum(Dip)
                petal_perc = [i*100.0/weights_sum for i in rose_hist[0]]
            else:
                rose_hist = np.histogram(azimPolar,nbins)#,new=True)
                petal_perc = [i*100.0/len(azimPolar) for i in rose_hist[0]]

            petal_mid = [i + petal/2 for i in nbins]
            petal_dens = [i/outer_circ for i in petal_perc]
            petal_max = max(petal_dens)*outer_circ

    # draws the petals
            for j in range(len(petal_dens)):

                x = []
                y = []
                    #define limits of petal
                start = np.radians(petal_mid[j] + petal/2)
                stop = np.radians(petal_mid[j] - petal/2)
        
                    #start drawing the petals (triangles: x0,y0 -> x2,y2 -> x3,y3 -> x0,y0)
                x.append(0)
                y.append(0)
        
                x2 = petal_dens[j] * np.cos(start)
                y2 = petal_dens[j] * np.sin(start)
        
                x.append(x2)
                y.append(y2)
        
                x3 = petal_dens[j] * np.cos(stop)
                y3 = petal_dens[j] * np.sin(stop)
        
                x.append(x3)
                y.append(y3)
                x.append(0)
                y.append(0)

                xy = np.array( [ x, y ] ) #convert lists to numpy array
                xy2 = xy.transpose() # transpose array from shape (2,4) to shape (4,2)
        
                l_petal = Polygon(xy2,fc=fillcolor,ec=edgecolor)

                axes.add_patch(l_petal)
        
    # draws the circle (or half-circle), and adds decorations (tick marks, rings, etc)
            if r360: #full-circle rose

                x_cross = [0,1,0,-1,0]
                y_cross = [0,0,1,0,-1]
                axes.plot(x_cross,y_cross,'k+',markersize=8)
                circ = Circle((0,0), radius=1, edgecolor='black', facecolor='none', clip_box='None', zorder=0)
                axes.add_patch(circ)
                axes.text(0.01,1.025,'N',family='sans-serif',size=fontsize,horizontalalignment='center' )
                axes.text(1.05,0,'%d %%' % outer_circ,family='sans-serif',size=fontsize,verticalalignment='center' )
                axes.text(-1.05,0,'%d %%' % outer_circ,family='sans-serif',size=fontsize,verticalalignment='center', horizontalalignment='right' )

                for i in np.arange(0.0,1.0,ring_steps):
                    ring = Circle ((0,0), radius=i, fc='none', ec=grid_col, lw=grid_width, zorder=0)
                    axes.add_patch(ring)

                for i in np.arange(0.0,90.0,diagonals):
                    diag = Line2D((np.sin(np.radians(i)),np.sin(np.radians(i + 180))), (np.cos(np.radians(i)),np.cos(np.radians(i + 180))),c=grid_col,lw=grid_width,zorder=0)
                    axes.add_line(diag)

                for i in np.arange(90.0,180.0,diagonals):
                    diag = Line2D((np.sin(np.radians(i)),np.sin(np.radians(i + 180))), (np.cos(np.radians(i)),np.cos(np.radians(i + 180))),c=grid_col,lw=grid_width,zorder=0)
                    axes.add_line(diag)

            # some texts..
                axes.text(-1.22,0.95,'%s' % self.Name,family='sans-serif',size=fontsize,horizontalalignment='left' )
                axes.text(-1.22,0.85,'n = %d' % len(azimPolar),family='sans-serif',size=fontsize,horizontalalignment='left' )
                axes.text(-1.22,0.77,'max = %.2f %%' % petal_max,family='sans-serif',size=fontsize,horizontalalignment='left' )
                if weighted:
                    axes.text(-1.22,0.67,'(weighted)',family='sans-serif',size=fontsize,horizontalalignment='left' )
                else:
                    axes.text(-1.22,0.67,'(frequency)',family='sans-serif',size=fontsize,horizontalalignment='left' )

                axes.text(0.7,0.95,u'Mean dir.: %3.1f°' % ThetaBarDeg,family='sans-serif',size=fontsize,horizontalalignment='left' )
                if plotConfidence:
                    axes.text(0.7,0.87,u'95 %% conf.: ± %3.1f°' % confidence,family='sans-serif',size=fontsize,horizontalalignment='left' )


            # marks for means direction and confidence interval
                if showMean:
                    if plotConfidence:
                        confcirc = Arc((0,0), width=2.08, height=2.08, angle=0.0, theta1=confidenceDw, theta2=confidenceUp, ec=meancolor, lw=meanwidth, fill=None, zorder=0)
                        axes.add_patch(confcirc)

                    x0 = np.cos(ThetaBar) + np.cos(ThetaBar)*0.11
                    x1 = np.cos(ThetaBar) + np.cos(ThetaBar)*0.065
                    y0 = np.sin(ThetaBar) + np.sin(ThetaBar)*0.11
                    y1 = np.sin(ThetaBar) + np.sin(ThetaBar)*0.065
                    lin = Line2D((x0,x1),(y0,y1), lw=meanwidth, c=meancolor)
                    axes.add_line(lin)

                self.plotaxes2.set_xlim(-1.3,1.3)
                self.plotaxes2.set_ylim(-1.15,1.15)
            
                self.roseCanvas.draw()

            else: #half-circle rose

                x_cross = [0,1,0,-1]
                y_cross = [0,0,1,0]
                axes.plot(x_cross,y_cross,'k+',markersize=8)
                circ = Arc((0,0), width=2, height=2, angle=0.0, theta1=0.0, theta2=180.0, ec=None, fill=None, zorder=0)
                axes.add_patch(circ)
                axes.text(0.01,1.025,'N',family='sans-serif',size=fontsize,horizontalalignment='center' )
                axes.text(1.05,0,'%d %%' % outer_circ,family='sans-serif',size=fontsize,verticalalignment='center' )
                axes.text(-1.05,0,'%d %%' % outer_circ,family='sans-serif',size=fontsize,verticalalignment='center', horizontalalignment='right' )

                for i in np.arange(0.0,1.0,ring_steps):
                    ring = Arc((0,0), width=i*2, height=i*2, angle=0.0, theta1=0.0, theta2=180.0, ec=grid_col, fill=None, lw=grid_width, zorder=0)
                    axes.add_patch(ring)

                for i in np.arange(0.0,90.1,diagonals):
                    diag = Line2D((0,np.sin(np.radians(i))), (0,np.cos(np.radians(i))),c=grid_col,lw=grid_width,zorder=0)
                    axes.add_line(diag)

                for i in np.arange(270.0,360.0,diagonals):
                    diag = Line2D((0,np.sin(np.radians(i))), (0,np.cos(np.radians(i))),c=grid_col,lw=grid_width,zorder=0)
                    axes.add_line(diag)

            # some texts..
                axes.text(-1.22,0.95,'%s' % self.Name,family='sans-serif',size=fontsize,horizontalalignment='left' )
                axes.text(-1.22,0.85,'n = %d' % len(azimPolar),family='sans-serif',size=fontsize,horizontalalignment='left' )
                axes.text(-1.22,0.77,'max = %.2f %%' % petal_max,family='sans-serif',size=fontsize,horizontalalignment='left' )
                if weighted:
                    axes.text(-1.22,0.67,'(weighted)',family='sans-serif',size=fontsize,horizontalalignment='left' )
                else:
                    axes.text(-1.22,0.67,'(frequency)',family='sans-serif',size=fontsize,horizontalalignment='left' )


                axes.text(0.7,0.95,u'Mean dir.: %3.1f°' % ThetaBarDeg,family='sans-serif',size=fontsize,horizontalalignment='left' )
                if plotConfidence:
                    axes.text(0.7,0.87,u'95 %% conf.: ± %3.1f°' % confidence,family='sans-serif',size=fontsize,horizontalalignment='left' )

            # marks for means direction and confidence interval
                if showMean:
                    if plotConfidence:
                        confcirc = Arc((0,0), width=2.08, height=2.08, angle=0.0, theta1=confidenceDw, theta2=confidenceUp, ec=meancolor, lw=meanwidth, fill=None, zorder=0)
                        axes.add_patch(confcirc)

                    x0 = np.cos(ThetaBar) + np.cos(ThetaBar)*0.11
                    x1 = np.cos(ThetaBar) + np.cos(ThetaBar)*0.065
                    y0 = np.sin(ThetaBar) + np.sin(ThetaBar)*0.11
                    y1 = np.sin(ThetaBar) + np.sin(ThetaBar)*0.065
                    lin = Line2D((x0,x1),(y0,y1), lw=meanwidth, c=meancolor)
                    axes.add_line(lin)


                self.plotaxes2.set_xlim(-1.3,1.3)
                self.plotaxes2.set_ylim(-0.05,1.15)
            
                self.roseCanvas.draw()

            self.mainframe.sb.SetStatusText('Rose diagram plotted with petals of %d degrees' % petal)

#~ # this is from the 'try' right after 'def DrawRose'
        except AttributeError:
            dlg = wx.MessageDialog(None, 'No file(s) selected (highlighted).\n\nOr maybe you are trying to make a diagram\nfor the wrong kind of data (like "trend" for planar data)', 'Oooops!', wx.OK|wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            pass


