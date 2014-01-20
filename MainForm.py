#!/usr/bin/env python

#==============================================================================#
#        OpenStereo - Open-source, Multiplatform Stereonet Analysis            #
#                                                                              #
#    Copyright (c)  2009-2011 Carlos H. Grohmann & Ginaldo A.C. Campanha.      #
#    Copyright (c)  2012-2014 Matteo Pasotti <matteo.pasotti@gmail.com>        #
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
#  Extended by:  Matteo Pasotti                                                #
#                Italy                                                         #
#                https://github.com/xquiet/openstereo                          #
#                                                                              #
#      Requirements:                                                           #
#         Python version 2.4 or higher                                         #
#         wxPython version 2.8.10 or higher                                    #
#         Matplotlib version 0.98 or higher                                    #
#         NumPy version 1.1 or higher                                          #
#         gettext                                                              #
#==============================================================================#

"""
OpenStereoNet - Open-source, Multiplatform Stereonet Analysis

"""

import os, sys, csv
import wx

from wx.lib.pubsub import Publisher as pub
import types as types
#import numpy as np
from wx.lib.wordwrap import wordwrap

# import i18n
import i18n
_ = i18n.language.ugettext #use ugettext instead of getttext to avoid unicode errors

# import matplotlib
# this sets to use wxagg instead of pyQt
import matplotlib as mpl
mpl.use('WXAgg')
#mpl.rcParams['backend'] = 'WXAgg'
#mpl.rcParams['savefig.extension'] = 'auto'


#local imports
import bitmaps # icons
import DataDefs as datad # open file defs
import RosePanel as rose # rose diagram class
import HistPanel as histo # histogram class
import StatsPanel as statsp # stats panel class
#import GridPanel as grd # grid panel class
import StereoPanel as stereo # plot stereonet panel class
#import EigenStat as eigen # eigenvectors stats for girdle/cluster analysis
import TreePanel as ctree # tree of files
import ToolsDefs as tools # various tools: merge data, etc

#----------------------------------------------------------------------
class MainFrame(wx.Frame):
    """ OpenStereoNet - Open-source, Multiplatform Stereonet Analysis """
    def __init__(self, parent, ID, title, size):
        wx.Frame.__init__(self, parent, ID, title,(-1,-1),size)
        self.sb = self.CreateStatusBar()

        self.pyversion = 'OpenStereoNet - Open-source, Multiplatform Stereonet Analysis'

        self.OpenStereo_version = '0.1.4' # this is for the 'about' box

        self.currentDirectory = os.getcwd()

