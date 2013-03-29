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
import wx.lib.colourselect as csel

import floatspin as FS
#import wx.lib.agw.floatspin as FS
import scrolledpanel as scrolled
from wx.lib.pubsub import Publisher as pub
from matplotlib import cm

symbolList = ['o       (circle)',\
'^       (triangle up)',\
'v       (triangle down)',\
'<       (triangle left)',\
'>       (triangle right)',\
's       (square)',\
'+       (plus)',\
'x       (cross)',\
'D      (diamond)',\
'd      (thin diamond)',\
'h      (hexagon 1)',\
'H      (hexagon 2)',\
'p      (pentagon)',\
'I      (vertical line)',\
'_      (horizontal line)',\
'*       (star)',\
'1      (tri_down)',\
'2      (tri_up)',\
'3      (tri_left)',\
'4      (tri_right)']
symbols = ['o','^','v','<','>','s','+','x','D','d','h','H','p','I','_','*','1','2','3','4']

styleList = ['-      (solid)',\
':      (dotted)',\
'--     (dashed)',\
'-.     (dashed dot)']
styles = ['-', ':', '--', '-.']

#countNodesList = ['331', '721', '1261', '2791']
countNodesList = ['Crude', 'Low', 'Medium', 'High']
countNodes = [331, 721, 1261, 2791]

interpList = ['Natural Neighbor',\
'Triangulation']

# this is for RBF interpolation (SciPy)
#interpList = ['Natural Neighbor',\
#'Triangulation',\
#'Multiquadric',\
#'Inverse Multiquadric',\
#'Gaussian',\
#'Linear RBF',\
#'Cubic',\
#'Quintic',\
#'Thin-plate Spline']


mapsList = ['jet',\
'jet_r',\
'hsv',\
'hsv_r',\
'Greys',\
'Greys_r',\
'Blues',\
'Blues_r',\
'Greens',\
'Greens_r',\
'Oranges',\
'Oranges_r',\
'Reds',\
'Reds_r']


class PlanarOptions(wx.Dialog):
    def __init__(self, parent, id, title, opt_dict):#, size=(725,425)
        wx.Dialog.__init__(self, parent, id, title, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME)

# defaults for colors and symbols
#        idx = opt_dict[0]
#        name = opt_dict[1]
        self.PolColor = opt_dict["PolColor"]
        self.PoleSymb = opt_dict["PoleSymb"]
        self.polespin = opt_dict["polespin"]
        self.CircColor = opt_dict["CircColor"]
        self.CircSty = opt_dict["CircSty"]
        self.circspin = opt_dict["circspin"]

        self.cbconf  = opt_dict["cb_conf"]
        self.conCircColor = opt_dict["conCircColor"]
        self.conCircSty = opt_dict["conCircSty"]
        self.conspin = opt_dict["conspin"]

        self.cbeigengc1 = opt_dict["cb_eigen_gc1"]
        self.CircGirdColor1 = opt_dict["CircGirdColor1"]
        self.CircGirdSty1 = opt_dict["styleGirdCirc1"]
        self.circGirdspin1 = opt_dict["circGirdspin1"]
        self.cbeigenp1 = opt_dict["cb_eigen_p1"]
        self.PolGirdColor1 = opt_dict["PolGirdColor1"]
        self.PoleGirdSymb1 = opt_dict["symbGirdPoles1"]
        self.poleGirdspin1 = opt_dict["poleGirdspin1"]

        self.cbeigengc2 = opt_dict["cb_eigen_gc2"]
        self.CircGirdColor2 = opt_dict["CircGirdColor2"]
        self.CircGirdSty2 = opt_dict["styleGirdCirc2"]
        self.circGirdspin2 = opt_dict["circGirdspin2"]
        self.cbeigenp2 = opt_dict["cb_eigen_p2"]
        self.PolGirdColor2 = opt_dict["PolGirdColor2"]
        self.PoleGirdSymb2 = opt_dict["symbGirdPoles2"]
        self.poleGirdspin2 = opt_dict["poleGirdspin2"]

        self.cbeigengc3 = opt_dict["cb_eigen_gc3"]
        self.CircGirdColor3 = opt_dict["CircGirdColor3"]
        self.CircGirdSty3 = opt_dict["styleGirdCirc3"]
        self.circGirdspin3 = opt_dict["circGirdspin3"]
        self.cbeigenp3 = opt_dict["cb_eigen_p3"]
        self.PolGirdColor3 = opt_dict["PolGirdColor3"]
        self.PoleGirdSymb3 = opt_dict["symbGirdPoles3"]
        self.poleGirdspin3 = opt_dict["poleGirdspin3"]

        self.countNodesNum = opt_dict["count_nodes"]
        self.perCent = opt_dict["percent"]
        self.interpMet = opt_dict["interpolation"]
        self.gridSpin = opt_dict["gridSpin"]
#        self.epsilSpin = opt_dict["epsilon"]
#        self.smootSpin = opt_dict["smoothing"]

        self.rbMinMax = opt_dict["minmax"]
        self.rbZeroMax = opt_dict["zeromax"]
        self.rbCustom = opt_dict["custom"]
        self.numContours = opt_dict["numcontours"]
        self.customcont = opt_dict["customcont"]

        self.ContStyle = opt_dict["contStyle"]
        self.contLwidths = opt_dict["contLws"]
        self.contColour = opt_dict["contColor"]
        self.contFilled = opt_dict["contFill"]
        self.addEdges = opt_dict["addedges"]
        self.colorMap = opt_dict["colormap"]
        self.contcolorMap = opt_dict["contcolormap"]
        self.rbSc = opt_dict["rbsc"] # single-colour contours
        self.rbCm = opt_dict["rbcm"] # gradient coloured contours
        self.antiAliased = opt_dict["antiAliased"]

        self.rbCossum = opt_dict["rbcossum"]
        self.ExpSpin = opt_dict["expSpin"]
        self.rbFisher = opt_dict["rbfisher"]
        self.KSpin = opt_dict["kSpin"]
        self.rbScarea = opt_dict["rbscarea"]
        self.AreaSpin = opt_dict["areaSpin"]
        self.rbScangle = opt_dict["rbscangle"]
        self.AngleSpin = opt_dict["angleSpin"]

# create scroled window
        self.scroll = wx.ScrolledWindow(self, -1, style=wx.TAB_TRAVERSAL)
        self.scroll.SetScrollRate(10, 10)

# create a notebook for prefs
        self.nb = wx.Notebook(self.scroll)#, size=(615,370))#, style=wx.TAB_TRAVERSAL)
        self.pgceigv = wx.Panel(self.nb, -1)# page 1, poles, great circles and eigenvectors
        self.cont = wx.Panel(self.nb, -1) # page 2, countours


        drawButton = wx.Button(self.scroll, wx.ID_OK, 'OK', size=(80, 30))
        closeButton = wx.Button(self.scroll, wx.ID_CANCEL, 'Cancel', size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.onClosePProps, id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_OK)
        self.SetEscapeId(wx.ID_CANCEL)



