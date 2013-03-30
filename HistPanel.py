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


import numpy as np


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


class HistPanel(wx.Panel):
    """class for the histogram page of the notebook """
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
        self.histFigure = Figure(figsize=(4,4),facecolor='white')
        self.histCanvas = FigureCanvas(self.right_panel, -1, self.histFigure)
        self.toolbar = VMToolbar(self.histCanvas)

#initialize the plot area
        self.axes = self.histFigure.add_axes([0.1, 0.1, 0.8, 0.8], clip_on='True', adjustable='box',autoscale_on='True',label='hist')
        self.axes.set_axis_off()

#create the variables for color and etc, or else the dialog crashes if one doesn't choose the colors
        self.fcolor = '#A52A2A'
        self.lcolor = '#000000'
        self.fontSize = 'x-small'

#define the controls
        txt = wx.StaticText(self.left_panel, -1, _('Histogram data'))
        txtp = wx.StaticText(self.left_panel, -1, _('(planes)'))
        self.rb1 = wx.RadioButton(self.left_panel, -1, _('Dip Dir.'), style=wx.RB_GROUP)
        self.rb3 = wx.RadioButton(self.left_panel, -1, _('Strike'))
        self.rb2 = wx.RadioButton(self.left_panel, -1, _('Dip'))
        txtl = wx.StaticText(self.left_panel, -1, _('(lines)'))
        self.rb4 = wx.RadioButton(self.left_panel, -1, _('Trend'))
        self.rb5 = wx.RadioButton(self.left_panel, -1, _('Plunge'))
        self.rb1.SetValue(True)



        grid1 = wx.GridSizer(8, 1)
        grid1.Add(txt,0, wx.LEFT, 5)
        grid1.Add(txtp,0, wx.LEFT|wx.TOP, 5)
        grid1.Add(self.rb1,0, wx.LEFT, 5)
        grid1.Add(self.rb3,0, wx.LEFT, 5)
        grid1.Add(self.rb2,0, wx.LEFT, 5)
        grid1.Add(txtl,0, wx.LEFT|wx.TOP, 5)
        grid1.Add(self.rb4,0, wx.LEFT, 5)
        grid1.Add(self.rb5,0, wx.LEFT, 5)
        
        txt1 = wx.StaticText(self.left_panel, -1, _('Interval (deg)'))
        self.spin = FS.FloatSpin(self.left_panel, -1, size=(60, -1), value=10, min_val=1, max_val=90, increment=1, digits=0)

        txt2 = wx.StaticText(self.left_panel, -1, _('Fill Colour'))
        self.fcbtn = csel.ColourSelect(self.left_panel, pos=(0, 0), size=(60, 20))
        self.fcbtn.SetColour(self.fcolor)

        txt3 = wx.StaticText(self.left_panel, -1, _('Outline Colour'))
        self.lcbtn = csel.ColourSelect(self.left_panel, pos=(0, 0), size=(60, 20))
        self.lcbtn.SetColour(self.lcolor)

        self.cb_norm = wx.CheckBox(self.left_panel, -1, _('Normed'))
        self.cb_norm.SetValue(False)


        grid2 = wx.FlexGridSizer(8, 1, 2, 2)
        grid2.Add(txt1,0, wx.LEFT|wx.TOP, 5)
        grid2.Add(self.spin,0, wx.LEFT, 5) # bins

        grid2.Add(txt2,0, wx.LEFT|wx.TOP, 5)
        grid2.Add(self.fcbtn,0, wx.LEFT, 5) # fill colour

        grid2.Add(txt3,0, wx.LEFT|wx.TOP, 5)
        grid2.Add(self.lcbtn,0, wx.LEFT, 5) # line colour

        grid2.Add((2,2),0, wx.TOP, 20)
        grid2.Add(self.cb_norm,0, wx.LEFT|wx.TOP, 5) # Normed


# create draw/clear buttons 
        self.drawButton = wx.Button(self.right_panel, -1, _('Plot'), size=(60, 30))
        self.clearButton = wx.Button(self.right_panel, -1, _('Clear'), size=(60, 30))
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(self.drawButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,3)
        hbox2.Add(self.clearButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,3)
        hbox2.Add(self.toolbar, 1, wx.EXPAND|wx.ALL, 1)

#bind buttons to events
        self.Bind(wx.EVT_BUTTON, self.onDrawHist, self.drawButton)
        self.Bind(wx.EVT_BUTTON, self.onClearHist, self.clearButton)
        self.fcbtn.Bind(csel.EVT_COLOURSELECT, self.chooseFColor)
        self.lcbtn.Bind(csel.EVT_COLOURSELECT, self.chooseLColor)

#layout of widgets, left panel
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(grid1, 0, wx.ALL, 5)
        vbox.Add(grid2, 0, wx.ALL, 5)
        self.left_panel.SetSizer(vbox)

#layout of canvas, right panel
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(self.histCanvas, 1, wx.EXPAND)#|wx.SHAPED
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


# which kind of file is selected
    def __onReceiveNameSel(self, message):
        self.name = message.data["itemName"]
        self.nametype = message.data["dtype"]


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
#            self.PeigenList=[]
            self.PidxList=[]
#            self.PProps=[]

        for i in range(len(message.data)):
            self.Ptype.append(message.data[i][0])       # filetype
            self.Pname.append(message.data[i][1])       # filename
            self.Pndata.append(message.data[i][2])      # n_data
            self.Pazim.append(message.data[i][3])       # azim
            self.Pdip.append(message.data[i][4])        # dip
            self.Pstrike.append(message.data[i][5])     # strike