#        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow) # for taskbar icon

        # remove matplotlib's fontList.cache, to prevent those Vera.ttf errors (mainly on Windows)
        configdir = mpl.get_configdir()
        listcache = os.path.join(configdir, 'fontList.cache')
        if(os.path.isfile(listcache)):
            os.remove(listcache)



    #get the icons from bitmaps.py
        DD_ico = bitmaps.DD.getBitmap()
        RH_ico = bitmaps.RH.getBitmap()
        L_ico = bitmaps.L.getBitmap()
        F_ico = bitmaps.F.getBitmap()
        SC_ico = bitmaps.SC.getBitmap()

        OStereo_ico = bitmaps.openstereo_icon_noname_32x32x32.getBitmap()

       # create the file menu
        filemenu=wx.Menu()
        menuOpenPlanarDDD = filemenu.Append(-1, _('Open &Planar Data (Dipdir/Dip)\tCtrl+P'), _('Open planar data (Dipdir/Dip)'))
        self.Bind(wx.EVT_MENU, self.OnOpenPlanarDataDDD, menuOpenPlanarDDD)

        menuOpenPlanarRH = filemenu.Append(-1, _('Open Planar Data (&Strike/Dip)\tCtrl+S'), _('Open planar data (Strike/Dip)'))
        self.Bind(wx.EVT_MENU, self.OnOpenPlanarDataRH, menuOpenPlanarRH)

        menuOpenLinear = filemenu.Append(-1, _('Open &Linear Data (Trend/Plunge)\tCtrl+L'), _('Open linear data (Trend/Plunge)'))
        self.Bind(wx.EVT_MENU, self.OnOpenLinearData, menuOpenLinear)

        menuOpenSmall = filemenu.Append(-1, _('Open Small &Circle Data (Trend/Plunge/Radius)\tCtrl+C'), _('Open Small Circle Data (Trend/Plunge/Radius)'))
        self.Bind(wx.EVT_MENU, self.OnOpenSmallData, menuOpenSmall)


        # fault data options submenu
        fault = wx.Menu()

        menuOpenFault = fault.Append(-1, _('Open &Fault Data (Dipdir/Dip // Trend/Plunge // Sense)\tCtrl+F'), _('Open fault data (Dipdir/Dip // Trend/Plunge // Sense)'))
        self.Bind(wx.EVT_MENU, self.OnOpenFaultData, menuOpenFault)

        menuOpenFaultPlanes = fault.Append(-1, _('Open Pla&nes from Fault Data (Dipdir/Dip)\tCtrl+N'), _('Open Planes from Fault Data (Dipdir/Dip)'))
        self.Bind(wx.EVT_MENU, self.OnOpenFaultPlanes, menuOpenFaultPlanes)

        menuOpenFaultLines = fault.Append(-1, _('Open L&ines from Fault Data (Trend/Plunge)\tCtrl+I'), _('Open lines from Fault Data (Trend/Plunge)'))
        self.Bind(wx.EVT_MENU, self.OnOpenFaultLines, menuOpenFaultLines)

        menuOpenFaultTectonicsFP = fault.Append(-1, _('Open &TectonicsFP Fault Data (comma separated)\tCtrl+T'), _('Open TectonicsFP Fault Data'))
        self.Bind(wx.EVT_MENU, self.OnOpenFaultTectonicsFP, menuOpenFaultTectonicsFP)

        menuOpenFaultTTECTO = fault.Append(-1, _('Open T-T&ECTO Fault Data (tab separated)\tCtrl+E'), _('Open T-TECTO Fault Data'))
        self.Bind(wx.EVT_MENU, self.OnOpenFaultTTECTO, menuOpenFaultTTECTO)

        filemenu.AppendMenu(-1, _('F&ault Data'), fault)


        # exit
        menuExit = filemenu.Append(wx.ID_EXIT, _('&Quit'), _('Quit the program'))
        self.Bind(wx.EVT_MENU, self.Exit, menuExit)



    #create the tools menu
        toolsmenu=wx.Menu()
        menuMergeData = toolsmenu.Append(-1, _('&Merge datasets'), _('Merge datasets'))
        self.Bind(wx.EVT_MENU, self.OnMergeData, menuMergeData)

        menuRotateData = toolsmenu.Append(-1, _('&Rotate datasets'), _('Rotate datasets'))
        self.Bind(wx.EVT_MENU, self.OnRotateData, menuRotateData)

        toolsmenu.AppendSeparator()

        # options menu - so far, only font size
        self.opt = wx.Menu()

        id_xxsmall = 1001
        id_xsmall = 1002
        id_small = 1003
        id_medium = 1004
        id_large = 1005
        id_xlarge = 1006
        id_xxlarge = 1007

        fontXXsmall = self.opt.AppendRadioItem(id_xxsmall, 'xx-small', 'xx-small')
        fontXsmall = self.opt.AppendRadioItem(id_xsmall, 'x-small', 'x-small')
        fontSmall = self.opt.AppendRadioItem(id_small, 'small', 'small')
        fontMedium = self.opt.AppendRadioItem(id_medium, 'medium', 'medium')
        fontLarge = self.opt.AppendRadioItem(id_large, 'large', 'large')
        fontXlarge = self.opt.AppendRadioItem(id_xlarge, 'x-large', 'x-large')
        fontXXlarge = self.opt.AppendRadioItem(id_xxlarge, 'xx-large', 'xx-large')

        self.Bind(wx.EVT_MENU, self.onFontSize, fontXXsmall)
        self.Bind(wx.EVT_MENU, self.onFontSize, fontXsmall)
        self.Bind(wx.EVT_MENU, self.onFontSize, fontSmall)
        self.Bind(wx.EVT_MENU, self.onFontSize, fontMedium)
        self.Bind(wx.EVT_MENU, self.onFontSize, fontLarge)
        self.Bind(wx.EVT_MENU, self.onFontSize, fontXlarge)
        self.Bind(wx.EVT_MENU, self.onFontSize, fontXXlarge)

        toolsmenu.AppendMenu(-1, 'Font Size', self.opt)

        self.opt.Check(id_xsmall, True)
        self.onFontSize(wx.EVT_MENU)



    #create the help menu
        helpmenu=wx.Menu()
        menuAbout = helpmenu.Append(-1, _('&About'), _('About'))
        self.Bind(wx.EVT_MENU, self.onAboutDlg, menuAbout)

    #create the menubar for the frame and add the menu to it
        menuBar=wx.MenuBar()
        menuBar.Append(filemenu, _('&File'))
        menuBar.Append(toolsmenu, _('&Tools'))
        menuBar.Append(helpmenu, _('&Help'))
        self.SetMenuBar(menuBar)

    #create the toolbar for the frame
        toolbar = self.CreateToolBar()
        toolbar.SetToolBitmapSize((16,16))  # sets icon size

        toolbarOpenPlanarDD = toolbar.AddLabelTool(-1, 'Open', DD_ico, wx.NullBitmap, wx.ITEM_NORMAL, _('Open planar data (Dipdir/Dip)'), '')
        toolbarOpenPlanarRH = toolbar.AddLabelTool(-1, 'Open', RH_ico, wx.NullBitmap, wx.ITEM_NORMAL, _('Open planar data (Strike/Dip)'), '')
        toolbarOpenLinear = toolbar.AddLabelTool(-1, 'Open', L_ico, wx.NullBitmap, wx.ITEM_NORMAL, _('Open linear data (Trend/Plunge)'), '')
        toolbarOpenFault = toolbar.AddLabelTool(-1, 'Open', F_ico, wx.NullBitmap, wx.ITEM_NORMAL, _('Open Fault Data (Dipdir/Dip // Trend/Plunge // Sense)'), '')
        toolbarOpenSmall = toolbar.AddLabelTool(-1, 'Open', SC_ico, wx.NullBitmap, wx.ITEM_NORMAL, _('Open Small Circle Data (Trend/Plunge/Radius)'), '')

        self.Bind(wx.EVT_TOOL, self.OnOpenPlanarDataDDD, toolbarOpenPlanarDD)
        self.Bind(wx.EVT_TOOL, self.OnOpenPlanarDataRH, toolbarOpenPlanarRH)
        self.Bind(wx.EVT_TOOL, self.OnOpenLinearData, toolbarOpenLinear)
        self.Bind(wx.EVT_TOOL, self.OnOpenFaultData, toolbarOpenFault)
        self.Bind(wx.EVT_TOOL, self.OnOpenSmallData, toolbarOpenSmall)

        toolbar.AddSeparator()

        toolbar.Realize()

        self.Bind(wx.EVT_SHOW, self.onShow) # plot the stereonet when program starts

    #split the window in two and create panels
        panelsizer = wx.BoxSizer(wx.HORIZONTAL) # sizer
        splitter = wx.SplitterWindow(self, -1)
        self.left_panel = wx.Panel(splitter, -1, style=wx.BORDER_SUNKEN)
        self.right_panel = wx.Panel(splitter, -1, style=wx.BORDER_SUNKEN)
        splitter.SetMinimumPaneSize(175) # cannot shrink panel to less than this

    #layout of widgets, right panel - notebook
        nb = wx.Notebook(self.right_panel)
        self.statsPanel = statsp.StatsPanel(nb) # each page has its own class
        self.stereoPanel = stereo.StereoPanel(nb) # notebook pages as "self" to be acessible from everywhere
        self.rosePanel = rose.RosePanel(nb) # notebook pages as "self" to be acessible from everywhere
        self.histPanel = histo.HistPanel(nb)
#        self.gridPanel = grd.GridPanel(nb)

#        nb.AddPage(self.gridPanel, "Data")
        nb.AddPage(self.stereoPanel, _("Stereonet"))
        nb.AddPage(self.rosePanel, _("Rose diagram"))
        nb.AddPage(self.statsPanel, _("Statistics"))
        nb.AddPage(self.histPanel, _("Histogram"))

        nb_box = wx.BoxSizer(wx.VERTICAL) # sizer
        nb_box.Add(nb, 1, wx.EXPAND)
        self.right_panel.SetSizer(nb_box)

        #layout of widgets, left panel - CustomTreeCtrl
        box = wx.BoxSizer(wx.VERTICAL)
        self.tree = ctree.CustomTreeCtrl(self.left_panel, -1, style=wx.SUNKEN_BORDER)
        box.Add(self.tree, 1, wx.EXPAND)
        self.left_panel.SetSizer(box)

        splitter.SplitVertically(self.left_panel,self.right_panel,185)
        panelsizer.Add(splitter,1, wx.EXPAND)#|wx.ALL, 2) # the panels are inside this sizer with 2px border
        self.SetSizer(panelsizer)
#        panelsizer.Fit(self)
        self.onShow(wx.EVT_SHOW)

    # Here we define the default graphical properties of data
    # default list of props for planar data
        self.pplist = {"pdata":'str', "itemName":'str', \
                    "PolColor":'#000000', "PoleSymb":'o', "polespin":3.0, \
                    "CircColor":'#4D4D4D', "CircSty":'-', "circspin":0.8, \
                    "cb_eigen_gc1":False, "CircGirdColor1":'#00FF00', "styleGirdCirc1":'-', "circGirdspin1":1.0, \
                    "cb_eigen_p1":True, "PolGirdColor1":'#00FF00', "symbGirdPoles1":'*', "poleGirdspin1":12.0, \
                    "cb_eigen_gc2":False, "CircGirdColor2":'#FF0000', "styleGirdCirc2":'-', "circGirdspin2":1.0, \
                    "cb_eigen_p2":True, "PolGirdColor2":'#FF0000', "symbGirdPoles2":'*', "poleGirdspin2":12.0, \
                    "cb_eigen_gc3":False, "CircGirdColor3":'#0000FF', "styleGirdCirc3":'-', "circGirdspin3":1.0, \
                    "cb_eigen_p3":True, "PolGirdColor3":'#0000FF', "symbGirdPoles3":'*', "poleGirdspin3":12.0, \
                    "count_nodes":721, "percent":True, "interpolation":'Natural Neighbor', "gridSpin":250, \
                    "contStyle":'-', "contColor":'#4D4D4D', "contFill":True, "contLws":0.5, "colormap":'Reds', \
                    "contcolormap":'jet', "addedges":False, "rbsc":True, "rbcm":False, "antiAliased":False, "minmax":True, \
                    "zeromax":False, "numcontours":10, "custom":False, "customcont":'', "rbcossum":False, "expSpin":100, \
                    "rbfisher":True, "kSpin":100, "rbscarea":False, "areaSpin":1, "rbscangle":False, "angleSpin":10, \
                     "conCircSty":'--', "conCircColor":'#A52A2A', "conspin":1.5, "cb_conf":False}