##---------------------
# widgets and layout, first panel (poles and great circles)

    # the wx.StaticBoxSizers must come before the things inside them or else it won't work properly on MacOSX
        poles_box = wx.StaticBoxSizer(wx.StaticBox(self.pgceigv, -1, ' Poles to Planes '), orient=wx.VERTICAL)
        circles_box = wx.StaticBoxSizer(wx.StaticBox(self.pgceigv, -1, ' Great Circles '), orient=wx.VERTICAL)
        confbox = wx.StaticBoxSizer(wx.StaticBox(self.pgceigv, -1, ' 95% Confidence Cone '), orient=wx.VERTICAL)
        eigen_box = wx.StaticBoxSizer(wx.StaticBox(self.pgceigv, -1, ' Eigenvectors '), orient=wx.VERTICAL)
        count_box = wx.StaticBoxSizer(wx.StaticBox(self.cont, -1, ' Counting '), orient=wx.VERTICAL)
        interp_box = wx.StaticBoxSizer(wx.StaticBox(self.cont, -1, ' Contouring '), orient=wx.VERTICAL)
        contgraph_box = wx.StaticBoxSizer(wx.StaticBox(self.cont, -1, ' Graphic properties '), orient=wx.VERTICAL)
        interval_box = wx.StaticBoxSizer(wx.StaticBox(self.cont, -1, ' Contour Intervals '), orient=wx.VERTICAL)

    # poles to planes
        txt_colPoles = wx.StaticText(self.pgceigv, -1, 'Colour')
        self.fcolPolesBtn = csel.ColourSelect(self.pgceigv, pos=(0, 0), size=(60, 20))
        self.fcolPolesBtn.SetColour(self.PolColor)
        
        txt_symbPoles = wx.StaticText(self.pgceigv, -1, 'Symbol')
        self.symbPoles = wx.ComboBox(self.pgceigv, -1, value=symbolList[symbols.index(self.PoleSymb)], choices=symbolList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        
        txt_polespin = wx.StaticText(self.pgceigv, -1, 'Size')
        self.polespin = FS.FloatSpin(self.pgceigv, -1, size=(60, -1), value=self.polespin, min_val=1, max_val=20, increment=0.50, digits=2)
        self.symbPoles.SetSelection(symbols.index(self.PoleSymb))

        grid2 = wx.FlexGridSizer(2, 3, 5, 5)
        grid2.Add(txt_colPoles,0, wx.LEFT|wx.TOP, 5)
        grid2.Add(txt_symbPoles,0, wx.LEFT|wx.TOP, 5)
        grid2.Add(txt_polespin,0, wx.LEFT|wx.TOP, 5)
        grid2.Add(self.fcolPolesBtn,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid2.Add(self.symbPoles,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid2.Add(self.polespin,0, wx.LEFT|wx.ALIGN_RIGHT, 5)
        poles_box.Add(grid2,0)

##---------------------
    #great circles
        txt_colCirc = wx.StaticText(self.pgceigv, -1, 'Colour')
        self.lcolCircBtn = csel.ColourSelect(self.pgceigv, pos=(0, 0), size=(60, 20))
        self.lcolCircBtn.SetColour(self.CircColor)
        
        txt_symbCirc = wx.StaticText(self.pgceigv, -1, 'Line Type')
        self.styleCirc = wx.ComboBox(self.pgceigv, -1, value=styleList[styles.index(self.CircSty)], choices=styleList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        
        txt_circspin = wx.StaticText(self.pgceigv, -1, 'Width')
        self.circspin = FS.FloatSpin(self.pgceigv, -1, size=(60, -1), value=self.circspin, min_val=0.1, max_val=5, increment=0.1, digits=1)
        self.styleCirc.SetSelection(styles.index(self.CircSty))

        grid4 = wx.FlexGridSizer(2, 3, 5, 5)
        grid4.Add(txt_colCirc,0, wx.LEFT|wx.TOP, 5)
        grid4.Add(txt_symbCirc,0, wx.LEFT|wx.TOP, 5)
        grid4.Add(txt_circspin,0, wx.LEFT|wx.TOP, 5)
        grid4.Add(self.lcolCircBtn,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid4.Add(self.styleCirc,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid4.Add(self.circspin,0, wx.LEFT|wx.ALIGN_RIGHT, 5)
        circles_box.Add(grid4,0)

        self.fcolPolesBtn.Bind(csel.EVT_COLOURSELECT, self.choosePolColor)
        self.lcolCircBtn.Bind(csel.EVT_COLOURSELECT, self.chooseCircColor)
        self.Bind(wx.EVT_COMBOBOX, self.choosePoleSymb, self.symbPoles )
        self.Bind(wx.EVT_COMBOBOX, self.chooseCircSty, self.styleCirc )

##---------------------
    # confidence cone
        txt_conCol = wx.StaticText(self.pgceigv, -1, 'Colour')
        self.concolCircBtn = csel.ColourSelect(self.pgceigv, pos=(0, 0), size=(60, 20))
        self.concolCircBtn.SetColour(self.conCircColor)
        
        txt_conCirc = wx.StaticText(self.pgceigv, -1, 'Line Type')
        self.constyleCirc = wx.ComboBox(self.pgceigv, -1, value=styleList[styles.index(self.conCircSty)], choices=styleList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        
        txt_conspin = wx.StaticText(self.pgceigv, -1, 'Width')
        self.conspin = FS.FloatSpin(self.pgceigv, -1, size=(60, -1), value=self.conspin, min_val=0.1, max_val=5, increment=0.1, digits=1)
        self.constyleCirc.SetSelection(styles.index(self.conCircSty))

        self.cb_conf = wx.CheckBox(self.pgceigv, -1, 'Plot Confidence Cone')
        self.cb_conf.SetValue(self.cbconf)
        grid15 = wx.BoxSizer(wx.VERTICAL)
        grid15.Add(self.cb_conf,0,wx.TOP,5)

        grid14 = wx.FlexGridSizer(2, 3, 5, 5)
        grid14.Add(txt_conCol,0, wx.LEFT|wx.TOP, 5)
        grid14.Add(txt_conCirc,0, wx.LEFT|wx.TOP, 5)
        grid14.Add(txt_conspin,0, wx.LEFT|wx.TOP, 5)
        grid14.Add(self.concolCircBtn,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid14.Add(self.constyleCirc,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid14.Add(self.conspin,0, wx.LEFT|wx.ALIGN_RIGHT, 5)
        confbox.Add(grid15,0)
        confbox.Add(grid14,0)

        self.concolCircBtn.Bind(csel.EVT_COLOURSELECT, self.chooseConCircColor)
        self.Bind(wx.EVT_COMBOBOX, self.chooseConCircSty, self.constyleCirc )



##---------------------
# widgets and layout, (eigenvectors)
    # eigenvector 1
        self.cb_eigen_gc1 = wx.CheckBox(self.pgceigv, -1, 'Great Circle')
        self.cb_eigen_gc1.SetValue(self.cbeigengc1)

        txt_colGirdCirc1 = wx.StaticText(self.pgceigv, -1, 'Colour')
        txt_symbGirdCirc1 = wx.StaticText(self.pgceigv, -1, 'Symbol')
        txt_circGirdspin1 = wx.StaticText(self.pgceigv, -1, 'Size')
        txt_eigen1 = wx.StaticText(self.pgceigv, -1, 'Eigenvector 1')
        txt_eigen2 = wx.StaticText(self.pgceigv, -1, 'Eigenvector 2')
        txt_eigen3 = wx.StaticText(self.pgceigv, -1, 'Eigenvector 3')

        self.lcolGirdCircBtn1 = csel.ColourSelect(self.pgceigv, pos=(0, 0), size=(60, 20))
        self.lcolGirdCircBtn1.SetColour(self.CircGirdColor1)
        self.styleGirdCirc1 = wx.ComboBox(self.pgceigv, -1, value=styleList[styles.index(self.CircGirdSty1)], choices=styleList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        self.circGirdspin1 = FS.FloatSpin(self.pgceigv, -1, size=(60, -1), value=self.circGirdspin1, min_val=0.1, max_val=5, increment=0.1, digits=1)
        self.styleGirdCirc1.SetSelection(styles.index(self.CircGirdSty1))

        self.cb_eigen_p1 = wx.CheckBox(self.pgceigv, -1, 'Pole')
        self.cb_eigen_p1.SetValue(self.cbeigenp1)
        self.fcolGirdPolesBtn1 = csel.ColourSelect(self.pgceigv, pos=(0, 0), size=(60, 20))
        self.fcolGirdPolesBtn1.SetColour(self.PolGirdColor1)
        self.symbGirdPoles1 = wx.ComboBox(self.pgceigv, -1, value=symbolList[symbols.index(self.PoleGirdSymb1)], choices=symbolList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        self.poleGirdspin1 = FS.FloatSpin(self.pgceigv, -1, size=(60, -1), value=self.poleGirdspin1, min_val=1, max_val=20, increment=0.5, digits=1)
        self.symbGirdPoles1.SetSelection(symbols.index(self.PoleGirdSymb1))

        grid6 = wx.FlexGridSizer(9, 4, 5, 5)
        grid6.Add(txt_eigen1,0, wx.LEFT|wx.TOP, 5) #
        grid6.Add(txt_colGirdCirc1,0, wx.LEFT|wx.ALIGN_CENTER, 5)
        grid6.Add(txt_symbGirdCirc1,0, wx.LEFT|wx.ALIGN_CENTER, 5)
        grid6.Add(txt_circGirdspin1,0, wx.LEFT|wx.ALIGN_CENTER, 5) #

        grid6.Add(self.cb_eigen_gc1,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5) #, wx.ALIGN_CENTER, 5)
        grid6.Add(self.lcolGirdCircBtn1,0, wx.LEFT, 5) #|wx.ALIGN_CENTER, 5)
        grid6.Add(self.styleGirdCirc1,0, wx.LEFT, 5) #|wx.ALIGN_CENTER, 5)
        grid6.Add(self.circGirdspin1,0, wx.LEFT, 5) #|wx.ALIGN_CENTER, 5)

        grid6.Add(self.cb_eigen_p1,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5) #|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.fcolGirdPolesBtn1,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.symbGirdPoles1,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.poleGirdspin1,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT, 5)
        
        self.lcolGirdCircBtn1.Bind(csel.EVT_COLOURSELECT, self.chooseCircGirdColor1)
        self.Bind(wx.EVT_COMBOBOX, self.chooseCircGirdSty1, self.styleGirdCirc1 )
        self.fcolGirdPolesBtn1.Bind(csel.EVT_COLOURSELECT, self.choosePolGirdColor1)
        self.Bind(wx.EVT_COMBOBOX, self.choosePoleGirdSymb1, self.symbGirdPoles1 )

##---------------------
    # eigenvector 2
        self.cb_eigen_gc2 = wx.CheckBox(self.pgceigv, -1, 'Great circle')
        self.cb_eigen_gc2.SetValue(self.cbeigengc2)
        
        self.lcolGirdCircBtn2 = csel.ColourSelect(self.pgceigv, pos=(0, 0), size=(60, 20))
        self.lcolGirdCircBtn2.SetColour(self.CircGirdColor2)
        
        self.styleGirdCirc2 = wx.ComboBox(self.pgceigv, -1, value=styleList[styles.index(self.CircGirdSty2)], choices=styleList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        self.circGirdspin2 = FS.FloatSpin(self.pgceigv, -1, size=(60, -1), value=self.circGirdspin2, min_val=0.1, max_val=5, increment=0.1, digits=1)
        self.styleGirdCirc2.SetSelection(styles.index(self.CircGirdSty2))

        self.cb_eigen_p2 = wx.CheckBox(self.pgceigv, -1, 'Pole')
        self.cb_eigen_p2.SetValue(self.cbeigenp2)
        
        self.fcolGirdPolesBtn2 = csel.ColourSelect(self.pgceigv, pos=(0, 0), size=(60, 20))
        self.fcolGirdPolesBtn2.SetColour(self.PolGirdColor2)
        
        self.symbGirdPoles2 = wx.ComboBox(self.pgceigv, -1, value=symbolList[symbols.index(self.PoleGirdSymb2)], choices=symbolList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        self.poleGirdspin2 = FS.FloatSpin(self.pgceigv, -1, size=(60, -1), value=self.poleGirdspin2, min_val=1, max_val=20, increment=0.5, digits=1)
        self.symbGirdPoles2.SetSelection(symbols.index(self.PoleGirdSymb2))

        grid6.Add(txt_eigen2,0, wx.LEFT|wx.TOP, 5) #
        grid6.Add((2,2))
        grid6.Add((2,2))
        grid6.Add((2,2))
        grid6.Add(self.cb_eigen_gc2,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.lcolGirdCircBtn2,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.styleGirdCirc2,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.circGirdspin2,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT, 5)

        grid6.Add(self.cb_eigen_p2,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.fcolGirdPolesBtn2,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.symbGirdPoles2,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.poleGirdspin2,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT, 5)

        self.lcolGirdCircBtn2.Bind(csel.EVT_COLOURSELECT, self.chooseCircGirdColor2)
        self.Bind(wx.EVT_COMBOBOX, self.chooseCircGirdSty2, self.styleGirdCirc2 )
        self.fcolGirdPolesBtn2.Bind(csel.EVT_COLOURSELECT, self.choosePolGirdColor2)
        self.Bind(wx.EVT_COMBOBOX, self.choosePoleGirdSymb2, self.symbGirdPoles2 )

##---------------------
    # eigenvector 3
        self.cb_eigen_gc3 = wx.CheckBox(self.pgceigv, -1, 'Great circle')
        self.cb_eigen_gc3.SetValue(self.cbeigengc3)

        self.lcolGirdCircBtn3 = csel.ColourSelect(self.pgceigv, pos=(0, 0), size=(60, 20))
        self.lcolGirdCircBtn3.SetColour(self.CircGirdColor3)
        
        self.styleGirdCirc3 = wx.ComboBox(self.pgceigv, -1, value=styleList[styles.index(self.CircGirdSty3)], choices=styleList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        self.circGirdspin3 = FS.FloatSpin(self.pgceigv, -1, size=(60, -1), value=self.circGirdspin3, min_val=0.1, max_val=5, increment=0.1, digits=1)
        self.styleGirdCirc3.SetSelection(styles.index(self.CircGirdSty3))

        self.cb_eigen_p3 = wx.CheckBox(self.pgceigv, -1, 'Pole')
        self.cb_eigen_p3.SetValue(self.cbeigenp3)
        self.fcolGirdPolesBtn3 = csel.ColourSelect(self.pgceigv, pos=(0, 0), size=(60, 20))
        self.fcolGirdPolesBtn3.SetColour(self.PolGirdColor3)
        
        self.symbGirdPoles3 = wx.ComboBox(self.pgceigv, -1, value=symbolList[symbols.index(self.PoleGirdSymb3)], choices=symbolList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        self.poleGirdspin3 = FS.FloatSpin(self.pgceigv, -1, size=(60, -1), value=self.poleGirdspin3, min_val=1, max_val=20, increment=0.5, digits=1)
        self.symbGirdPoles3.SetSelection(symbols.index(self.PoleGirdSymb3))

        grid6.Add(txt_eigen3,0, wx.LEFT|wx.TOP, 5) #
        grid6.Add((2,2))
        grid6.Add((2,2))
        grid6.Add((2,2))
        grid6.Add(self.cb_eigen_gc3,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.lcolGirdCircBtn3,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.styleGirdCirc3,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.circGirdspin3,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT, 5)

        grid6.Add(self.cb_eigen_p3,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.fcolGirdPolesBtn3,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.symbGirdPoles3,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.poleGirdspin3,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT, 5)

        eigen_box.Add(grid6,0)

        self.lcolGirdCircBtn3.Bind(csel.EVT_COLOURSELECT, self.chooseCircGirdColor3)
        self.Bind(wx.EVT_COMBOBOX, self.chooseCircGirdSty3, self.styleGirdCirc3 )
        self.fcolGirdPolesBtn3.Bind(csel.EVT_COLOURSELECT, self.choosePolGirdColor3)
        self.Bind(wx.EVT_COMBOBOX, self.choosePoleGirdSymb3, self.symbGirdPoles3 )

    #layout of widgets
        pgcbox = wx.FlexGridSizer(3, 1, 5, 5)
        pgcbox.Add(poles_box,0,wx.ALL,5)
        pgcbox.Add(circles_box,0,wx.ALL,5)
        pgcbox.Add(confbox,0,wx.ALL,5)

        eigbox = wx.BoxSizer(wx.VERTICAL)
        eigbox.Add(eigen_box,0,wx.ALL,5)

        pgceigvbox = wx.FlexGridSizer(1, 2, 5, 5)
        pgceigvbox.Add(pgcbox,0,wx.ALL,5)
        pgceigvbox.Add(eigbox,0,wx.ALL,5)
        self.pgceigv.SetSizer(pgceigvbox)


##---------------------
# widgets and layout, third panel (contours)
    # counting options
        txt_cntNodes = wx.StaticText(self.cont, -1, 'Grid Density')#'Counting Nodes')

        self.countNodes = wx.ComboBox(self.cont, -1, value=countNodesList[countNodes.index(self.countNodesNum)], choices=countNodesList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(90, -1))
        self.countNodes.SetSelection(countNodes.index(self.countNodesNum))
        self.percent = wx.CheckBox(self.cont, -1, 'Percentage')
        self.percent.SetValue(self.perCent)

        grid7 = wx.FlexGridSizer(1, 3, 5, 5)
        grid7.Add(txt_cntNodes,0, wx.TOP|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid7.Add(self.countNodes,0, wx.LEFT|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid7.Add(self.percent,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)


        self.rbcossum = wx.RadioButton(self.cont, -1, 'Cossine sums', style=wx.RB_GROUP)
        self.rbcossum.SetValue(self.rbCossum)
        self.rbfisher = wx.RadioButton(self.cont, -1, 'Gaussian distribution')
        self.rbfisher.SetValue(self.rbFisher)
        self.rbscarea = wx.RadioButton(self.cont, -1, 'Small circle count')
        self.rbscarea.SetValue(self.rbScarea)
        self.rbscangle = wx.RadioButton(self.cont, -1, 'Small circle count')
        self.rbscangle.SetValue(self.rbScangle)
        txt_expoent = wx.StaticText(self.cont, -1, '(expoent)')
        txt_paramk = wx.StaticText(self.cont, -1, '(K param.)')
        txt_area = wx.StaticText(self.cont, -1, '(% area)')
        txt_angle = wx.StaticText(self.cont, -1, '(angle)')
        self.expSpin = FS.FloatSpin(self.cont, -1, size=(60, -1), value=self.ExpSpin, min_val=1, max_val=999, increment=1, digits=0)
        self.kSpin = FS.FloatSpin(self.cont, -1, size=(60, -1), value=self.KSpin, min_val=1, max_val=999, increment=1, digits=0)
        self.areaSpin = FS.FloatSpin(self.cont, -1, size=(60, -1), value=self.AreaSpin, min_val=0.50, max_val=25, increment=0.50, digits=1)
        self.angleSpin = FS.FloatSpin(self.cont, -1, size=(60, -1), value=self.AngleSpin, min_val=0.50, max_val=45, increment=0.50, digits=1)

        grid7a = wx.FlexGridSizer(4, 3, 5, 5)
        grid7a.Add(self.rbfisher,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid7a.Add(txt_paramk,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid7a.Add(self.kSpin,0, wx.LEFT|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)

        grid7a.Add(self.rbcossum,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid7a.Add(txt_expoent,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid7a.Add(self.expSpin,0, wx.LEFT|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)

        grid7a.Add(self.rbscarea,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid7a.Add(txt_area,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid7a.Add(self.areaSpin,0, wx.LEFT|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)

        grid7a.Add(self.rbscangle,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid7a.Add(txt_angle,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid7a.Add(self.angleSpin,0, wx.LEFT|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)


        self.Bind(wx.EVT_COMBOBOX, self.chooseCountNodes, self.countNodes )

        count_box.Add(grid7,0)
        count_box.Add(grid7a,0, wx.TOP, 5)

##---------------------
    # interpolation options
        txt_method = wx.StaticText(self.cont, -1, 'Method')
        txt_ngrid = wx.StaticText(self.cont, -1, 'Steps')
#        txt_epsil = wx.StaticText(self.cont, -1, 'Epsilon')
#        txt_smoot = wx.StaticText(self.cont, -1, 'Smoothing')

        self.interps = wx.ComboBox(self.cont, -1, value=interpList[interpList.index(self.interpMet)], choices=interpList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(185, -1))
        self.interps.SetSelection(interpList.index(self.interpMet))

        self.gridSpin = FS.FloatSpin(self.cont, -1, size=(60, -1), value=self.gridSpin, min_val=10, max_val=1000, increment=10, digits=0)
#        self.epsilSpin = FS.FloatSpin(self.cont, -1, size=(60, -1), value=self.epsilSpin, min_val=0.001, max_val=1, increment=0.01, digits=3)
#        self.smootSpin = FS.FloatSpin(self.cont, -1, size=(60, -1), value=self.smootSpin, min_val=0, max_val=1, increment=0.001, digits=3)


        grid8 = wx.FlexGridSizer(1, 2, 5, 5)
        grid8.Add(txt_method,0, wx.LEFT|wx.TOP|wx.ALIGN_CENTER_VERTICAL, 5)
        grid8.Add(self.interps,0, wx.LEFT|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)

        grid8a = wx.FlexGridSizer(3, 2, 5, 5)
        grid8a.Add(txt_ngrid,0, wx.LEFT|wx.TOP|wx.ALIGN_CENTER_VERTICAL, 5)
        grid8a.Add(self.gridSpin,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
#        grid8a.Add(txt_epsil,0, wx.LEFT|wx.TOP|wx.ALIGN_CENTER_VERTICAL, 5)
#        grid8a.Add(self.epsilSpin,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
#        grid8a.Add(txt_smoot,0, wx.LEFT|wx.TOP|wx.ALIGN_CENTER_VERTICAL, 5)
#        grid8a.Add(self.smootSpin,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)

        self.Bind(wx.EVT_COMBOBOX, self.chooseInterps, self.interps )

        interp_box.Add(grid8,0)
        interp_box.Add(grid8a,0,wx.TOP, 5)

##---------------------
    # graphic options
        txt_csymb = wx.StaticText(self.cont, -1, 'Style')
        txt_cwdt = wx.StaticText(self.cont, -1, 'Width')
        self.contSty = wx.ComboBox(self.cont, -1, value=styleList[styles.index(self.ContStyle)], choices=styleList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        self.contSty.SetSelection(styles.index(self.ContStyle))
        self.contLws = FS.FloatSpin(self.cont, -1, size=(60, -1), value=self.contLwidths, min_val=0.1, max_val=5, increment=0.1, digits=1)
        
        self.contColBtn = csel.ColourSelect(self.cont, pos=(0, 0), size=(60, 20))
        self.contColBtn.SetColour(self.contColour)
        
        self.cont_fill = wx.CheckBox(self.cont, -1, 'Fill contours')
        self.cont_fill.SetValue(self.contFilled)
        self.add_edges = wx.CheckBox(self.cont, -1, 'Draw contours over filled')
        self.add_edges.SetValue(self.addEdges)
        self.antialiased = wx.CheckBox(self.cont, -1, 'Antialiased')
        self.antialiased.SetValue(self.antiAliased)

        self.contcolorMapsChoice = wx.ComboBox(self.cont, -1, value=mapsList[mapsList.index(self.contcolorMap)], choices=mapsList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(105, -1))
        self.contcolorMapsChoice.SetSelection(mapsList.index(self.contcolorMap))
        self.contcolorMapsChoice.Bind(wx.EVT_COMBOBOX, self.OnSelectcontColorMap)

        self.colorMapsChoice = wx.ComboBox(self.cont, -1, value=mapsList[mapsList.index(self.colorMap)], choices=mapsList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(105, -1))
        self.colorMapsChoice.SetSelection(mapsList.index(self.colorMap))
        self.colorMapsChoice.Bind(wx.EVT_COMBOBOX, self.OnSelectColorMap)

        self.rbsc = wx.RadioButton(self.cont, -1, 'Line Colour', style=wx.RB_GROUP)
        self.rbcm = wx.RadioButton(self.cont, -1, 'Line Gradient')
        self.rbsc.SetValue(self.rbSc)
        self.rbcm.SetValue(self.rbCm)
        self.contColBtn.Bind(csel.EVT_COLOURSELECT, self.chooseContCol)
        self.Bind(wx.EVT_COMBOBOX, self.chooseContSty, self.contSty )

        grid9 = wx.FlexGridSizer(4, 4, 5, 5)
        grid9.Add(self.rbsc,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid9.Add(self.contColBtn,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid9.Add(txt_csymb,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid9.Add(self.contSty,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)

        grid9.Add(self.rbcm,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid9.Add(self.contcolorMapsChoice,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid9.Add(txt_cwdt,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid9.Add(self.contLws,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)

        grid9.Add(self.cont_fill,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid9.Add(self.colorMapsChoice,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid9.Add((2,2))
        grid9.Add((2,2))

        grid9a = wx.FlexGridSizer(2, 1, 5, 5)
        grid9a.Add(self.antialiased,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid9a.Add(self.add_edges,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)

        contgraph_box.Add(grid9,0)
        contgraph_box.Add(grid9a,0, wx.TOP, 5)

##---------------------
# interval options

        self.rbminmax = wx.RadioButton(self.cont, -1, 'From minimum to maximum', style=wx.RB_GROUP)
        self.rbzeromax = wx.RadioButton(self.cont, -1, 'From zero to maximum')
        self.rbcustom = wx.RadioButton(self.cont, -1, 'Custom list')
        self.rbminmax.SetValue(self.rbMinMax)
        self.rbzeromax.SetValue(self.rbZeroMax)
        self.rbcustom.SetValue(self.rbCustom)
        txt_numcont = wx.StaticText(self.cont, -1, 'Number of contours')
        self.numcontours = FS.FloatSpin(self.cont, -1, size=(60, -1), value=self.numContours, min_val=1, max_val=50, increment=1, digits=0)
        self.control1 = wx.TextCtrl(self.cont, -1, size=(203,-1))
        self.control1.SetValue(self.customcont)

        grid10 = wx.FlexGridSizer(2, 1, 5, 5)
        grid10.Add(self.rbminmax,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid10.Add(self.rbzeromax,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid10a = wx.FlexGridSizer(2, 2, 5, 5)
        grid10a.Add(txt_numcont,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid10a.Add(self.numcontours,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid10a.Add(self.rbcustom,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid10a.Add(self.control1,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)

        interval_box.Add(grid10,0, wx.TOP, 5)
        interval_box.Add(grid10a,0, wx.TOP, 5)

##---------------------
# set the contour panel layout
        contbox = wx.FlexGridSizer(2, 2, 5, 5)
        contbox.Add(contgraph_box,0,wx.ALL,5)
        contbox.Add(count_box,0,wx.ALL,5)
        contbox.Add(interval_box,0,wx.ALL,5)
        contbox.Add(interp_box,0,wx.ALL,5)
        self.cont.SetSizer(contbox)

##---------------------
        dlgbox = wx.BoxSizer(wx.VERTICAL) 
        btnbox = wx.BoxSizer(wx.HORIZONTAL)
        nbbox = wx.BoxSizer(wx.VERTICAL) 

        self.nb.AddPage(self.pgceigv, "Poles / Great Circles / Eigenvectors")
        self.nb.AddPage(self.cont, "Contours")

        btnbox.Add(drawButton, 0)
        btnbox.Add(closeButton, 0, wx.LEFT, 10)

        nbbox.Add(self.nb, 0, wx.ALL|wx.EXPAND,5) # add notebook to sizer
        nbbox.Add(btnbox, 0, wx.ALL|wx.ALIGN_CENTER, 5) # add OK and Cancel btns to sizer

        self.scroll.SetSizer(nbbox)
        nbbox.Fit(self.scroll)
        nbbox.SetSizeHints(self.scroll)

        dlgbox.Add(self.scroll, 0, wx.EXPAND,0)
        self.SetSizer(dlgbox)
        dlgbox.Fit(self)
        dlgbox.SetSizeHints(self)

        self.SetFocus()

##-----------------------------------------------------------------------------
    def onClosePProps(self, event):
        self.Destroy()

##-----------------------------------------------------------------------------

#choose poles to planes color dialog. Get color datas as hex, for matplotlib
    def choosePolColor(self,event):
        """Colour dialog for Poles Fill colour"""
        self.PolColor = self.fcolPolesBtn.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)

#choose poles to planes symbol
    def choosePoleSymb(self,event):
        """Choose poles to planes simbol"""
        symb1 = self.symbPoles.GetValue()
        self.PoleSymb = symbols[symbolList.index(symb1)]
#        print self.PoleSymb

#choose great circle line color dialog
    def chooseCircColor(self,event):
        """Colour dialog for Line colour"""
        self.CircColor = self.lcolCircBtn.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)

#choose great circle line style
    def chooseCircSty(self,event):
        """Choose poles to planes simbol"""
        sty1 = self.styleCirc.GetValue()
        self.CircSty = styles[styleList.index(sty1)]
#        print self.CircSty
##-----------------------------------------------------------------------------

#choose confidence cone line color dialog
    def chooseConCircColor(self,event):
        """Colour dialog for Line colour"""
        self.conCircColor = self.concolCircBtn.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)

#choose confidence cone line style
    def chooseConCircSty(self,event):
        """Choose poles to planes simbol"""
        sty1 = self.constyleCirc.GetValue()
        self.conCircSty = styles[styleList.index(sty1)]


##-----------------------------------------------------------------------------

#choose girdle line color dialog - vector 1
    def chooseCircGirdColor1(self,event):
        """Colour dialog for Girdle colour"""
        self.CircGirdColor1 = self.lcolGirdCircBtn1.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)

#choose girdle line color dialog - vector 2
    def chooseCircGirdColor2(self,event):
        """Colour dialog for Girdle colour"""
        self.CircGirdColor2 = self.lcolGirdCircBtn2.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)

#choose girdle line color dialog - vector 3
    def chooseCircGirdColor3(self,event):
        """Colour dialog for Girdle colour"""
        self.CircGirdColor3 = self.lcolGirdCircBtn3.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)

#choose girdle great circle line style - vector 1
    def chooseCircGirdSty1(self,event):
        """Choose poles to planes simbol"""
        sty1 = self.styleGirdCirc1.GetValue()
        self.CircGirdSty1 = styles[styleList.index(sty1)]

#choose girdle great circle line style - vector 2
    def chooseCircGirdSty2(self,event):
        """Choose poles to planes simbol"""
        sty1 = self.styleGirdCirc2.GetValue()
        self.CircGirdSty2 = styles[styleList.index(sty1)]

#choose girdle great circle line style - vector 3
    def chooseCircGirdSty3(self,event):
        """Choose poles to planes simbol"""
        sty1 = self.styleGirdCirc3.GetValue()
        self.CircGirdSty3 = styles[styleList.index(sty1)]

#choose pole to girdle color dialog. - vector 1
    def choosePolGirdColor1(self,event):
        """Colour dialog for Poles Fill colour"""
        self.PolGirdColor1 = self.fcolGirdPolesBtn1.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)

#choose pole to girdle color dialog. - vector 2
    def choosePolGirdColor2(self,event):
        """Colour dialog for Poles Fill colour"""
        self.PolGirdColor2 = self.fcolGirdPolesBtn2.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)

#choose pole to girdle color dialog. - vector 3
    def choosePolGirdColor3(self,event):
        """Colour dialog for Poles Fill colour"""
        self.PolGirdColor3 = self.fcolGirdPolesBtn3.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)

#choose pole to girdle symbol - vector 1
    def choosePoleGirdSymb1(self,event):
        """Choose poles to planes simbol"""
        symb1 = self.symbGirdPoles1.GetValue()
        self.PoleGirdSymb1 = symbols[symbolList.index(symb1)]

#choose pole to girdle symbol - vector 2
    def choosePoleGirdSymb2(self,event):
        """Choose poles to planes simbol"""
        symb1 = self.symbGirdPoles2.GetValue()
        self.PoleGirdSymb2 = symbols[symbolList.index(symb1)]

#choose pole to girdle symbol - vector 3
    def choosePoleGirdSymb3(self,event):
        """Choose poles to planes simbol"""
        symb1 = self.symbGirdPoles3.GetValue()
        self.PoleGirdSymb3 = symbols[symbolList.index(symb1)]

#-----------------------------------------------------------------------------
#choose number of nodes for counting
    def chooseCountNodes(self,event):
        """Choose number of counting nodes"""
        cnt = self.countNodes.GetValue()
        self.countNodesNum = countNodes[countNodesList.index(cnt)]

#choose interpolation method
    def chooseInterps(self,event):
        """Choose interpolation method"""
        interp = self.interps.GetValue()
        self.interpMet = interpList[interpList.index(interp)]

#choose contour lines color dialog. Get color datas as hex, for matplotlib
    def chooseContCol(self,event):
        """Contour lines colour dialog"""
        self.contColour = self.contColBtn.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)

#choose contour line style 
    def chooseContSty(self,event):
        """Choose style of contour lines"""
        sty1 = self.contSty.GetValue()
        self.ContStyle = styles[styleList.index(sty1)]

#choose colormap for fill
    def OnSelectColorMap(self, evt=None):
        ''' Handles the selection of a color map from a choice box. '''
        cmap = self.colorMapsChoice.GetValue()
        self.colorMap = mapsList[mapsList.index(cmap)] #self.colorMapsChoice.GetStringSelection()


#choose colormap for contour lines 
    def OnSelectcontColorMap(self, evt=None):
        ''' Handles the selection of a color map from a choice box. '''
        cmap = self.contcolorMapsChoice.GetValue()
        self.contcolorMap = mapsList[mapsList.index(cmap)] #self.colorMapsChoice.GetStringSelection()


#-----------------------------------------------------------------------------
# return graphic properties of planar data
    def onPlanProps(self):
        val = self.ShowModal()
        if val == wx.ID_OK:
            return self.PolColor, self.PoleSymb, self.polespin.GetValue(),\
            self.CircColor, self.CircSty, self.circspin.GetValue(), \
            self.cb_eigen_gc1.GetValue(), self.CircGirdColor1, self.CircGirdSty1, self.circGirdspin1.GetValue(), \
            self.cb_eigen_p1.GetValue(), self.PolGirdColor1, self.PoleGirdSymb1, self.poleGirdspin1.GetValue(), \
            self.cb_eigen_gc2.GetValue(), self.CircGirdColor2, self.CircGirdSty2, self.circGirdspin2.GetValue(), \
            self.cb_eigen_p2.GetValue(), self.PolGirdColor2, self.PoleGirdSymb2, self.poleGirdspin2.GetValue(), \
            self.cb_eigen_gc3.GetValue(), self.CircGirdColor3, self.CircGirdSty3, self.circGirdspin3.GetValue(), \
            self.cb_eigen_p3.GetValue(), self.PolGirdColor3, self.PoleGirdSymb3, self.poleGirdspin3.GetValue(), \
            self.countNodesNum, self.percent.GetValue(), self.interpMet, self.gridSpin.GetValue(), \
            self.ContStyle, self.contColour, \
            self.cont_fill.GetValue(), self.contLws.GetValue(), self.colorMap, self.contcolorMap, self.add_edges.GetValue(), \
            self.rbsc.GetValue(), self.rbcm.GetValue(), self.antialiased.GetValue(), self.rbminmax.GetValue(), \
            self.rbzeromax.GetValue(), self.numcontours.GetValue(), self.rbcustom.GetValue(), self.control1.GetValue(), \
            self.rbcossum.GetValue(), self.expSpin.GetValue(), self.rbfisher.GetValue(), self.kSpin.GetValue(), \
            self.rbscarea.GetValue(), self.areaSpin.GetValue(), self.rbscangle.GetValue(), self.angleSpin.GetValue(), \
            self.conCircSty, self.conCircColor, self.conspin.GetValue(), self.cb_conf.GetValue()
        else:
            return None

        dlg.Destroy()

#self.epsilSpin.GetValue(), self.smootSpin.GetValue(), 


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

class LinearOptions(wx.Dialog):
    def __init__(self, parent, id, title, opt_dict):
        wx.Dialog.__init__(self, parent, id, title)#, size=(340, 365))

# default list of properties for linear data

#        idx = opt_dict[0]
#        name = opt_dict[1]
        self.LinColor = opt_dict["LinColor"]
        self.LineSymb = opt_dict["LineSymb"]
        self.polespin = opt_dict["linespin"]

        self.cbconf  = opt_dict["cb_conf"]
        self.conCircColor = opt_dict["conCircColor"]
        self.conCircSty = opt_dict["conCircSty"]
        self.conspin = opt_dict["conspin"]

        self.cbeigengc1 = opt_dict["cb_eigen_gc1"]
        self.CircGirdColor1 = opt_dict["CircGirdColor1"]
        self.CircGirdSty1 = opt_dict["styleGirdCirc1"]
        self.circGirdspin1 = opt_dict["circGirdspin1"]
        self.cbeigenp1 = opt_dict["cb_eigen_p1"]
        self.PolGirdColor1 = opt_dict["PolGirdColor1"]
        self.PoleGirdSymb1 = opt_dict["symbGirdPoles1"]
        self.poleGirdspin1 = opt_dict["poleGirdspin1"]

        self.cbeigengc2 = opt_dict["cb_eigen_gc2"]
        self.CircGirdColor2 = opt_dict["CircGirdColor2"]
        self.CircGirdSty2 = opt_dict["styleGirdCirc2"]
        self.circGirdspin2 = opt_dict["circGirdspin2"]
        self.cbeigenp2 = opt_dict["cb_eigen_p2"]
        self.PolGirdColor2 = opt_dict["PolGirdColor2"]
        self.PoleGirdSymb2 = opt_dict["symbGirdPoles2"]
        self.poleGirdspin2 = opt_dict["poleGirdspin2"]

        self.cbeigengc3 = opt_dict["cb_eigen_gc3"]
        self.CircGirdColor3 = opt_dict["CircGirdColor3"]
        self.CircGirdSty3 = opt_dict["styleGirdCirc3"]
        self.circGirdspin3 = opt_dict["circGirdspin3"]
        self.cbeigenp3 = opt_dict["cb_eigen_p3"]
        self.PolGirdColor3 = opt_dict["PolGirdColor3"]
        self.PoleGirdSymb3 = opt_dict["symbGirdPoles3"]
        self.poleGirdspin3 = opt_dict["poleGirdspin3"]

        self.countNodesNum = opt_dict["count_nodes"]
        self.perCent = opt_dict["percent"]
        self.interpMet = opt_dict["interpolation"]
        self.gridSpin = opt_dict["gridSpin"]
#        self.epsilSpin = opt_dict["epsilon"]
#        self.smootSpin = opt_dict["smoothing"]

        self.rbMinMax = opt_dict["minmax"]
        self.rbZeroMax = opt_dict["zeromax"]
        self.rbCustom = opt_dict["custom"]
        self.numContours = opt_dict["numcontours"]
        self.customcont = opt_dict["customcont"]

        self.ContStyle = opt_dict["contStyle"]
        self.contLwidths = opt_dict["contLws"]
        self.contColour = opt_dict["contColor"]
        self.contFilled = opt_dict["contFill"]
        self.addEdges = opt_dict["addedges"]
        self.colorMap = opt_dict["colormap"]
        self.contcolorMap = opt_dict["contcolormap"]
        self.rbSc = opt_dict["rbsc"]
        self.rbCm = opt_dict["rbcm"]
        self.antiAliased = opt_dict["antiAliased"]

        self.rbCossum = opt_dict["rbcossum"]
        self.ExpSpin = opt_dict["expSpin"]
        self.rbFisher = opt_dict["rbfisher"]
        self.KSpin = opt_dict["kSpin"]
        self.rbScarea = opt_dict["rbscarea"]
        self.AreaSpin = opt_dict["areaSpin"]
        self.rbScangle = opt_dict["rbscangle"]
        self.AngleSpin = opt_dict["angleSpin"]

# create scroled window
        self.scroll = wx.ScrolledWindow(self, -1, style=wx.TAB_TRAVERSAL)
        self.scroll.SetScrollRate(10, 10)

# create a notebook for prefs
        self.nb = wx.Notebook(self.scroll)#, size=(615,370))#, style=wx.TAB_TRAVERSAL)
        self.pgceigv = wx.Panel(self.nb, -1)# page 1, poles and eigenvectors
        self.cont = wx.Panel(self.nb, -1) # page 2, countours


        drawButton = wx.Button(self.scroll, wx.ID_OK, 'OK', size=(80, 30))
        closeButton = wx.Button(self.scroll, wx.ID_CANCEL, 'Cancel', size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.onCloseLProps, id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_OK)
        self.SetEscapeId(wx.ID_CANCEL)

##---------------------
# widgets and layout, first panel (poles and great circles)
    # the wx.StaticBoxSizers must come before the things inside them or else it won't work properly on MacOSX
        lines_box = wx.StaticBoxSizer(wx.StaticBox(self.pgceigv, -1, 'Poles to Lines'), orient=wx.VERTICAL)
        confbox = wx.StaticBoxSizer(wx.StaticBox(self.pgceigv, -1, ' 95% Confidence Cone '), orient=wx.VERTICAL)
        eigen_box = wx.StaticBoxSizer(wx.StaticBox(self.pgceigv, -1, ' Eigenvectors '), orient=wx.VERTICAL)
        count_box = wx.StaticBoxSizer(wx.StaticBox(self.cont, -1, ' Counting '), orient=wx.VERTICAL)
        interp_box = wx.StaticBoxSizer(wx.StaticBox(self.cont, -1, ' Contouring '), orient=wx.VERTICAL)
        contgraph_box = wx.StaticBoxSizer(wx.StaticBox(self.cont, -1, ' Graphic properties '), orient=wx.VERTICAL)
        interval_box = wx.StaticBoxSizer(wx.StaticBox(self.cont, -1, ' Contour Intervals '), orient=wx.VERTICAL)


    # poles to lines
        txt_colLines = wx.StaticText(self.pgceigv, -1, 'Colour')
        self.fcolLinesBtn = csel.ColourSelect(self.pgceigv, pos=(0, 0), size=(60, 20))
        self.fcolLinesBtn.SetColour(self.LinColor)

        txt_symbLines = wx.StaticText(self.pgceigv, -1, 'Symbol')
        self.symbLines = wx.ComboBox(self.pgceigv, -1, value=symbolList[symbols.index(self.LineSymb)], choices=symbolList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        self.symbLines.SetSelection(symbols.index(self.LineSymb))

        txt_linespin = wx.StaticText(self.pgceigv, -1, 'Size')
        self.linespin = FS.FloatSpin(self.pgceigv, -1, size=(60, -1), value=self.polespin, min_val=1, max_val=20, increment=0.5, digits=1)

        grid3 = wx.FlexGridSizer(2, 3, 5, 5)
        grid3.Add(txt_colLines,0, wx.LEFT|wx.TOP, 5)
        grid3.Add(txt_symbLines,0, wx.LEFT|wx.TOP, 5)
        grid3.Add(txt_linespin,0, wx.LEFT|wx.TOP, 5)
        grid3.Add(self.fcolLinesBtn,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid3.Add(self.symbLines,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid3.Add(self.linespin,0, wx.LEFT|wx.ALIGN_RIGHT, 5)
        lines_box.Add(grid3,0)

        self.fcolLinesBtn.Bind(csel.EVT_COLOURSELECT, self.chooseLinColor)
        self.Bind(wx.EVT_COMBOBOX, self.chooseLineSymb, self.symbLines )

###---------------------
##         confidence cone of line poles
        txt_conCol = wx.StaticText(self.pgceigv, -1, 'Colour')
        self.concolCircBtn = csel.ColourSelect(self.pgceigv, pos=(0, 0), size=(60, 20))
        self.concolCircBtn.SetColour(self.conCircColor)

        txt_conCirc = wx.StaticText(self.pgceigv, -1, 'Line Type')
        self.constyleCirc = wx.ComboBox(self.pgceigv, -1, value=styleList[styles.index(self.conCircSty)], choices=styleList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        self.constyleCirc.SetSelection(styles.index(self.conCircSty))

        txt_conspin = wx.StaticText(self.pgceigv, -1, 'Width')
        self.conspin = FS.FloatSpin(self.pgceigv, -1, size=(60, -1), value=self.conspin, min_val=0.1, max_val=5, increment=0.1, digits=1)

        self.cb_conf = wx.CheckBox(self.pgceigv, -1, 'Plot Confidence Cone')
        self.cb_conf.SetValue(self.cbconf)
        grid15 = wx.BoxSizer(wx.VERTICAL)
        grid15.Add(self.cb_conf,0,wx.TOP,5)

        grid14 = wx.FlexGridSizer(2, 3, 5, 5)
        grid14.Add(txt_conCol,0, wx.LEFT|wx.TOP, 5)
        grid14.Add(txt_conCirc,0, wx.LEFT|wx.TOP, 5)
        grid14.Add(txt_conspin,0, wx.LEFT|wx.TOP, 5)
        grid14.Add(self.concolCircBtn,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid14.Add(self.constyleCirc,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid14.Add(self.conspin,0, wx.LEFT|wx.ALIGN_RIGHT, 5)
        confbox.Add(grid15,0)
        confbox.Add(grid14,0)

        self.concolCircBtn.Bind(csel.EVT_COLOURSELECT, self.chooseConCircColor)
        self.Bind(wx.EVT_COMBOBOX, self.chooseConCircSty, self.constyleCirc )

##---------------------
# widgets and layout, eigenvectors
    # eigenvector 1
        self.cb_eigen_gc1 = wx.CheckBox(self.pgceigv, -1, 'Great Circle')
        self.cb_eigen_gc1.SetValue(self.cbeigengc1)

        txt_colGirdCirc1 = wx.StaticText(self.pgceigv, -1, 'Colour')
        txt_symbGirdCirc1 = wx.StaticText(self.pgceigv, -1, 'Symbol')
        txt_circGirdspin1 = wx.StaticText(self.pgceigv, -1, 'Size')
        txt_eigen1 = wx.StaticText(self.pgceigv, -1, 'Eigenvector 1')
        txt_eigen2 = wx.StaticText(self.pgceigv, -1, 'Eigenvector 2')
        txt_eigen3 = wx.StaticText(self.pgceigv, -1, 'Eigenvector 3')

        self.lcolGirdCircBtn1 = csel.ColourSelect(self.pgceigv, pos=(0, 0), size=(60, 20))
        self.lcolGirdCircBtn1.SetColour(self.CircGirdColor1)

        self.styleGirdCirc1 = wx.ComboBox(self.pgceigv, -1, value=styleList[styles.index(self.CircGirdSty1)], choices=styleList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        self.styleGirdCirc1.SetSelection(styles.index(self.CircGirdSty1))

        self.circGirdspin1 = FS.FloatSpin(self.pgceigv, -1, size=(60, -1), value=self.circGirdspin1, min_val=0.1, max_val=5, increment=0.1, digits=1)

        self.cb_eigen_p1 = wx.CheckBox(self.pgceigv, -1, 'Pole')
        self.cb_eigen_p1.SetValue(self.cbeigenp1)

        self.fcolGirdPolesBtn1 = csel.ColourSelect(self.pgceigv, pos=(0, 0), size=(60, 20))
        self.fcolGirdPolesBtn1.SetColour(self.PolGirdColor1)

        self.symbGirdPoles1 = wx.ComboBox(self.pgceigv, -1, value=symbolList[symbols.index(self.PoleGirdSymb1)], choices=symbolList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        self.symbGirdPoles1.SetSelection(symbols.index(self.PoleGirdSymb1))

        self.poleGirdspin1 = FS.FloatSpin(self.pgceigv, -1, size=(60, -1), value=self.poleGirdspin1, min_val=1, max_val=20, increment=0.5, digits=1)

        grid6 = wx.FlexGridSizer(9, 4, 5, 5)
        grid6.Add(txt_eigen1,0, wx.LEFT|wx.TOP, 5) #
        grid6.Add(txt_colGirdCirc1,0, wx.LEFT|wx.ALIGN_CENTER, 5)
        grid6.Add(txt_symbGirdCirc1,0, wx.LEFT|wx.ALIGN_CENTER, 5)
        grid6.Add(txt_circGirdspin1,0, wx.LEFT|wx.ALIGN_CENTER, 5) #

        grid6.Add(self.cb_eigen_gc1,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5) #, wx.ALIGN_CENTER, 5)
        grid6.Add(self.lcolGirdCircBtn1,0, wx.LEFT, 5) #|wx.ALIGN_CENTER, 5)
        grid6.Add(self.styleGirdCirc1,0, wx.LEFT, 5) #|wx.ALIGN_CENTER, 5)
        grid6.Add(self.circGirdspin1,0, wx.LEFT, 5) #|wx.ALIGN_CENTER, 5)

        grid6.Add(self.cb_eigen_p1,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5) #|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.fcolGirdPolesBtn1,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.symbGirdPoles1,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.poleGirdspin1,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT, 5)

        self.lcolGirdCircBtn1.Bind(csel.EVT_COLOURSELECT, self.chooseCircGirdColor1)
        self.Bind(wx.EVT_COMBOBOX, self.chooseCircGirdSty1, self.styleGirdCirc1 )
        self.fcolGirdPolesBtn1.Bind(csel.EVT_COLOURSELECT, self.choosePolGirdColor1)
        self.Bind(wx.EVT_COMBOBOX, self.choosePoleGirdSymb1, self.symbGirdPoles1 )

##---------------------
    # eigenvector 2
        self.cb_eigen_gc2 = wx.CheckBox(self.pgceigv, -1, 'Great circle')
        self.cb_eigen_gc2.SetValue(self.cbeigengc2)

        self.lcolGirdCircBtn2 = csel.ColourSelect(self.pgceigv, pos=(0, 0), size=(60, 20))
        self.lcolGirdCircBtn2.SetColour(self.CircGirdColor2)

        self.styleGirdCirc2 = wx.ComboBox(self.pgceigv, -1, value=styleList[styles.index(self.CircGirdSty2)], choices=styleList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        self.styleGirdCirc2.SetSelection(styles.index(self.CircGirdSty2))

        self.circGirdspin2 = FS.FloatSpin(self.pgceigv, -1, size=(60, -1), value=self.circGirdspin2, min_val=0.1, max_val=5, increment=0.1, digits=1)

        self.cb_eigen_p2 = wx.CheckBox(self.pgceigv, -1, 'Pole')
        self.cb_eigen_p2.SetValue(self.cbeigenp2)

        self.fcolGirdPolesBtn2 = csel.ColourSelect(self.pgceigv, pos=(0, 0), size=(60, 20))
        self.fcolGirdPolesBtn2.SetColour(self.PolGirdColor2)

        self.symbGirdPoles2 = wx.ComboBox(self.pgceigv, -1, value=symbolList[symbols.index(self.PoleGirdSymb2)], choices=symbolList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        self.symbGirdPoles2.SetSelection(symbols.index(self.PoleGirdSymb2))

        self.poleGirdspin2 = FS.FloatSpin(self.pgceigv, -1, size=(60, -1), value=self.poleGirdspin2, min_val=1, max_val=20, increment=0.5, digits=1)

        grid6.Add(txt_eigen2,0, wx.LEFT|wx.TOP, 5) #
        grid6.Add((2,2))
        grid6.Add((2,2))
        grid6.Add((2,2))
        grid6.Add(self.cb_eigen_gc2,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.lcolGirdCircBtn2,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.styleGirdCirc2,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.circGirdspin2,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT, 5)

        grid6.Add(self.cb_eigen_p2,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.fcolGirdPolesBtn2,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.symbGirdPoles2,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.poleGirdspin2,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT, 5)

        self.lcolGirdCircBtn2.Bind(csel.EVT_COLOURSELECT, self.chooseCircGirdColor2)
        self.Bind(wx.EVT_COMBOBOX, self.chooseCircGirdSty2, self.styleGirdCirc2 )
        self.fcolGirdPolesBtn2.Bind(csel.EVT_COLOURSELECT, self.choosePolGirdColor2)
        self.Bind(wx.EVT_COMBOBOX, self.choosePoleGirdSymb2, self.symbGirdPoles2 )

##---------------------
    # eigenvector 3
        self.cb_eigen_gc3 = wx.CheckBox(self.pgceigv, -1, 'Great circle')
        self.cb_eigen_gc3.SetValue(self.cbeigengc3)

        self.lcolGirdCircBtn3 = csel.ColourSelect(self.pgceigv, pos=(0, 0), size=(60, 20))
        self.lcolGirdCircBtn3.SetColour(self.CircGirdColor3)

        self.styleGirdCirc3 = wx.ComboBox(self.pgceigv, -1, value=styleList[styles.index(self.CircGirdSty3)], choices=styleList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        self.styleGirdCirc3.SetSelection(styles.index(self.CircGirdSty3))

        self.circGirdspin3 = FS.FloatSpin(self.pgceigv, -1, size=(60, -1), value=self.circGirdspin3, min_val=0.1, max_val=5, increment=0.1, digits=1)

        self.cb_eigen_p3 = wx.CheckBox(self.pgceigv, -1, 'Pole')
        self.cb_eigen_p3.SetValue(self.cbeigenp3)

        self.fcolGirdPolesBtn3 = csel.ColourSelect(self.pgceigv, pos=(0, 0), size=(60, 20))
        self.fcolGirdPolesBtn3.SetColour(self.PolGirdColor3)

        self.symbGirdPoles3 = wx.ComboBox(self.pgceigv, -1, value=symbolList[symbols.index(self.PoleGirdSymb3)], choices=symbolList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        self.symbGirdPoles3.SetSelection(symbols.index(self.PoleGirdSymb3))

        self.poleGirdspin3 = FS.FloatSpin(self.pgceigv, -1, size=(60, -1), value=self.poleGirdspin3, min_val=1, max_val=20, increment=0.5, digits=1)

        grid6.Add(txt_eigen3,0, wx.LEFT|wx.TOP, 5) #
        grid6.Add((2,2))
        grid6.Add((2,2))
        grid6.Add((2,2))
        grid6.Add(self.cb_eigen_gc3,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.lcolGirdCircBtn3,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.styleGirdCirc3,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.circGirdspin3,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT, 5)

        grid6.Add(self.cb_eigen_p3,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.fcolGirdPolesBtn3,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.symbGirdPoles3,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.poleGirdspin3,0, wx.LEFT, 5) #|wx.ALIGN_RIGHT, 5)

        eigen_box.Add(grid6,0)

        self.lcolGirdCircBtn3.Bind(csel.EVT_COLOURSELECT, self.chooseCircGirdColor3)
        self.Bind(wx.EVT_COMBOBOX, self.chooseCircGirdSty3, self.styleGirdCirc3 )
        self.fcolGirdPolesBtn3.Bind(csel.EVT_COLOURSELECT, self.choosePolGirdColor3)
        self.Bind(wx.EVT_COMBOBOX, self.choosePoleGirdSymb3, self.symbGirdPoles3 )

    #layout of widgets
        pgcbox = wx.FlexGridSizer(2, 1, 5, 5)
        pgcbox.Add(lines_box,0,wx.ALL,5)
        pgcbox.Add(confbox,0,wx.ALL,5)

        eigbox = wx.BoxSizer(wx.VERTICAL)
        eigbox.Add(eigen_box,0,wx.ALL,5)

        pgceigvbox = wx.FlexGridSizer(1, 2, 5, 5)
        pgceigvbox.Add(pgcbox,0,wx.ALL,5)
        pgceigvbox.Add(eigbox,0,wx.ALL,5)
        self.pgceigv.SetSizer(pgceigvbox)

##---------------------
# widgets and layout, contours
    # counting options
        txt_cntNodes = wx.StaticText(self.cont, -1, 'Grid Density')#'Counting Nodes')

        self.countNodes = wx.ComboBox(self.cont, -1, value=countNodesList[countNodes.index(self.countNodesNum)], choices=countNodesList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(90, -1))
        self.countNodes.SetSelection(countNodes.index(self.countNodesNum))
        self.percent = wx.CheckBox(self.cont, -1, 'Percentage')
        self.percent.SetValue(self.perCent)

        grid7 = wx.FlexGridSizer(1, 3, 5, 5)
        grid7.Add(txt_cntNodes,0, wx.TOP|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid7.Add(self.countNodes,0, wx.LEFT|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid7.Add(self.percent,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)


        self.rbcossum = wx.RadioButton(self.cont, -1, 'Cossine sums', style=wx.RB_GROUP)
        self.rbcossum.SetValue(self.rbCossum)

        self.rbfisher = wx.RadioButton(self.cont, -1, 'Gaussian distribution')
        self.rbfisher.SetValue(self.rbFisher)

        self.rbscarea = wx.RadioButton(self.cont, -1, 'Small circle count')
        self.rbscarea.SetValue(self.rbScarea)

        self.rbscangle = wx.RadioButton(self.cont, -1, 'Small circle count')
        self.rbscangle.SetValue(self.rbScangle)

        txt_expoent = wx.StaticText(self.cont, -1, '(expoent)')
        txt_paramk = wx.StaticText(self.cont, -1, '(K param.)')
        txt_area = wx.StaticText(self.cont, -1, '(% area)')
        txt_angle = wx.StaticText(self.cont, -1, '(angle)')

        self.expSpin = FS.FloatSpin(self.cont, -1, size=(60, -1), value=self.ExpSpin, min_val=1, max_val=999, increment=1, digits=0)
        self.kSpin = FS.FloatSpin(self.cont, -1, size=(60, -1), value=self.KSpin, min_val=1, max_val=999, increment=1, digits=0)
        self.areaSpin = FS.FloatSpin(self.cont, -1, size=(60, -1), value=self.AreaSpin, min_val=0.50, max_val=25, increment=0.50, digits=1)
        self.angleSpin = FS.FloatSpin(self.cont, -1, size=(60, -1), value=self.AngleSpin, min_val=0.50, max_val=45, increment=0.50, digits=1)

        grid7a = wx.FlexGridSizer(4, 3, 5, 5)
        grid7a.Add(self.rbfisher,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid7a.Add(txt_paramk,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid7a.Add(self.kSpin,0, wx.LEFT|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)

        grid7a.Add(self.rbcossum,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid7a.Add(txt_expoent,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid7a.Add(self.expSpin,0, wx.LEFT|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)

        grid7a.Add(self.rbscarea,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid7a.Add(txt_area,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid7a.Add(self.areaSpin,0, wx.LEFT|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)

        grid7a.Add(self.rbscangle,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid7a.Add(txt_angle,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid7a.Add(self.angleSpin,0, wx.LEFT|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)


        self.Bind(wx.EVT_COMBOBOX, self.chooseCountNodes, self.countNodes )

        count_box.Add(grid7,0)
        count_box.Add(grid7a,0, wx.TOP, 5)

##---------------------
    # interpolation options
        txt_method = wx.StaticText(self.cont, -1, 'Method')
        txt_ngrid = wx.StaticText(self.cont, -1, 'Steps')
#        txt_epsil = wx.StaticText(self.cont, -1, 'Epsilon')
#        txt_smoot = wx.StaticText(self.cont, -1, 'Smoothing')

        self.interps = wx.ComboBox(self.cont, -1, value=interpList[interpList.index(self.interpMet)], choices=interpList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(185, -1))
        self.interps.SetSelection(interpList.index(self.interpMet))

        self.gridSpin = FS.FloatSpin(self.cont, -1, size=(60, -1), value=self.gridSpin, min_val=10, max_val=1000, increment=10, digits=0)
#        self.epsilSpin = FS.FloatSpin(self.cont, -1, size=(60, -1), value=self.epsilSpin, min_val=0.001, max_val=1, increment=0.01, digits=3)
#        self.smootSpin = FS.FloatSpin(self.cont, -1, size=(60, -1), value=self.smootSpin, min_val=0, max_val=1, increment=0.001, digits=3)


        grid8 = wx.FlexGridSizer(1, 2, 5, 5)
        grid8.Add(txt_method,0, wx.LEFT|wx.TOP|wx.ALIGN_CENTER_VERTICAL, 5)
        grid8.Add(self.interps,0, wx.LEFT|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)

        grid8a = wx.FlexGridSizer(3, 2, 5, 5)
        grid8a.Add(txt_ngrid,0, wx.LEFT|wx.TOP|wx.ALIGN_CENTER_VERTICAL, 5)
        grid8a.Add(self.gridSpin,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
#        grid8a.Add(txt_epsil,0, wx.LEFT|wx.TOP|wx.ALIGN_CENTER_VERTICAL, 5)
#        grid8a.Add(self.epsilSpin,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
#        grid8a.Add(txt_smoot,0, wx.LEFT|wx.TOP|wx.ALIGN_CENTER_VERTICAL, 5)
#        grid8a.Add(self.smootSpin,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)

        self.Bind(wx.EVT_COMBOBOX, self.chooseInterps, self.interps )

        interp_box.Add(grid8,0)
        interp_box.Add(grid8a,0,wx.TOP, 5)

##---------------------
    # graphic options
        txt_csymb = wx.StaticText(self.cont, -1, 'Style')
        self.contSty = wx.ComboBox(self.cont, -1, value=styleList[styles.index(self.ContStyle)], choices=styleList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        self.contSty.SetSelection(styles.index(self.ContStyle))

        txt_cwdt = wx.StaticText(self.cont, -1, 'Width')
        self.contLws = FS.FloatSpin(self.cont, -1, size=(60, -1), value=self.contLwidths, min_val=0.1, max_val=5, increment=0.1, digits=1)

        self.contColBtn = csel.ColourSelect(self.cont, pos=(0, 0), size=(60, 20))
        self.contColBtn.SetColour(self.contColour)

        self.cont_fill = wx.CheckBox(self.cont, -1, 'Fill contours')
        self.cont_fill.SetValue(self.contFilled)

        self.add_edges = wx.CheckBox(self.cont, -1, 'Draw contours over filled')
        self.add_edges.SetValue(self.addEdges)

        self.antialiased = wx.CheckBox(self.cont, -1, 'Antialiased')
        self.antialiased.SetValue(self.antiAliased)

        self.contcolorMapsChoice = wx.ComboBox(self.cont, -1, value=mapsList[mapsList.index(self.contcolorMap)], choices=mapsList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(105, -1))
        self.contcolorMapsChoice.SetSelection(mapsList.index(self.contcolorMap))
        self.contcolorMapsChoice.Bind(wx.EVT_COMBOBOX, self.OnSelectcontColorMap)

        self.colorMapsChoice = wx.ComboBox(self.cont, -1, value=mapsList[mapsList.index(self.colorMap)], choices=mapsList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(105, -1))
        self.colorMapsChoice.SetSelection(mapsList.index(self.colorMap))
        self.colorMapsChoice.Bind(wx.EVT_COMBOBOX, self.OnSelectColorMap)


        self.rbsc = wx.RadioButton(self.cont, -1, 'Line Colour', style=wx.RB_GROUP)
        self.rbcm = wx.RadioButton(self.cont, -1, 'Line Gradient')
        self.rbsc.SetValue(self.rbSc)
        self.rbcm.SetValue(self.rbCm)

        self.contColBtn.Bind(csel.EVT_COLOURSELECT, self.chooseContCol)
        self.Bind(wx.EVT_COMBOBOX, self.chooseContSty, self.contSty )

        grid9 = wx.FlexGridSizer(4, 4, 5, 5)
        grid9.Add(self.rbsc,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid9.Add(self.contColBtn,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid9.Add(txt_csymb,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid9.Add(self.contSty,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)

        grid9.Add(self.rbcm,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid9.Add(self.contcolorMapsChoice,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid9.Add(txt_cwdt,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid9.Add(self.contLws,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)

        grid9.Add(self.cont_fill,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid9.Add(self.colorMapsChoice,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid9.Add((2,2))
        grid9.Add((2,2))

        grid9a = wx.FlexGridSizer(2, 1, 5, 5)
        grid9a.Add(self.antialiased,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid9a.Add(self.add_edges,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)


        contgraph_box.Add(grid9,0)
        contgraph_box.Add(grid9a,0, wx.TOP, 5)

##---------------------
# interval options

        self.rbminmax = wx.RadioButton(self.cont, -1, 'From minimum to maximum', style=wx.RB_GROUP)
        self.rbzeromax = wx.RadioButton(self.cont, -1, 'From zero to maximum')
        self.rbcustom = wx.RadioButton(self.cont, -1, 'Custom list')

        self.rbminmax.SetValue(self.rbMinMax)
        self.rbzeromax.SetValue(self.rbZeroMax)
        self.rbcustom.SetValue(self.rbCustom)

        txt_numcont = wx.StaticText(self.cont, -1, 'Number of contours')
        self.numcontours = FS.FloatSpin(self.cont, -1, size=(60, -1), value=self.numContours, min_val=1, max_val=50, increment=1, digits=0)
        self.control1 = wx.TextCtrl(self.cont, -1, size=(203,-1))
        self.control1.SetValue(self.customcont)

        grid10 = wx.FlexGridSizer(2, 1, 5, 5)
        grid10.Add(self.rbminmax,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid10.Add(self.rbzeromax,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid10a = wx.FlexGridSizer(2, 2, 5, 5)
        grid10a.Add(txt_numcont,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid10a.Add(self.numcontours,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid10a.Add(self.rbcustom,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid10a.Add(self.control1,0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)

        interval_box.Add(grid10,0, wx.TOP, 5)
        interval_box.Add(grid10a,0, wx.TOP, 5)

##---------------------
# set the contour panel layout
        contbox = wx.FlexGridSizer(2, 2, 5, 5)
        contbox.Add(contgraph_box,0,wx.ALL,5)
        contbox.Add(count_box,0,wx.ALL,5)
        contbox.Add(interval_box,0,wx.ALL,5)
        contbox.Add(interp_box,0,wx.ALL,5)
        self.cont.SetSizer(contbox)

##---------------------
        dlgbox = wx.BoxSizer(wx.VERTICAL) 
        btnbox = wx.BoxSizer(wx.HORIZONTAL)
        nbbox = wx.BoxSizer(wx.VERTICAL) 

        self.nb.AddPage(self.pgceigv, "Poles / Great Circles / Eigenvectors")
        self.nb.AddPage(self.cont, "Contours")

        btnbox.Add(drawButton, 0)
        btnbox.Add(closeButton, 0, wx.LEFT, 10)

        nbbox.Add(self.nb, 0, wx.ALL|wx.EXPAND,5) # add notebook to sizer
        nbbox.Add(btnbox, 0, wx.ALL|wx.ALIGN_CENTER, 5) # add OK and Cancel btns to sizer

        self.scroll.SetSizer(nbbox)
        nbbox.Fit(self.scroll)
        nbbox.SetSizeHints(self.scroll)

        dlgbox.Add(self.scroll, 0, wx.EXPAND,0)
        self.SetSizer(dlgbox)
        dlgbox.Fit(self)
        dlgbox.SetSizeHints(self)

        self.SetFocus()

##-----------------------------------------------------------------------------
    def onCloseLProps(self, event):
        self.Destroy()


##-----------------------------------------------------------------------------
#choose poles to lines color dialog.
    def chooseLinColor(self,event):
        """Colour dialog for Poles Fill colour"""
        self.LinColor = self.fcolLinesBtn.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)

#choose poles to lines symbol
    def chooseLineSymb(self,event):
        """Choose poles to planes simbol"""
        symb2 = self.symbLines.GetValue()
        self.LineSymb = symbols[symbolList.index(symb2)]

##-----------------------------------------------------------------------------


#choose confidence cone line color dialog
    def chooseConCircColor(self,event):
        """Colour dialog for confidence cone line colour"""
        self.conCircColor = self.concolCircBtn.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)

#choose confidence cone line style
    def chooseConCircSty(self,event):
        """Choose line style"""
        sty1 = self.constyleCirc.GetValue()
        self.conCircSty = styles[styleList.index(sty1)]

##-----------------------------------------------------------------------------

#choose girdle line color dialog - vector 1
    def chooseCircGirdColor1(self,event):
        """Colour dialog for Girdle colour"""
        self.CircGirdColor1 = self.lcolGirdCircBtn1.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)

#choose girdle line color dialog - vector 2
    def chooseCircGirdColor2(self,event):
        """Colour dialog for Girdle colour"""
        self.CircGirdColor2 = self.lcolGirdCircBtn2.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)

#choose girdle line color dialog - vector 3
    def chooseCircGirdColor3(self,event):
        """Colour dialog for Girdle colour"""
        self.CircGirdColor3 = self.lcolGirdCircBtn3.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)

#choose girdle great circle line style - vector 1
    def chooseCircGirdSty1(self,event):
        """Choose poles to planes simbol"""
        sty1 = self.styleGirdCirc1.GetValue()
        self.CircGirdSty1 = styles[styleList.index(sty1)]

#choose girdle great circle line style - vector 2
    def chooseCircGirdSty2(self,event):
        """Choose poles to planes simbol"""
        sty1 = self.styleGirdCirc2.GetValue()
        self.CircGirdSty2 = styles[styleList.index(sty1)]

#choose girdle great circle line style - vector 3
    def chooseCircGirdSty3(self,event):
        """Choose poles to planes simbol"""
        sty1 = self.styleGirdCirc3.GetValue()
        self.CircGirdSty3 = styles[styleList.index(sty1)]

#choose pole to girdle color dialog. - vector 1
    def choosePolGirdColor1(self,event):
        """Colour dialog for Poles Fill colour"""
        self.PolGirdColor1 = self.fcolGirdPolesBtn1.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)

#choose pole to girdle color dialog. - vector 2
    def choosePolGirdColor2(self,event):
        """Colour dialog for Poles Fill colour"""
        self.PolGirdColor2 = self.fcolGirdPolesBtn2.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)

#choose pole to girdle color dialog. - vector 3
    def choosePolGirdColor3(self,event):
        """Colour dialog for Poles Fill colour"""
        self.PolGirdColor3 = self.fcolGirdPolesBtn3.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)

#choose pole to girdle symbol - vector 1
    def choosePoleGirdSymb1(self,event):
        """Choose poles to planes simbol"""
        symb1 = self.symbGirdPoles1.GetValue()
        self.PoleGirdSymb1 = symbols[symbolList.index(symb1)]

#choose pole to girdle symbol - vector 2
    def choosePoleGirdSymb2(self,event):
        """Choose poles to planes simbol"""
        symb1 = self.symbGirdPoles2.GetValue()
        self.PoleGirdSymb2 = symbols[symbolList.index(symb1)]

#choose pole to girdle symbol - vector 3
    def choosePoleGirdSymb3(self,event):
        """Choose poles to planes simbol"""
        symb1 = self.symbGirdPoles3.GetValue()
        self.PoleGirdSymb3 = symbols[symbolList.index(symb1)]

#-----------------------------------------------------------------------------
#choose number of nodes for counting
    def chooseCountNodes(self,event):
        """Choose number of counting nodes"""
        cnt = self.countNodes.GetValue()
        self.countNodesNum = countNodes[countNodesList.index(cnt)]

#choose interpolation method
    def chooseInterps(self,event):
        """Choose interpolation method"""
        interp = self.interps.GetValue()
        self.interpMet = interpList[interpList.index(interp)]

#choose contour lines color dialog. Get color datas as hex, for matplotlib
    def chooseContCol(self,event):
        """Contour lines colour dialog"""

        self.contColour = self.contColBtn.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)

#choose contour line style 
    def chooseContSty(self,event):
        """Choose style of contour lines"""
        sty1 = self.contSty.GetValue()
        self.ContStyle = styles[styleList.index(sty1)]

#choose colormap for fill
    def OnSelectColorMap(self, evt=None):
        ''' Handles the selection of a color map from a choice box. '''
        cmap = self.colorMapsChoice.GetValue()
        self.colorMap = mapsList[mapsList.index(cmap)] #self.colorMapsChoice.GetStringSelection()

#choose colormap for contour lines 
    def OnSelectcontColorMap(self, evt=None):
        ''' Handles the selection of a color map from a choice box. '''
        cmap = self.contcolorMapsChoice.GetValue()
        self.contcolorMap = mapsList[mapsList.index(cmap)] #self.colorMapsChoice.GetStringSelection()


#-----------------------------------------------------------------------------

# return graphic properties of linear data
    def onLinProps(self):
        val = self.ShowModal()
        if val == wx.ID_OK:
            return self.LinColor, self.LineSymb, self.linespin.GetValue(), \
            self.cb_eigen_gc1.GetValue(), self.CircGirdColor1, self.CircGirdSty1, self.circGirdspin1.GetValue(), \
            self.cb_eigen_p1.GetValue(), self.PolGirdColor1, self.PoleGirdSymb1, self.poleGirdspin1.GetValue(), \
            self.cb_eigen_gc2.GetValue(), self.CircGirdColor2, self.CircGirdSty2, self.circGirdspin2.GetValue(), \
            self.cb_eigen_p2.GetValue(), self.PolGirdColor2, self.PoleGirdSymb2, self.poleGirdspin2.GetValue(), \
            self.cb_eigen_gc3.GetValue(), self.CircGirdColor3, self.CircGirdSty3, self.circGirdspin3.GetValue(), \
            self.cb_eigen_p3.GetValue(), self.PolGirdColor3, self.PoleGirdSymb3, self.poleGirdspin3.GetValue(), \
            self.countNodesNum, self.percent.GetValue(), self.interpMet, self.gridSpin.GetValue(), \
            self.ContStyle, self.contColour, \
            self.cont_fill.GetValue(), self.contLws.GetValue(), self.colorMap, self.contcolorMap, self.add_edges.GetValue(), \
            self.rbsc.GetValue(), self.rbcm.GetValue(), self.antialiased.GetValue(), self.rbminmax.GetValue(), \
            self.rbzeromax.GetValue(), self.numcontours.GetValue(), self.rbcustom.GetValue(), self.control1.GetValue(), \
            self.rbcossum.GetValue(), self.expSpin.GetValue(), self.rbfisher.GetValue(), self.kSpin.GetValue(), \
            self.rbscarea.GetValue(), self.areaSpin.GetValue(), self.rbscangle.GetValue(), self.angleSpin.GetValue(), \
            self.conCircSty, self.conCircColor, self.conspin.GetValue(), self.cb_conf.GetValue()
        else:
            return None

        dlg.Destroy()

#self.epsilSpin.GetValue(), self.smootSpin.GetValue(), 


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------


class SmallOptions(wx.Dialog):
    def __init__(self, parent, id, title, opt_dict):#, size=(725,425))
        wx.Dialog.__init__(self, parent, id, title, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME)

# defaults for colors and symbols
#        idx = opt_dict[0]
#        name = opt_dict[1]

        self.ScColor = opt_dict["ScColor"]
        self.ScSty = opt_dict["ScSty"]
        self.ScSpin = opt_dict["ScSpin"]
        self.ScFull = opt_dict["ScFull"]

        drawButton = wx.Button(self, wx.ID_OK, 'OK', size=(80, 30))
        closeButton = wx.Button(self, wx.ID_CANCEL, 'Cancel', size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.onCloseScProps, id=wx.ID_CANCEL)

        self.SetAffirmativeId(wx.ID_OK)
        self.SetEscapeId(wx.ID_CANCEL)

##---------------------
# widgets and layout, small circles
    # the wx.StaticBoxSizers must come before the things inside them or else it won't work properly on MacOSX
        circlesbox = wx.StaticBoxSizer(wx.StaticBox(self, -1, ' Small Circles '), orient=wx.VERTICAL)
        
        
        txt_colCirc = wx.StaticText(self, -1, 'Colour')
        self.lcolCircBtn = csel.ColourSelect(self, pos=(0, 0), size=(60, 20))
        self.lcolCircBtn.SetColour(self.ScColor)

        txt_symbCirc = wx.StaticText(self, -1, 'Line Type')
        self.styleCirc = wx.ComboBox(self, -1, value=styleList[styles.index(self.ScSty)], choices=styleList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        txt_circspin = wx.StaticText(self, -1, 'Width')
        self.circspin = FS.FloatSpin(self, -1, size=(60, -1), value=self.ScSpin, min_val=0.1, max_val=5, increment=0.1, digits=1)
        self.styleCirc.SetSelection(styles.index(self.ScSty))
#        self.cb_full = wx.CheckBox(self, -1, 'Plot full circle')
#        self.cb_full.SetValue(self.ScFull)


        grid4 = wx.FlexGridSizer(3, 3, 5, 5)
        grid4.Add(txt_colCirc,0, wx.LEFT|wx.TOP, 5)
        grid4.Add(txt_symbCirc,0, wx.LEFT|wx.TOP, 5)
        grid4.Add(txt_circspin,0, wx.LEFT|wx.TOP, 5)
        grid4.Add(self.lcolCircBtn,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid4.Add(self.styleCirc,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid4.Add(self.circspin,0, wx.LEFT|wx.ALIGN_RIGHT, 5)

#        fullbox = wx.BoxSizer(wx.HORIZONTAL)
#        fullbox.Add(self.cb_full,0, wx.LEFT, 5)

        self.lcolCircBtn.Bind(csel.EVT_COLOURSELECT, self.chooseCircColor)
        self.Bind(wx.EVT_COMBOBOX, self.chooseCircSty, self.styleCirc )

    #layout of widgets
        circlesbox.Add(grid4,0)
        
        btnbox = wx.BoxSizer(wx.HORIZONTAL)
        btnbox.Add(drawButton, 0)
        btnbox.Add(closeButton, 0, wx.LEFT, 10)

        dlgbox = wx.BoxSizer(wx.VERTICAL) 
        dlgbox.Add(circlesbox, 0, wx.ALL, 5)
#        dlgbox.Add(fullbox, 0, wx.ALL, 5)
        dlgbox.Add(btnbox, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.SetSizer(dlgbox)
        dlgbox.Fit(self)
#        dlgbox.SetSizeHints(self)

        self.SetFocus()

##-----------------------------------------------------------------------------
    def onCloseScProps(self, event):
        self.Destroy()

##-----------------------------------------------------------------------------

#choose small circle line color dialog
    def chooseCircColor(self,event):
        """Colour dialog for Line colour"""
        self.ScColor = self.lcolCircBtn.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)

#choose small circle line style
    def chooseCircSty(self,event):
        """Choose poles to planes simbol"""
        sty1 = self.styleCirc.GetValue()
        self.ScSty = styles[styleList.index(sty1)]
#        print self.CircSty

#-----------------------------------------------------------------------------
# return graphic properties of small circle data
    def onSmallProps(self):
        val = self.ShowModal()
        if val == wx.ID_OK:
            return self.ScColor, self.ScSty, self.circspin.GetValue() #, self.cb_full.GetValue()
        else:
            return None

        dlg.Destroy()



#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------


class FaultOptions(wx.Dialog):
    def __init__(self, parent, id, title, opt_dict):#, size=(725,425))
        wx.Dialog.__init__(self, parent, id, title, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME)

        self.FaultCircColor = opt_dict["FaultCircColor"]
        self.FaultCircSty = opt_dict["FaultCircSty"]
        self.FaultCircSpin = opt_dict["FaultCircSpin"]

        self.SlickPlotPoles  = opt_dict["SlickPlotPoles"]
        self.SlickPoleColor = opt_dict["SlickPoleColor"]
        self.SlickPoleSymb = opt_dict["SlickPoleSymb"]
        self.SlickPoleSpin = opt_dict["SlickPoleSpin"]
        
        self.SlickArrowSpin = opt_dict["SlickArrowSpin"]
        self.SlickArrowColor = opt_dict["SlickArrowColor"]
        self.SlickArrowWidthSpin = opt_dict["SlickArrowWidthSpin"]    

        self.DisplacePlotPoles  = opt_dict["DisplacePlotPoles"]
        self.DisplacePoleColor = opt_dict["DisplacePoleColor"]
        self.DisplacePoleSymb = opt_dict["DisplacePoleSymb"]
        self.DisplacePoleSpin = opt_dict["DisplacePoleSpin"]

        self.DisplaceArrowSpin = opt_dict["DisplaceArrowSpin"]
        self.DisplaceArrowColor = opt_dict["DisplaceArrowColor"]
        self.DisplaceArrowWidthSpin = opt_dict["DisplaceArrowWidthSpin"]  

        self.footwall = opt_dict["footwall"] 

        
        # create scroled window
        self.scroll = wx.ScrolledWindow(self, -1, style=wx.TAB_TRAVERSAL)
        self.scroll.SetScrollRate(10, 10)

# create a notebook for prefs
        self.nb = wx.Notebook(self.scroll)#, size=(615,370))#, style=wx.TAB_TRAVERSAL)
        self.fault = wx.Panel(self.nb, -1)# page 1, great vircle, poles and arrows for slickensides
#        self.cont = wx.Panel(self.nb, -1) # page 2, countours

        drawButton = wx.Button(self.scroll, wx.ID_OK, 'OK', size=(80, 30))
        closeButton = wx.Button(self.scroll, wx.ID_CANCEL, 'Cancel', size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.onCloseFProps, id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_OK)
        self.SetEscapeId(wx.ID_CANCEL)



##---------------------
# widgets and layout, first panel (poles and great circles)

    # the wx.StaticBoxSizers must come before the things inside them or else it won't work properly on MacOSX
        circles_box = wx.StaticBoxSizer(wx.StaticBox(self.fault, -1, 'Great Circles'), orient=wx.VERTICAL)
        arrows_box = wx.StaticBoxSizer(wx.StaticBox(self.fault, -1, 'Arrows for slickensides'), orient=wx.VERTICAL)
        poles_box = wx.StaticBoxSizer(wx.StaticBox(self.fault, -1, ' Poles to Slickensides '), orient=wx.VERTICAL)
        arrows_box2 = wx.StaticBoxSizer(wx.StaticBox(self.fault, -1, 'Arrows for slip-linear'), orient=wx.VERTICAL)
        hopp_box = wx.StaticBoxSizer(wx.StaticBox(self.fault, -1, ' Poles to Fault Planes '), orient=wx.VERTICAL)


    #great circles
        txt_colCirc = wx.StaticText(self.fault, -1, 'Colour')
        self.fcolCircBtn = csel.ColourSelect(self.fault, pos=(0, 0), size=(60, 20))
        self.fcolCircBtn.SetColour(self.FaultCircColor)
        
        txt_symbCirc = wx.StaticText(self.fault, -1, 'Line Type')
        self.fstyleCirc = wx.ComboBox(self.fault, -1, value=styleList[styles.index(self.FaultCircSty)], choices=styleList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        self.fstyleCirc.SetSelection(styles.index(self.FaultCircSty))
        
        txt_circspin = wx.StaticText(self.fault, -1, 'Width')
        self.fcircspin = FS.FloatSpin(self.fault, -1, size=(60, -1), value=self.FaultCircSpin, min_val=0.1, max_val=5, increment=0.1, digits=1)

        grid4 = wx.FlexGridSizer(2, 3, 5, 5)
        grid4.Add(txt_colCirc,0, wx.LEFT|wx.TOP, 5)
        grid4.Add(txt_symbCirc,0, wx.LEFT|wx.TOP, 5)
        grid4.Add(txt_circspin,0, wx.LEFT|wx.TOP, 5)
        grid4.Add(self.fcolCircBtn,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid4.Add(self.fstyleCirc,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid4.Add(self.fcircspin,0, wx.LEFT|wx.ALIGN_RIGHT, 5)
        circles_box.Add(grid4,0)

        self.fcolCircBtn.Bind(csel.EVT_COLOURSELECT, self.chooseFCircColor)
        self.Bind(wx.EVT_COMBOBOX, self.chooseFCircSty, self.fstyleCirc )

##---------------------
    # arrows to slickensides
        txt_colArr = wx.StaticText(self.fault, -1, 'Colour')
        self.fcolArrBtn = csel.ColourSelect(self.fault, pos=(0, 0), size=(60, 20))
        self.fcolArrBtn.SetColour(self.SlickArrowColor)
        
        txt_ArrSize = wx.StaticText(self.fault, -1, 'Size')
        self.fArrWspin = FS.FloatSpin(self.fault, -1, size=(60, -1), value=self.SlickArrowWidthSpin, min_val=0.1, max_val=5, increment=0.1, digits=1)
        
        txt_ArrSpin = wx.StaticText(self.fault, -1, 'Width')
        self.fArrSpin = FS.FloatSpin(self.fault, -1, size=(60, -1), value=self.SlickArrowSpin, min_val=0.1, max_val=5, increment=0.1, digits=1)

        grid5 = wx.FlexGridSizer(2, 3, 5, 5)
        grid5.Add(txt_colArr,0, wx.LEFT|wx.TOP, 5)
        grid5.Add(txt_ArrSize,0, wx.LEFT|wx.TOP, 5)
        grid5.Add(txt_ArrSpin,0, wx.LEFT|wx.TOP, 5)
        grid5.Add(self.fcolArrBtn,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid5.Add(self.fArrWspin,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid5.Add(self.fArrSpin,0, wx.LEFT|wx.ALIGN_RIGHT, 5)
        arrows_box.Add(grid5,0)

        self.fcolArrBtn.Bind(csel.EVT_COLOURSELECT, self.chooseFArrowColor)
        
##---------------------
    # poles to fault planes (for slip-linear)
        self.cbDisplacePlotPoles = wx.CheckBox(self.fault, -1, 'Plot poles to fault planes')
        self.cbDisplacePlotPoles.SetValue(self.DisplacePlotPoles)
        
        txt_colDisplacePoles = wx.StaticText(self.fault, -1, 'Colour')
        self.DisplacecolPolesBtn = csel.ColourSelect(self.fault, pos=(0, 0), size=(60, 20))
        self.DisplacecolPolesBtn.SetColour(self.DisplacePoleColor)
        
        txt_symbDisplacePoles = wx.StaticText(self.fault, -1, 'Symbol')
        self.DisplacesymbPoles = wx.ComboBox(self.fault, -1, value=symbolList[symbols.index(self.DisplacePoleSymb)], choices=symbolList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        self.DisplacesymbPoles.SetSelection(symbols.index(self.DisplacePoleSymb))
        
        txt_Displacespin = wx.StaticText(self.fault, -1, 'Size')
        self.Displacepolespin = FS.FloatSpin(self.fault, -1, size=(60, -1), value=self.DisplacePoleSpin, min_val=1, max_val=20, increment=0.50, digits=2)

        grid6 = wx.FlexGridSizer(2, 3, 5, 5)
        grid6.Add(txt_colDisplacePoles,0, wx.LEFT|wx.TOP, 5)
        grid6.Add(txt_symbDisplacePoles,0, wx.LEFT|wx.TOP, 5)
        grid6.Add(txt_Displacespin,0, wx.LEFT|wx.TOP, 5)
        grid6.Add(self.DisplacecolPolesBtn,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.DisplacesymbPoles,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid6.Add(self.Displacepolespin,0, wx.LEFT|wx.ALIGN_RIGHT, 5)
        hopp_box.Add(self.cbDisplacePlotPoles,0)
        hopp_box.Add(grid6,0)

        self.DisplacecolPolesBtn.Bind(csel.EVT_COLOURSELECT, self.chooseDisplacePolColor)
        self.Bind(wx.EVT_COMBOBOX, self.chooseDisplacePoleSymb, self.DisplacesymbPoles )

##---------------------       
    # poles to slickensides
        self.cbSlickPlotPoles = wx.CheckBox(self.fault, -1, 'Plot poles to slickensides')
        self.cbSlickPlotPoles.SetValue(self.SlickPlotPoles)
        
        txt_colPoles = wx.StaticText(self.fault, -1, 'Colour')
        self.slkcolPolesBtn = csel.ColourSelect(self.fault, pos=(0, 0), size=(60, 20))
        self.slkcolPolesBtn.SetColour(self.SlickPoleColor)
        
        txt_symbPoles = wx.StaticText(self.fault, -1, 'Symbol')
        self.slksymbPoles = wx.ComboBox(self.fault, -1, value=symbolList[symbols.index(self.SlickPoleSymb)], choices=symbolList, style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(60, -1))
        self.slksymbPoles.SetSelection(symbols.index(self.SlickPoleSymb))
        
        txt_polespin = wx.StaticText(self.fault, -1, 'Size')
        self.slkpolespin = FS.FloatSpin(self.fault, -1, size=(60, -1), value=self.SlickPoleSpin, min_val=1, max_val=20, increment=0.50, digits=2)

        grid2 = wx.FlexGridSizer(2, 3, 5, 5)
        grid2.Add(txt_colPoles,0, wx.LEFT|wx.TOP, 5)
        grid2.Add(txt_symbPoles,0, wx.LEFT|wx.TOP, 5)
        grid2.Add(txt_polespin,0, wx.LEFT|wx.TOP, 5)
        grid2.Add(self.slkcolPolesBtn,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid2.Add(self.slksymbPoles,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid2.Add(self.slkpolespin,0, wx.LEFT|wx.ALIGN_RIGHT, 5)
        poles_box.Add(self.cbSlickPlotPoles,0)
        poles_box.Add(grid2,0)

        self.slkcolPolesBtn.Bind(csel.EVT_COLOURSELECT, self.chooseSlkPolColor)
        self.Bind(wx.EVT_COMBOBOX, self.chooseSlkPoleSymb, self.slksymbPoles )


##---------------------       
    # arrows to slip-linear
        self.cbDisplaceFootwall = wx.CheckBox(self.fault, -1, 'Plot slip for footwall')
        self.cbDisplaceFootwall.SetValue(self.footwall)
        
        txt_colArrSlp = wx.StaticText(self.fault, -1, 'Colour')
        self.fcolArrBtnSlp = csel.ColourSelect(self.fault, pos=(0, 0), size=(60, 20))
        self.fcolArrBtnSlp.SetColour(self.DisplaceArrowColor)
        
        txt_ArrSizeSlp = wx.StaticText(self.fault, -1, 'Size')
        self.fArrWspinSlp = FS.FloatSpin(self.fault, -1, size=(60, -1), value=self.DisplaceArrowWidthSpin, min_val=0.1, max_val=5, increment=0.1, digits=1)
        
        txt_ArrSpinSlp = wx.StaticText(self.fault, -1, 'Width')
        self.fArrSpinSlp = FS.FloatSpin(self.fault, -1, size=(60, -1), value=self.DisplaceArrowSpin, min_val=0.1, max_val=5, increment=0.1, digits=1)

        gridx = wx.FlexGridSizer(2, 3, 5, 5)
        gridx.Add(txt_colArrSlp,0, wx.LEFT|wx.TOP, 5)
        gridx.Add(txt_ArrSizeSlp,0, wx.LEFT|wx.TOP, 5)
        gridx.Add(txt_ArrSpinSlp,0, wx.LEFT|wx.TOP, 5)
        gridx.Add(self.fcolArrBtnSlp,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        gridx.Add(self.fArrWspinSlp,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        gridx.Add(self.fArrSpinSlp,0, wx.LEFT|wx.ALIGN_RIGHT, 5)
        arrows_box2.Add(self.cbDisplaceFootwall,0)
        arrows_box2.Add(gridx,0)

        self.fcolArrBtnSlp.Bind(csel.EVT_COLOURSELECT, self.chooseFArrowColorSlp)


##---------------------    
    #layout of widgets
        pgbox = wx.FlexGridSizer(3, 2, 5, 5) #BoxSizer(wx.VERTICAL)
        pgbox.Add(circles_box,0,wx.ALL,5)
        pgbox.Add(arrows_box,0,wx.ALL,5)
        pgbox.Add(hopp_box,0,wx.ALL,5)
        pgbox.Add(poles_box,0,wx.ALL,5)
        pgbox.Add(arrows_box2,0,wx.ALL,5)        
        self.fault.SetSizer(pgbox)
        

##---------------------
        dlgbox = wx.BoxSizer(wx.VERTICAL) 
        btnbox = wx.BoxSizer(wx.HORIZONTAL)
        nbbox = wx.BoxSizer(wx.VERTICAL) 

        self.nb.AddPage(self.fault, "Great Circles / Slickensides")
#        self.nb.AddPage(self.cont, "Contours")

        btnbox.Add(drawButton, 0)
        btnbox.Add(closeButton, 0, wx.LEFT, 10)

        nbbox.Add(self.nb, 0, wx.ALL|wx.EXPAND,5) # add notebook to sizer
        nbbox.Add(btnbox, 0, wx.ALL|wx.ALIGN_CENTER, 5) # add OK and Cancel btns to sizer

        self.scroll.SetSizer(nbbox)
        nbbox.Fit(self.scroll)
        nbbox.SetSizeHints(self.scroll)

        dlgbox.Add(self.scroll, 0, wx.EXPAND,0)
        self.SetSizer(dlgbox)
        dlgbox.Fit(self)
        dlgbox.SetSizeHints(self)

        self.SetFocus()
        
        
        
        
        
        
        
        
##-----------------------------------------------------------------------------
#choose fault plane great circle line color dialog
    def chooseFCircColor(self,event):
        """Colour dialog for fault plane great circle line colour"""
        dlg = wx.ColourDialog(self)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            self.FaultCircColor = dlg.GetColourData().GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)
            self.fcolCircBtn.SetBackgroundColour(self.FaultCircColor)
        dlg.Destroy()

#choose fault plane great circle line style
    def chooseFCircSty(self,event):
        """Choose fault plane great circle line style"""
        sty1 = self.fstyleCirc.GetValue()
        self.FaultCircSty = styles[styleList.index(sty1)]
        

##-----------------------------------------------------------------------------
#choose slickenside line color dialog
    def chooseFArrowColor(self,event):
        """Colour dialog for slickenside colour"""
        dlg = wx.ColourDialog(self)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            self.SlickArrowColor = dlg.GetColourData().GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)
            self.fcolArrBtn.SetBackgroundColour(self.SlickArrowColor)
        dlg.Destroy()

##-----------------------------------------------------------------------------
#choose slip-linear line color dialog
    def chooseFArrowColorSlp(self,event):
        """Colour dialog for slickenside colour"""
        self.DisplaceArrowColor = self.fcolArrBtnSlp.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)


##-----------------------------------------------------------------------------
#choose poles to fault planes color dialog.
    def chooseDisplacePolColor(self,event):
        """Colour dialog for Poles to slickensides colour"""
        self.DisplacePoleColor = self.DisplacecolPolesBtn.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)


#choose poles to lines symbol
    def chooseDisplacePoleSymb(self,event):
        """Choose poles to to slickensides simbol"""
        symb2 = self.DisplacesymbPoles.GetValue()
        self.DisplacePoleSymb = symbols[symbolList.index(symb2)]


##-----------------------------------------------------------------------------
#choose poles to slickensides color dialog.
    def chooseSlkPolColor(self,event):
        """Colour dialog for Poles to slickensides colour"""
        self.SlickPoleColor = self.slkcolPolesBtn.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)


#choose poles to lines symbol
    def chooseSlkPoleSymb(self,event):
        """Choose poles to to slickensides simbol"""
        symb2 = self.slksymbPoles.GetValue()
        self.SlickPoleSymb = symbols[symbolList.index(symb2)]



##-----------------------------------------------------------------------------
    def onCloseFProps(self, event):
        self.Destroy()
        
        
##-----------------------------------------------------------------------------
    def onFaultProps(self):
        val = self.ShowModal()
        if val == wx.ID_OK:

            return self.FaultCircColor, self.FaultCircSty, self.FaultCircSpin, \
                self.cbSlickPlotPoles.GetValue(), self.SlickPoleColor, self.SlickPoleSymb, self.slkpolespin.GetValue(), \
                self.fArrSpin.GetValue(), self.SlickArrowColor, self.fArrWspin.GetValue(), \
                self.cbDisplacePlotPoles.GetValue(), self.DisplacePoleColor, self.DisplacePoleSymb, self.Displacepolespin.GetValue(), \
                self.fArrSpinSlp.GetValue(), self.DisplaceArrowColor, self.fArrWspinSlp.GetValue(), self.cbDisplaceFootwall.GetValue()
        else:
            return None

        dlg.Destroy()