#            self.PeigenList.append(message.data[i][6])  # eigenList
            self.PidxList.append(message.data[i][7])    # DDD_idx
#            self.PProps.append(message.data[i][8])      # pplist


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
#            self.LeigenList=[]
            self.LidxList=[]
#            self.LProps=[]

        for i in range(len(message.data)):
            self.Ltype.append(message.data[i][0])       # filetype
            self.Lname.append(message.data[i][1])       # filename
            self.Lndata.append(message.data[i][2])      # n_data
            self.Lazim.append(message.data[i][3])       # azim
            self.Ldip.append(message.data[i][4])        # dip
            self.Lstrike.append(message.data[i][5])     # strike
#            self.LeigenList.append(message.data[i][6])  # eigenList
            self.LidxList.append(message.data[i][7])    # Lin_idx
#            self.LProps.append(message.data[i][8])      # lplist




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
#            self.FeigenList=[]
            self.Ftrend=[]
            self.Fplunge=[]
            self.Fsense=[]
            self.FidxList=[]
#            self.FProps=[]

        for i in range(len(message.data)):
            self.Ftype.append(message.data[i][0])       # filetype
            self.Fname.append(message.data[i][1])       # filename
            self.Fndata.append(message.data[i][2])      # n_data
            self.Fazim.append(message.data[i][3])       # dipdir
            self.Fdip.append(message.data[i][4])        # dip
            self.Fstrike.append(message.data[i][5])     # strike
#            self.FeigenList.append(message.data[i][6])  # eigenList
            self.Ftrend.append(message.data[i][7])      # trend
            self.Fplunge.append(message.data[i][8])     # plunge
            self.Fsense.append(message.data[i][9])      # sense
            self.FidxList.append(message.data[i][10])   # F_idx
#            self.FProps.append(message.data[i][11])     # fplist - default properties set in MainForm.py



#choose fill color dialog. Get color datas as hex, for matplotlib
    def chooseFColor(self,event):
        """Colour dialog for Fill colour"""
        self.fcolor = self.fcbtn.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)        
       
#choose line color dialog
    def chooseLColor(self,event):
        """Colour dialog for Line colour"""
        self.lcolor = self.lcbtn.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)


# clear the plot area
    def onClearHist(self,event):
        self.axes.cla()
        self.axes.set_axis_off()
        self.histCanvas.draw()

#draws the histogram according to the user's options
    def onDrawHist(self,event):
        """ Draw Histogram """

        try: # 
            i = self.file_i

            dipdir = self.rb1.GetValue() # plot histogram of DipDirection
            strike = self.rb3.GetValue() # plot histogram of Strike
            dip = self.rb2.GetValue() # plot histogram of Dip
            trend = self.rb4.GetValue() # plot histogram of Trend
            plunge = self.rb5.GetValue() # plot histogram of Plunge

            # bins for the histogram
            petal = self.spin.GetValue()

            fillcolor = self.fcolor
            edgecolor = self.lcolor

            normed = self.cb_norm.GetValue()


            if self.nametype == 1:  # 1 == itemPlanar
                ddir = self.Pazim[i]
                dp = self.Pdip[i]
                strk = self.Pstrike[i]
            elif self.nametype == 2: # 2 == itemLinear
                trd = self.Lazim[i]
                plng = self.Ldip[i]
            elif self.nametype == 4: # 2 == itemFault
                ddir = self.Fazim[i]
                dp = self.Fdip[i]
                strk = self.Fstrike[i]
                trd = self.Ftrend[i]
                plng = self.Fplunge[i]
            else:
                pass

            # what should be plotted
            if dipdir:
                histdata = ddir
                nbins = np.arange(0.,360.1,petal)
                xmax=360
                title = _('Dip Direction %s') % self.name
            elif strike:
                histdata = strk
                nbins = np.arange(0.,360.1,petal)
                xmax=360
                title = _('Strike %s') % self.name
            elif dip:
                histdata = dp
                nbins = np.arange(0.,90.1,petal)
                xmax=90
                title = _('Dip %s') % self.name
            elif trend:
                histdata = trd
                nbins = np.arange(0.,360.1,petal)
                xmax=360
                title = _('Trend %s') % self.name
            elif plunge:
                histdata = plng
                nbins = np.arange(0.,90.1,petal)
                xmax=90
                title = _('Plunge %s') % self.name


            nph = np.histogram(histdata, bins=nbins, normed=normed)
            ymax = np.max(nph[0])

            self.axes.cla()
            self.axes.hist(histdata, bins=nbins, normed=normed, ec=edgecolor, fc=fillcolor)
            self.axes.text(xmax/2.0,ymax+((2*ymax)/100.0),title ,family='sans-serif',size=self.fontSize,horizontalalignment='center')
            self.axes.axis([0, xmax, 0, ymax])
            self.histCanvas.draw()


            self.mainframe.sb.SetStatusText(_('Histogram created for %s') % title)

# this is from the 'try' right after 'def DrawHist'
        except (AttributeError, UnboundLocalError):
#            self.histFigure.clf()
            self.axes.cla()
            self.axes.set_axis_off()
            self.histCanvas.draw()
            dlg = wx.MessageDialog(None, _('No file(s) selected (highlighted).\n\nOr maybe you are trying to make an histogram\nfor the wrong kind of data (like "trend" for planar data)'), _('Oooops!'), wx.OK|wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            pass