#"epsilon":0.01, "smoothing":0, \

        # default list of props for linear data
        self.lplist = {"pdata":'str', "itemName":'str', \
                    "LinColor":'#4D4D4D', "LineSymb":'o', "linespin":3.0,\
                    "cb_eigen_gc1":False, "CircGirdColor1":'#00FF00', "styleGirdCirc1":'-', "circGirdspin1":1.0, \
                    "cb_eigen_p1":True, "PolGirdColor1":'#00FF00', "symbGirdPoles1":'*', "poleGirdspin1":12.0, \
                    "cb_eigen_gc2":False, "CircGirdColor2":'#FF0000', "styleGirdCirc2":'-', "circGirdspin2":1.0, \
                    "cb_eigen_p2":True, "PolGirdColor2":'#FF0000', "symbGirdPoles2":'*', "poleGirdspin2":12.0, \
                    "cb_eigen_gc3":False, "CircGirdColor3":'#0000FF', "styleGirdCirc3":'-', "circGirdspin3":1.0, \
                    "cb_eigen_p3":True, "PolGirdColor3":'#0000FF', "symbGirdPoles3":'*', "poleGirdspin3":12.0, \
                    "count_nodes":721, "percent":True, "interpolation":'Natural Neighbor', "gridSpin":250, \
                    "contStyle":'-', "contColor":'#4D4D4D', "contFill":True, "contLws":0.5, \
                    "colormap":'Blues', "contcolormap":'jet', "addedges":False, "rbsc":True, "rbcm":False, "antiAliased":False, \
                    "minmax":True, "zeromax":False, "numcontours":10, "custom":False, "customcont":'', "rbcossum":False, \
                    "expSpin":100, "rbfisher":True, "kSpin":100, "rbscarea":False, "areaSpin":1, "rbscangle":False, "angleSpin":10, \
                     "conCircSty":'--', "conCircColor":'#A52A2A', "conspin":1.5, "cb_conf":False}
#"epsilon":0.01, "smoothing":0, \


        # default list of props for fault data
        self.fplist = {"pdata":'str', "itemName":'str', \
                    "FaultCircColor":'#4D4D4D', "FaultCircSty":'-', "FaultCircSpin":0.8, \
                    "SlickPlotPoles":False, "SlickPoleColor":'#4D4D4D', "SlickPoleSymb":'o', "SlickPoleSpin":3.0, \
                    "SlickArrowSpin":1.0, "SlickArrowColor":'#4D4D4D', "SlickArrowWidthSpin":1.0, \
                    "DisplacePlotPoles":True, "DisplacePoleColor":'#4D4D4D', "DisplacePoleSymb":'o', "DisplacePoleSpin":3.0, \
                    "DisplaceArrowSpin":1.0, "DisplaceArrowColor":'#4D4D4D', "DisplaceArrowWidthSpin":1.0, \
                    "footwall":False}

        # default list of properties for small circle data
        self.scplist = {"pdata":'str',"itemName":'str',"ScColor":'#1E90FF',"ScSty":'-',"ScSpin":0.9, "ScFull":False}



    # indexes for files (to keep track of them)
        self.DDD_idx = 0
        self.RH_idx = 0
        self.Lin_idx = 0
        self.Sc_idx = 0
        self.F_idx = 0
        pub.subscribe(self.__onReceiveIdxs, 'object.Idxs') # pubsub only inside this class

    # subscriptions to pubsub
        pub.subscribe(self.__onReceivePlanarData, 'object.Plan_added_DDD') # from MainForm
        pub.subscribe(self.__onReceivePlanarData, 'object.Plan_added_RH') # from MainForm
        pub.subscribe(self.__onReceiveLinearData, 'object.Lin_added') # from MainForm
        pub.subscribe(self.__onReceiveFaultData, 'object.Fault_added') # from MainForm
        pub.subscribe(self.__onReceiveSmallData, 'object.Sc_added') # from MainForm
        pub.subscribe(self.__onReceiveIdxItemsDel, 'object.IdxItemsDeleted') # from TreePanel

        pub.subscribe(self.__onReceiveCurrentDir, 'object.CurrentDir') # pubsub only inside this class


    # icon for panel / taskbar
        image = OStereo_ico
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(image)
        self.SetIcon(icon)

#        self.tbicon = TaskBarIcon(self)

#        self.Bind(wx.EVT_ICONIZE, self.onMinimize)
#    # hide the frame
#    def onMinimize(self, event):
#        self.Hide()
##        event.Skip()

    def onShow(self, event):
        pub.sendMessage('object.axes_added', 1)
#        event.Skip()


# receiving indexes
    def __onReceiveIdxs(self, message):
        self.DDD_idx = message.data[0] # self.DDD_idx + message.data[0]
        self.RH_idx = message.data[1] # self.RH_idx + message.data[1]
        self.Lin_idx = message.data[2] # self.Lin_idx + message.data[2]
        self.Sc_idx = message.data[3] # self.Sc_idx + message.data[3]
        self.F_idx = message.data[4] # self.F_idx + message.data[4]

# receiving current Directory
    def __onReceiveCurrentDir(self, message):
        self.currentDirectory = message.data

# change font size

    def onFontSize(self,event):
        for item in self.opt.GetMenuItems():
            if item.IsChecked():
                size = item.GetItemLabelText()
                pub.sendMessage('object.FontSize', size) # send to StereoPanel, TreePanel, RosePanel, StatsPanel and HistPanel


#Open file, planar data (dipdir / dip)
    def OnOpenPlanarDataDDD(self, event):
        """ Open planar data (dipdir / dip) """

        if wx.Platform == '__WXMSW__':
            wildcard = 'TXT files (*.txt)|*.txt|CSV files (*.csv)|*.csv|DAT files (*.dat)|*.dat|All files (*.*)|*.*'
        else:
            wildcard = 'TXT files (*.txt)|*.txt|CSV files (*.csv)|*.csv|DAT files (*.dat)|*.dat|All files (*)|*'

        try:
            dlg=wx.FileDialog(
                self, message='Choose a file (planar data - dipdir/dip)',
                defaultDir=self.currentDirectory,
                defaultFile="",
                wildcard=wildcard,
                style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                )
            directory = self.currentDirectory
            if dlg.ShowModal() == wx.ID_OK:
                directory = dlg.GetDirectory()
                paths = dlg.GetPaths()
                files = dlg.GetFilenames()
                self.planDataDDD = []


                filetype = 1 # 1 = planar data

                for i in range(len(paths)):
                    filename = files[i]
                    self.DDD_idx = self.DDD_idx + 1
                    DDD_idx = 'DDD_%d' % self.DDD_idx
                    datalist = datad.getData(paths[i])
                    n_data,dipdir,dip,strike,eigenDict = datad.doPlanarDDD(datalist)
                    self.planDataDDD.append([filetype,filename,n_data,dipdir,dip,strike,eigenDict,DDD_idx,self.pplist])

            self.SetTitle(self.pyversion) # Set window title
            dlg.Destroy()

            pub.sendMessage('object.Plan_added_DDD', self.planDataDDD) # send to StereoPanel, TreePanel, RosePanel, StatsPanel and HistPanel
            pub.sendMessage('object.Idxs', [self.DDD_idx,self.RH_idx,self.Lin_idx,self.Sc_idx,self.F_idx])
            pub.sendMessage('object.CurrentDir', directory)

        except AttributeError:
            pass

#Open file, planar data (strike / dip - right hand rule)
    def OnOpenPlanarDataRH(self, event):
        """ Open planar data (strike / dip - right hand rule) """

        if wx.Platform == '__WXMSW__':
            wildcard = 'TXT files (*.txt)|*.txt|CSV files (*.csv)|*.csv|DAT files (*.dat)|*.dat|All files (*.*)|*.*'
        else:
            wildcard = 'TXT files (*.txt)|*.txt|CSV files (*.csv)|*.csv|DAT files (*.dat)|*.dat|All files (*)|*'

        try:
            dlg=wx.FileDialog(
                self, 'Choose a file (planar data - strike/dip - right hand rule)',
                defaultDir=self.currentDirectory,
                defaultFile="",
                wildcard=wildcard,
                style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                )
            directory = self.currentDirectory
            if dlg.ShowModal() == wx.ID_OK:
                directory = dlg.GetDirectory()
                paths = dlg.GetPaths()
                files = dlg.GetFilenames()

                self.planDataRH = []

                filetype = 1 # 1 = planar data

                for i in range(len(paths)):
                    filename = files[i]
                    self.RH_idx = self.RH_idx + 1
                    RH_idx = 'RH_%d' % self.RH_idx
                    datalist = datad.getData(paths[i])
                    n_data,dipdir,dip,strike,eigenDict = datad.doPlanarRH(datalist)
                    self.planDataRH.append([filetype,filename,n_data,dipdir,dip,strike,eigenDict,RH_idx,self.pplist])

            self.SetTitle(self.pyversion) # Set window title
            dlg.Destroy()

            pub.sendMessage('object.Plan_added_RH', self.planDataRH) # send to StereoPanel, TreePanel, RosePanel, StatsPanel and HistPanel
            pub.sendMessage('object.Idxs', [self.DDD_idx,self.RH_idx,self.Lin_idx,self.Sc_idx,self.F_idx])
            pub.sendMessage('object.CurrentDir', directory)

        except AttributeError:
            pass

#Open file, linear data
    def OnOpenLinearData(self, event):
        """ Open linear data (Trend/ Plunge) """

        if wx.Platform == '__WXMSW__':
            wildcard = 'TXT files (*.txt)|*.txt|CSV files (*.csv)|*.csv|DAT files (*.dat)|*.dat|All files (*.*)|*.*'
        else:
            wildcard = 'TXT files (*.txt)|*.txt|CSV files (*.csv)|*.csv|DAT files (*.dat)|*.dat|All files (*)|*'

        try:
            dlg=wx.FileDialog(
                self, 'Choose a file (linear data)',
                defaultDir=self.currentDirectory,
                defaultFile="",
                wildcard=wildcard,
                style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                )
            directory = self.currentDirectory
            if dlg.ShowModal() == wx.ID_OK:
                directory = dlg.GetDirectory()
                paths = dlg.GetPaths()
                files = dlg.GetFilenames()
                self.linData =[]

                filetype = 2 # 2 = linear data

                for i in range(len(paths)):
                    filename = files[i]
                    self.Lin_idx = self.Lin_idx + 1
                    Lin_idx = 'Lin_%d' % self.Lin_idx
                    datalist = datad.getData(paths[i])
                    n_data,dipdir,dip,strike,eigenDict = datad.doLinear(datalist)
                    self.linData.append([filetype,filename,n_data,dipdir,dip,strike,eigenDict,Lin_idx,self.lplist])

            self.SetTitle(self.pyversion) # Set window title
            dlg.Destroy()

            pub.sendMessage('object.Lin_added', self.linData) # send to StereoPanel, TreePanel, RosePanel, StatsPanel and HistPanel
            pub.sendMessage('object.Idxs', [self.DDD_idx,self.RH_idx,self.Lin_idx,self.Sc_idx,self.F_idx])
            pub.sendMessage('object.CurrentDir', directory)

        except AttributeError:
            pass


#Open file, fault data (dipdir/dip // trend/plunge // sense)
    def OnOpenFaultData(self, event):
        """ Open fault data (dipdir/dip // trend/plunge // sense) """

        if wx.Platform == '__WXMSW__':
            wildcard = 'TXT files (*.txt)|*.txt|CSV files (*.csv)|*.csv|DAT files (*.dat)|*.dat|All files (*.*)|*.*'
        else:
            wildcard = 'TXT files (*.txt)|*.txt|CSV files (*.csv)|*.csv|DAT files (*.dat)|*.dat|All files (*)|*'

        try:
            dlg=wx.FileDialog(
                self, 'Choose a file (fault data (dipdir/dip // trend/plunge // sense)',
                defaultDir=self.currentDirectory,
                defaultFile="",
                wildcard=wildcard,
                style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                )
            directory = self.currentDirectory
            if dlg.ShowModal() == wx.ID_OK:
                directory = dlg.GetDirectory()
                paths = dlg.GetPaths()
                files = dlg.GetFilenames()
                self.faultData = []

                filetype = 4 # 4 = fault data

                for i in range(len(paths)):
                    filename = files[i]
                    self.F_idx = self.F_idx + 1
                    F_idx = 'F_%d' % self.F_idx
                    datalist = datad.getData(paths[i])
                    n_data,dipdir,dip,strike,eigenDict,trend,plunge,sense = datad.doFault(datalist)
                    self.faultData.append([filetype,filename,n_data,dipdir,dip,strike,eigenDict,trend,plunge,sense,F_idx,self.fplist])

            self.SetTitle(self.pyversion) # Set window title
            dlg.Destroy()

            pub.sendMessage('object.Fault_added', self.faultData) # send to StereoPanel, TreePanel, RosePanel, StatsPanel and HistPanel
            pub.sendMessage('object.Idxs', [self.DDD_idx,self.RH_idx,self.Lin_idx,self.Sc_idx,self.F_idx])
            pub.sendMessage('object.CurrentDir', directory)

        except AttributeError:
            pass



#Open file, PLANES from fault data (dipdir/dip)
    def OnOpenFaultPlanes(self, event):
        """ Open planes from fault data (dipdir/dip // trend/plunge // sense) """

        if wx.Platform == '__WXMSW__':
            wildcard = 'TXT files (*.txt)|*.txt|CSV files (*.csv)|*.csv|DAT files (*.dat)|*.dat|All files (*.*)|*.*'
        else:
            wildcard = 'TXT files (*.txt)|*.txt|CSV files (*.csv)|*.csv|DAT files (*.dat)|*.dat|All files (*)|*'

        try:
            dlg=wx.FileDialog(
                self, 'Choose a file (fault data (dipdir/dip // trend/plunge // sense)',
                defaultDir=self.currentDirectory,
                defaultFile="",
                wildcard=wildcard,
                style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                )
            directory = self.currentDirectory
            if dlg.ShowModal() == wx.ID_OK:
                directory = dlg.GetDirectory()
                paths = dlg.GetPaths()
                files = dlg.GetFilenames()
                self.planDataDDD = []

                filetype = 1 # 1 = planar data

                for i in range(len(paths)):
                    filename = files[i]
                    self.DDD_idx = self.DDD_idx + 1
                    DDD_idx = 'DDD_%d' % self.DDD_idx
                    datalist = datad.getData(paths[i])
                    n_data,dipdir,dip,strike,eigenDict = datad.doFaultPlanar(datalist)
                    self.planDataDDD.append([filetype,filename,n_data,dipdir,dip,strike,eigenDict,DDD_idx,self.pplist])

            self.SetTitle(self.pyversion) # Set window title
            dlg.Destroy()

            pub.sendMessage('object.Plan_added_DDD', self.planDataDDD) # send to StereoPanel, TreePanel, RosePanel, StatsPanel and HistPanel
            pub.sendMessage('object.Idxs', [self.DDD_idx,self.RH_idx,self.Lin_idx,self.Sc_idx,self.F_idx])
            pub.sendMessage('object.CurrentDir', directory)

        except AttributeError:
            pass



#Open file, LINES from fault data (trend/plunge)
    def OnOpenFaultLines(self, event):
        """ Open lines from fault data (dipdir/dip // trend/plunge // sense) """

        if wx.Platform == '__WXMSW__':
            wildcard = 'TXT files (*.txt)|*.txt|CSV files (*.csv)|*.csv|DAT files (*.dat)|*.dat|All files (*.*)|*.*'
        else:
            wildcard = 'TXT files (*.txt)|*.txt|CSV files (*.csv)|*.csv|DAT files (*.dat)|*.dat|All files (*)|*'

        try:
            dlg=wx.FileDialog(
                self, 'Choose a file (fault data (dipdir/dip // trend/plunge // sense)',
                defaultDir=self.currentDirectory,
                defaultFile="",
                wildcard=wildcard,
                style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                )
            directory = self.currentDirectory
            if dlg.ShowModal() == wx.ID_OK:
                directory = dlg.GetDirectory()
                paths = dlg.GetPaths()
                files = dlg.GetFilenames()
                self.linData =[]

                filetype = 2 # 2 = linear data

                for i in range(len(paths)):
                    filename = files[i]
                    self.Lin_idx = self.Lin_idx + 1
                    Lin_idx = 'Lin_%d' % self.Lin_idx
                    datalist = datad.getData(paths[i])
                    n_data,dipdir,dip,strike,eigenDict = datad.doFaultLinear(datalist)
                    self.linData.append([filetype,filename,n_data,dipdir,dip,strike,eigenDict,Lin_idx,self.lplist])

            self.SetTitle(self.pyversion) # Set window title
            dlg.Destroy()

            pub.sendMessage('object.Lin_added', self.linData) # send to StereoPanel, TreePanel, RosePanel, StatsPanel and HistPanel
            pub.sendMessage('object.Idxs', [self.DDD_idx,self.RH_idx,self.Lin_idx,self.Sc_idx,self.F_idx])
            pub.sendMessage('object.CurrentDir', directory)

        except AttributeError:
            pass


#Open TectonicsFP file, fault data (dipdir/dip // trend/plunge // sense)
    def OnOpenFaultTectonicsFP(self, event):
        """ Open fault data (dipdir/dip // trend/plunge // sense) """

        if wx.Platform == '__WXMSW__':
            wildcard = 'COR files (*.cor)|*.cor|FPL files (*.fpl)|*.fpl|TXT files (*.txt)|*.txt|All files (*.*)|*.*'
        else:
            wildcard = 'COR files (*.cor)|*.cor|FPL files (*.fpl)|*.fpl|TXT files (*.txt)|*.txt|All files (*)|*'

        try:
            dlg=wx.FileDialog(
                self, 'Choose a file (fault data (dipdir/dip // trend/plunge // sense)',
                defaultDir=self.currentDirectory,
                defaultFile="",
                wildcard=wildcard,
                style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                )
            directory = self.currentDirectory
            if dlg.ShowModal() == wx.ID_OK:
                directory = dlg.GetDirectory()
                paths = dlg.GetPaths()
                files = dlg.GetFilenames()
                self.faultData = []

                filetype = 4 # 4 = fault data

                for i in range(len(paths)):
                    filename = files[i]
                    self.F_idx = self.F_idx + 1
                    F_idx = 'F_%d' % self.F_idx
                    datalist = datad.getDataTectonicsFP(paths[i])
                    n_data,dipdir,dip,strike,eigenDict,trend,plunge,sense = datad.doFault(datalist)
                    self.faultData.append([filetype,filename,n_data,dipdir,dip,strike,eigenDict,trend,plunge,sense,F_idx,self.fplist])

            self.SetTitle(self.pyversion) # Set window title
            dlg.Destroy()

            pub.sendMessage('object.Fault_added', self.faultData) # send to StereoPanel, TreePanel, RosePanel, StatsPanel and HistPanel
            pub.sendMessage('object.Idxs', [self.DDD_idx,self.RH_idx,self.Lin_idx,self.Sc_idx,self.F_idx])
            pub.sendMessage('object.CurrentDir', directory)

        except AttributeError:
            pass




#Open TTECTO file, fault data (dipdir/dip // trend/plunge // sense)
    def OnOpenFaultTTECTO(self, event):
        """ Open fault data (dipdir/dip // trend/plunge // sense) """

        if wx.Platform == '__WXMSW__':
            wildcard = 'COR files (*.cor)|*.cor|FPL files (*.fpl)|*.fpl|TXT files (*.txt)|*.txt|All files (*.*)|*.*'
        else:
            wildcard = 'COR files (*.cor)|*.cor|FPL files (*.fpl)|*.fpl|TXT files (*.txt)|*.txt|All files (*)|*'

        try:
            dlg=wx.FileDialog(
                self, 'Choose a file (fault data (dipdir/dip // trend/plunge // sense)',
                defaultDir=self.currentDirectory,
                defaultFile="",
                wildcard=wildcard,
                style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                )
            directory = self.currentDirectory
            if dlg.ShowModal() == wx.ID_OK:
                directory = dlg.GetDirectory()
                paths = dlg.GetPaths()
                files = dlg.GetFilenames()
                self.faultData = []

                filetype = 4 # 4 = fault data

                for i in range(len(paths)):
                    filename = files[i]
                    self.F_idx = self.F_idx + 1
                    F_idx = 'F_%d' % self.F_idx
                    datalist = datad.getDataTTECTO(paths[i])
                    n_data,dipdir,dip,strike,eigenDict,trend,plunge,sense = datad.doFault(datalist)
                    self.faultData.append([filetype,filename,n_data,dipdir,dip,strike,eigenDict,trend,plunge,sense,F_idx,self.fplist])

            self.SetTitle(self.pyversion) # Set window title
            dlg.Destroy()

            pub.sendMessage('object.Fault_added', self.faultData) # send to StereoPanel, TreePanel, RosePanel, StatsPanel and HistPanel
            pub.sendMessage('object.Idxs', [self.DDD_idx,self.RH_idx,self.Lin_idx,self.Sc_idx,self.F_idx])
            pub.sendMessage('object.CurrentDir', directory)

        except AttributeError:
            pass




#Open file, small circle data
    def OnOpenSmallData(self, event):
        """ Open small circle data """

        if wx.Platform == '__WXMSW__':
            wildcard = 'TXT files (*.txt)|*.txt|CSV files (*.csv)|*.csv|DAT files (*.dat)|*.dat|All files (*.*)|*.*'
        else:
            wildcard = 'TXT files (*.txt)|*.txt|CSV files (*.csv)|*.csv|DAT files (*.dat)|*.dat|All files (*)|*'

        try:
            dlg=wx.FileDialog(
                self, 'Choose a file (small circle data)',
                defaultDir=self.currentDirectory,
                defaultFile="",
                wildcard=wildcard,
                style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                )
            directory = self.currentDirectory
            if dlg.ShowModal() == wx.ID_OK:
                directory = dlg.GetDirectory()
                paths = dlg.GetPaths()
                files = dlg.GetFilenames()
                self.scData =[]

                filetype = 3 # 3 = small circle data

                for i in range(len(paths)):
                    filename = files[i]
                    self.Sc_idx = self.Sc_idx + 1
                    Sc_idx = 'Sc_%d' % self.Sc_idx
                    datalist = datad.getData(paths[i])
                    n_data,azim,dip,alpha = datad.doSmall(datalist)
                    self.scData.append([filetype,filename,n_data,azim,dip,alpha,Sc_idx,self.scplist])

            self.SetTitle(self.pyversion) # Set window title
            dlg.Destroy()

            pub.sendMessage('object.Sc_added', self.scData) # send to StereoPanel, TreePanel and StatsPanel
            pub.sendMessage('object.Idxs', [self.DDD_idx,self.RH_idx,self.Lin_idx,self.Sc_idx,self.F_idx])
            pub.sendMessage('object.CurrentDir', directory)

        except AttributeError:
            pass


# about box
    def onAboutDlg(self, event):
        info = wx.AboutDialogInfo()
        info.Name = "OpenStereoNet"
        info.Version = self.OpenStereo_version
        info.Copyright = "(C) 2009-2011 Carlos H. Grohmann and Ginaldo A.C. Campanha"
        info.Copyright += "\n(C) 2012-2013 Matteo Pasotti"
        info.Description = wordwrap(
            "OpenStereoNet is a Open-source, multiplatform software for "
            "structural geology analysis using stereonets. ",
            350, wx.ClientDC(self.right_panel))
        #info.WebSite = ("http://www.igc.usp.br/openstereo", "Original OpenStereo Home Page")
        info.WebSite = ("https://github.com/xquiet/openstereo", "OpenStereoNet")
        info.Developers = ["Carlos H. Grohmann & Ginaldo A.C. Campanha",
                        "Matteo Pasotti"]
        info.License = wordwrap('''OpenStereoNet is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenStereoNet is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenStereoNet.  If not, see <http://www.gnu.org/licenses/>.


Originally developed by: Carlos H. Grohmann & Ginaldo A.C. Campanha
            Institute of Geosciences - University of Sao Paulo - Brazil
            Rua do Lago, 562 - Sao Paulo - SP - Brazil - 05508-080
            guano@usp.br, ginaldo@usp.br
            http://www.igc.usp.br/openstereo
Forked by: Matteo Pasotti <matteo.pasotti@gmail.com>
           Lombardy, Italy


Requirements:
     Python version 2.4 or higher
     wxPython version 2.8.10 or higher
     Matplotlib version 0.98 or higher
     NumPy version 1.1 or higher
     Gettext

''', 500,
                                wx.ClientDC(self.right_panel))
        # Show the wx.AboutBox
        wx.AboutBox(info)



# pubsub - retrieving planar data - from TreePanel (for list of loaded files)
    def __onReceivePlanarData(self, message):

        try:
            len(self.Pname) # dummy action just to see if self.Pname exists
        except:
            self.Pname=[]
            self.Pndata=[]
            self.Pazim=[]
            self.Pdip=[]
            self.PidxList=[]

        for i in range(len(message.data)):
            self.Pname.append('[P] %s' % message.data[i][1])
            self.Pndata.append(message.data[i][2])
            self.Pazim.append(message.data[i][3])
            self.Pdip.append(message.data[i][4])
            self.PidxList.append(message.data[i][7])


# pubsub - retrieving linear data - from TreePanel (for list of loaded files)
    def __onReceiveLinearData(self, message):

        try:
            len(self.Lname) # dummy action just to see if self.Lname exists
        except:
            self.Lname=[]
            self.Lndata=[]
            self.Lazim=[]
            self.Ldip=[]
            self.LidxList=[]

        for i in range(len(message.data)):
            self.Lname.append('[L] %s' % message.data[i][1])
            self.Lndata.append(message.data[i][2])
            self.Lazim.append(message.data[i][3])
            self.Ldip.append(message.data[i][4])
            self.LidxList.append(message.data[i][7])



# pubsub - retrieving fault data - from TreePanel (for list of loaded files)
    def __onReceiveFaultData(self, message):

        try:
            len(self.Fname) # dummy action just to see if self.Lname exists
        except:
            self.Fname=[]
            self.Fndata=[]
            self.Fazim=[]
            self.Fdip=[]
            self.Ftrend=[]
            self.Fplunge=[]
            self.Fsense=[]
            self.FidxList=[]

        for i in range(len(message.data)):
            self.Fname.append('[F] %s' % message.data[i][1])       # filename
            self.Fndata.append(message.data[i][2])      # n_data
            self.Fazim.append(message.data[i][3])       # dipdir
            self.Fdip.append(message.data[i][4])        # dip
            self.Ftrend.append(message.data[i][7])      # trend
            self.Fplunge.append(message.data[i][8])     # plunge
            self.Fsense.append(message.data[i][9])      # sense
            self.FidxList.append(message.data[i][10])   # F_idx



# pubsub - retrieving small circle data - from TreePanel (for list of loaded files)
    def __onReceiveSmallData(self, message):

        try:
            len(self.Scname) # dummy action just to see if self.Lname exists
        except:
            self.Scname=[]
            self.Scndata=[]
            self.ScidxList=[]
            self.Scazim=[]
            self.Scdip=[]
            self.Scalpha=[]

        for i in range(len(message.data)):
            self.Scname.append('[SC] %s' % message.data[i][1])
            self.Scndata.append(message.data[i][2])
            self.Scazim.append(message.data[i][3])
            self.Scdip.append(message.data[i][4])
            self.Scalpha.append(message.data[i][5])
            self.ScidxList.append(message.data[i][6])


# pubsub - retrieving indexes of deleted items (fromm TreePanel)
    def __onReceiveIdxItemsDel(self, message):

        if message.data[0] is not None:
            PidxListDel = message.data[0]
            self.Pname.pop(PidxListDel)
            self.Pndata.pop(PidxListDel)
            self.Pazim.pop(PidxListDel)
            self.Pdip.pop(PidxListDel)
            self.PidxList.pop(PidxListDel)

        if message.data[1] is not None:
            LidxListDel = message.data[1]
            self.Lname.pop(LidxListDel)
            self.Lndata.pop(LidxListDel)
            self.Lazim.pop(LidxListDel)
            self.Ldip.pop(LidxListDel)
            self.LidxList.pop(LidxListDel)

        if message.data[2] is not None:
            ScidxListDel = message.data[2]
            self.Scname.pop(ScidxListDel)
            self.Scndata.pop(ScidxListDel)
            self.Scazim.pop(ScidxListDel)
            self.Scdip.pop(ScidxListDel)
            self.Scalpha.pop(ScidxListDel)
            self.ScidxList.pop(ScidxListDel)

        if message.data[3] is not None:
            FidxListDel = message.data[3]
            self.Fname.pop(FidxListDel)
            self.Fndata.pop(FidxListDel)
            self.Fazim.pop(FidxListDel)
            self.Fdip.pop(FidxListDel)
            self.Ftrend.pop(FidxListDel)
            self.Fplunge.pop(FidxListDel)
            self.Fsense.pop(FidxListDel)
            self.FidxList.pop(FidxListDel)


# get list of opened files
    def GetListOfFiles(self):
        """ returns a list of opened files """

        filesList = []

        try:
            filesList.append([self.Pname, self.Pndata, self.Pazim, self.Pdip, self.PidxList])
        except AttributeError:
            pass

        try:
            filesList.append([self.Lname, self.Lndata, self.Lazim, self.Ldip, self.LidxList])
        except AttributeError:
            pass

        try:
            filesList.append([self.Scname,self.Scndata, self.Scazim, self.Scdip, self.Scalpha, self.ScidxList])
        except AttributeError:
            pass

        try:
            filesList.append([self.Fname,self.Fndata,self.Fazim,self.Fdip,self.Ftrend,self.Fplunge,self.Fsense,self.FidxList])
        except AttributeError:
            pass

        return filesList


#Join (merge) two or more data files
    def OnMergeData(self, event):
        """ join (merge) two or more data files """

        filesList = self.GetListOfFiles()
        mergedlg = tools.MergeData(self, -1, 'Merge Data', filesList)

        try:
            newname, filename, azMerge, dpMerge, trMerge, pgMerge, snMerge, alphaMerge, dataType, \
            cb_append, cb_save, rbPlanar, rbLinear, rbSmall, rbFault =  mergedlg.onMergeData()

            if cb_save:
                # check what kind of data we have and then save
                if 'S' in dataType: # small circle data
                    filehandle=open(newname,'wt')
                    for i in range(len(azMerge)):
                        filehandle.write('%3.2f\t%3.2f\t%3.2f\n' % (azMerge[i], dpMerge[i], alphaMerge[i]))
                    filehandle.close()
                elif 'F' in dataType: # fault data
                    filehandle=open(newname,'wt')
                    for i in range(len(azMerge)):
                        filehandle.write('%3.2f\t%3.2f\t%3.2f\t%3.2f\t%s\n' % (azMerge[i], dpMerge[i], trMerge[i], pgMerge[i], snMerge[i]))
                    filehandle.close()
                else: # 'P' or 'L' in dataType: # merged has only planar or linear data, no need for a third column
                    filehandle=open(newname,'wt')
                    for i in range(len(azMerge)):
                        filehandle.write('%3.2f\t%3.2f\n' % (azMerge[i], dpMerge[i]))
                    filehandle.close()

                # now define if 'datalist' will be created from the saved file or from the data in memory
                # from the file
                datalist = datad.getData(newname)

            else: # data in memory only
                if 'S' in dataType:
                    datalist = [[azMerge[i], dpMerge[i], alphaMerge[i]] for i in range(len(azMerge))]
                elif 'F' in dataType:
                    datalist = [[azMerge[i], dpMerge[i], trMerge[i], pgMerge[i], snMerge[i]] for i in range(len(azMerge))]
                else:
                    datalist = [[azMerge[i], dpMerge[i]] for i in range(len(azMerge))]




            # check if data should be loaded in the tree
            if cb_append:
                if rbPlanar:
                    self.planDataDDD = []
                    filetype = 1 # 1 = planar data

                    self.DDD_idx = self.DDD_idx + 1
                    DDD_idx = 'DDD_%d' % self.DDD_idx
                    n_data,dipdir,dip,strike,eigenDict = datad.doPlanarDDD(datalist)
                    self.planDataDDD.append([filetype,filename,n_data,dipdir,dip,strike,eigenDict,DDD_idx,self.pplist])

                    pub.sendMessage('object.Plan_added_DDD', self.planDataDDD) # send to StereoPanel, TreePanel and StatsPanel
                    pub.sendMessage('object.Idxs', [self.DDD_idx,self.RH_idx,self.Lin_idx,self.Sc_idx,self.F_idx])

                elif rbLinear:
                    self.linData =[]
                    filetype = 2 # 2 = linear data

                    self.Lin_idx = self.Lin_idx + 1
                    Lin_idx = 'Lin_%d' % self.Lin_idx
                    n_data,dipdir,dip,strike,eigenDict = datad.doLinear(datalist)
                    self.linData.append([filetype,filename,n_data,dipdir,dip,strike,eigenDict,Lin_idx,self.lplist])

                    pub.sendMessage('object.Lin_added', self.linData) # send to StereoPanel, TreePanel and StatsPanel
                    pub.sendMessage('object.Idxs', [self.DDD_idx,self.RH_idx,self.Lin_idx,self.Sc_idx,self.F_idx])

                elif rbFault:
                    self.faultData = []
                    filetype = 4 # 4 = fault data

                    self.F_idx = self.F_idx + 1
                    F_idx = 'F_%d' % self.F_idx
                    n_data,dipdir,dip,strike,eigenDict,trend,plunge,sense = datad.doFault(datalist)
                    self.faultData.append([filetype,filename,n_data,dipdir,dip,strike,eigenDict,trend,plunge,sense,F_idx,self.fplist])

                    pub.sendMessage('object.Fault_added', self.faultData) # send to StereoPanel, TreePanel, RosePanel, StatsPanel and HistPanel
                    pub.sendMessage('object.Idxs', [self.DDD_idx,self.RH_idx,self.Lin_idx,self.Sc_idx,self.F_idx])


                elif rbSmall:
                    self.scData =[]
                    filetype = 3 # 2 = small circle data

                    self.Sc_idx = self.Sc_idx + 1
                    Sc_idx = 'Sc_%d' % self.Sc_idx
                    n_data,azim,dip,alpha = datad.doSmall(datalist)
                    self.scData.append([filetype,filename,n_data,azim,dip,alpha,Sc_idx,self.scplist])

                    pub.sendMessage('object.Sc_added', self.scData) # send to StereoPanel, TreePanel and StatsPanel
                    pub.sendMessage('object.Idxs', [self.DDD_idx,self.RH_idx,self.Lin_idx,self.Sc_idx,self.F_idx])

        except:
            pass


# Rotate data files
    def OnRotateData(self, event):
        """ rotate data files """

        filesList = self.GetListOfFiles()

        rotadlg = tools.RotateData(self, -1, 'Rotate Data', filesList)

        try:
            newname, filename, azRot, dpRot, trRot, pgRot, sense, alphaRot, dataType, \
            cb_append, cb_save, rbPlanar, rbLinear, rbSmall, rbFault =  rotadlg.onRotateData()

            if cb_save:
                # check what kind of data we have and then save
                if 'S' in dataType: # small circle data
                    filehandle=open(newname,'wt')
                    for i in range(len(azMerge)):
                        filehandle.write('%3.2f\t%3.2f\t%3.2f\n' % (azRot[i], dpRot[i], alphaRot[i]))
                    filehandle.close()
                elif 'F' in dataType: # fault data
                    filehandle=open(newname,'wt')
                    for i in range(len(azMerge)):
                        filehandle.write('%3.2f\t%3.2f\t%3.2f\t%3.2f\t%s\n' % (azRot[i], dpRot[i], trRot[i], pgRot[i], sense[i]))
                    filehandle.close()
                else: # 'P' or 'L' in dataType: # merged has only planar or linear data, no need for a third column
                    filehandle=open(newname,'wt')
                    for i in range(len(azMerge)):
                        filehandle.write('%3.2f\t%3.2f\n' % (azRot[i], dpRot[i]))
                    filehandle.close()
                # now define if 'datalist' will be created from the saved file or from the data in memory
                # from the file
                datalist = datad.getData(newname)

            else: # from data in memory
                if 'S' in dataType:
                    datalist = [[azRot[i], dpRot[i], alphaRot[i]] for i in range(len(azRot))]
                elif 'F' in dataType:
                    datalist = [[azRot[i], dpRot[i], trRot[i], pgRot[i], sense[i]] for i in range(len(azRot))]
                else:
                    datalist = [[azRot[i], dpRot[i]] for i in range(len(azRot))]


            # check if data should be loaded in the tree
            if cb_append:
                if rbPlanar:
                    self.planDataDDD = []
                    filetype = 1 # 1 = planar data

                    self.DDD_idx = self.DDD_idx + 1
                    DDD_idx = 'DDD_%d' % self.DDD_idx
                    n_data,dipdir,dip,strike,eigenDict = datad.doPlanarDDD(datalist)
                    self.planDataDDD.append([filetype,filename,n_data,dipdir,dip,strike,eigenDict,DDD_idx,self.pplist])

                    pub.sendMessage('object.Plan_added_DDD', self.planDataDDD) # send to StereoPanel, TreePanel and StatsPanel
                    pub.sendMessage('object.Idxs', [self.DDD_idx,self.RH_idx,self.Lin_idx,self.Sc_idx,self.F_idx])

                elif rbLinear:
                    self.linData =[]
                    filetype = 2 # 2 = linear data

                    self.Lin_idx = self.Lin_idx + 1
                    Lin_idx = 'Lin_%d' % self.Lin_idx
                    n_data,dipdir,dip,strike,eigenDict = datad.doLinear(datalist)
                    self.linData.append([filetype,filename,n_data,dipdir,dip,strike,eigenDict,Lin_idx,self.lplist])

                    pub.sendMessage('object.Lin_added', self.linData) # send to StereoPanel, TreePanel and StatsPanel
                    pub.sendMessage('object.Idxs', [self.DDD_idx,self.RH_idx,self.Lin_idx,self.Sc_idx,self.F_idx])

                elif rbFault:
                    self.faultData = []
                    filetype = 4 # 4 = fault data

                    self.F_idx = self.F_idx + 1
                    F_idx = 'F_%d' % self.F_idx
                    n_data,dipdir,dip,strike,eigenDict,trend,plunge,sense = datad.doFault(datalist)
                    self.faultData.append([filetype,filename,n_data,dipdir,dip,strike,eigenDict,trend,plunge,sense,F_idx,self.fplist])

                    pub.sendMessage('object.Fault_added', self.faultData) # send to StereoPanel, TreePanel, RosePanel, StatsPanel and HistPanel
                    pub.sendMessage('object.Idxs', [self.DDD_idx,self.RH_idx,self.Lin_idx,self.Sc_idx,self.F_idx])

                elif rbSmall:
                    self.scData =[]
                    filetype = 3 # 2 = small circle data

                    self.Sc_idx = self.Sc_idx + 1
                    Sc_idx = 'Sc_%d' % self.Sc_idx
                    n_data,azim,dip,alpha = datad.doSmall(datalist)
                    self.scData.append([filetype,filename,n_data,azim,dip,alpha,Sc_idx,self.scplist])

                    pub.sendMessage('object.Sc_added', self.scData) # send to StereoPanel, TreePanel and StatsPanel
                    pub.sendMessage('object.Idxs', [self.DDD_idx,self.RH_idx,self.Lin_idx,self.Sc_idx,self.F_idx])

        except:
            pass








    def Exit(self, event):
        if getattr(self, 'file',0):
            self.file.close()
        self.Close(True)


#    def OnCloseWindow(self, evt):
#        self.tbicon.Destroy()
#        evt.Skip()


#class TaskBarIcon(wx.TaskBarIcon):
#    TBMENU_RESTORE = wx.NewId()
#    TBMENU_CLOSE   = wx.NewId()
#    TBMENU_CHANGE  = wx.NewId()
#    TBMENU_REMOVE  = wx.NewId()

#    def __init__(self, frame):
#        wx.TaskBarIcon.__init__(self)
#        self.frame = frame

#        # Set the image
#        guirdle_ico = bitmaps.plot_girdle.GetImage()
#        icon = self.MakeIcon(guirdle_ico)
#        self.SetIcon(icon, 'OpenStereo')
#        self.imgidx = 1

#        # bind some events
#        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarActivate)
#        self.Bind(wx.EVT_MENU, self.OnTaskBarActivate, id=self.TBMENU_RESTORE)
#        self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=self.TBMENU_CLOSE)


#    def CreatePopupMenu(self):
#        """
#        This method is called by the base class when it needs to popup
#        the menu for the default EVT_RIGHT_DOWN event.  Just create
#        the menu how you want it and return it from this function,
#        the base class takes care of the rest.
#        """
#        menu = wx.Menu()
#        menu.Append(self.TBMENU_RESTORE, "Restore wxPython Demo")
#        menu.Append(self.TBMENU_CLOSE,   "Close wxPython Demo")
#        return menu


#    def MakeIcon(self, img):
#        """
#        The various platforms have different requirements for the
#        icon size...
#        """
#        if "wxMSW" in wx.PlatformInfo:
#            img = img.Scale(16, 16)
#        elif "wxGTK" in wx.PlatformInfo:
#            img = img.Scale(22, 22)
#        # wxMac can be any size upto 128x128, so leave the source img alone....
#        icon = wx.IconFromBitmap(img.ConvertToBitmap())
#        return icon


#    def OnTaskBarActivate(self, evt):
#        if self.frame.IsIconized():
#            self.frame.Iconize(False)
#        if not self.frame.IsShown():
#            self.frame.Show(True)
#        self.frame.Raise()


#    def OnTaskBarClose(self, evt):
#        wx.CallAfter(self.frame.Close)
