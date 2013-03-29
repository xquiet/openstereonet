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

import os, sys
import wx
#import wx.lib.agw.floatspin as FS
import floatspin as FS

import MiscDefs as md

import numpy as np


########################## Merge data
class MergeData(wx.Dialog):
    """Creates a dialog to select files to merge"""
    def __init__(self, parent, id, title, filesList):
        wx.Dialog.__init__(self, parent, id, title, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME, size=(200, 250))

        self.filesList = filesList
        self.pathChoosed = 0

        Panel = wx.Panel(self, -1)

        txt = wx.StaticText(Panel, -1, 'Select datasets:')
        self.listbox = wx.ListBox(Panel, -1, style=wx.LB_EXTENDED, size=(180, 150))
        self.Bind(wx.EVT_LISTBOX, self.OnSelect, self.listbox, filesList)

        mergeButton = wx.Button(Panel, wx.ID_OK, 'OK', size=(80, 30))
        closeButton = wx.Button(Panel, wx.ID_CANCEL, 'Cancel', size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.onCloseTool, id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_OK)
        self.SetEscapeId(wx.ID_CANCEL)

        txt2 = wx.StaticText(Panel, -1, 'Options:')
        self.cb_save = wx.CheckBox(Panel, -1, 'Save to disk')
        self.cb_save.SetValue(True)
        self.cb_append = wx.CheckBox(Panel, -1, 'Load merged file')
        self.cb_append.SetValue(True)

        self.rb1 = wx.RadioButton(Panel, -1, 'as planes', style=wx.RB_GROUP)
        self.rb2 = wx.RadioButton(Panel, -1, 'as lines')
        self.rb4 = wx.RadioButton(Panel, -1, 'as faults')
        self.rb3 = wx.RadioButton(Panel, -1, 'as small circles')


        txt3 = wx.StaticText(Panel, -1, 'Save file as:')
        SaveButton = wx.Button(Panel, wx.ID_SAVEAS, '...', size=(40, 25))
        self.Bind(wx.EVT_BUTTON, self.ChooseSaveFile, id=wx.ID_SAVEAS)
        self.SaveTextCtrl = wx.TextCtrl(Panel, -1)
        self.SaveTextCtrl.SetMinSize((270, -1))

    # populate listbox with names of opened files
        for i in filesList:
            for j in range(len(i[0])):
                self.listbox.Append(i[0][j])

    #layout
        # listbox
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(txt, 0, wx.LEFT, 5)
        vbox1.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 5)

        # options
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(txt2, 0, wx.LEFT, 5)
        vbox2.Add(self.cb_save, 0, wx.ALL, 5)
        vbox2.Add(self.cb_append, 0, wx.LEFT, 5)
        vbox2.Add(self.rb1, 0, wx.TOP | wx.LEFT, 5)
        vbox2.Add(self.rb2, 0, wx.TOP | wx.LEFT, 5)
        vbox2.Add(self.rb4, 0, wx.TOP | wx.LEFT, 5)
        vbox2.Add(self.rb3, 0, wx.TOP | wx.LEFT, 5)

        # listbox + options
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(vbox1, 1, wx.EXPAND) # listbox
        hbox1.Add(vbox2, 0, wx.ALL, 5) # options

        # 'save as' txtctrl and button
        hbox3  = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(self.SaveTextCtrl, 1, wx.EXPAND | wx.ALL, 5) # 'save as' txt ctrl
        hbox3.Add(SaveButton, 0, wx.LEFT | wx.RIGHT | wx.TOP, 5) # 'save as' button

        vbox4 = wx.BoxSizer(wx.VERTICAL)
        vbox4.Add(txt3, 0, wx.LEFT, 5)
        vbox4.Add(hbox3, 1, wx.EXPAND | wx.ALL, 0)  # 'save as' txtctrl and button

        # buttons (OK, Cancel)
        hbox2  = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(mergeButton, 0, wx.BOTTOM, 5)
        hbox2.Add(closeButton, 0, wx.LEFT | wx.BOTTOM , 5)

        # everything

        vbox5 = wx.BoxSizer(wx.VERTICAL)
        vbox5.Add(vbox4, 1, wx.ALL | wx.EXPAND, 5)  # 'save as' txt ctrl and buton
        vbox5.Add(hbox2, 0, wx.ALL | wx.ALIGN_CENTER, 5)  # buttons (OK, Cancel)

        vbox3 = wx.BoxSizer(wx.VERTICAL)
        vbox3.Add(hbox1, 1, wx.ALL | wx.EXPAND, 5)  # listbox + options
        vbox3.Add(vbox5, 0, wx.ALL | wx.EXPAND | wx.ALIGN_BOTTOM, 5)  # 

        Panel.SetSizer(vbox3)
        vbox3.Fit(Panel)
        vbox3.SetSizeHints(Panel)

        dlgbox = wx.BoxSizer(wx.VERTICAL) 
        dlgbox.Add(Panel, 1, wx.EXPAND, 0)
        self.SetSizer(dlgbox)
        dlgbox.Fit(self)
        dlgbox.SetSizeHints(self)

        self.SetFocus()


    def OnSelect(self, event):
        nomMerge = []
        name_list = self.listbox.GetItems()
        # for multiple and single item select use this ...
        pos_tuple = self.listbox.GetSelections()
        selected_list = []
        for pos in pos_tuple:
            selected_list.append(name_list[pos])

        for i in self.filesList: # check if it is planar, linear, fault or small circle
            for j in range(len(i[0])): # all loaded files (P, L, F, or SC)
                for k in selected_list:
                    if k == i[0][j]: # if file in selected_list is the same as the one in filesList
                        nomMerge.append(i[0][j]) # names

        # remove file extensions, join all names and remove white spaces (all at once)
        self.nomMerge = 'Merge_' + "".join(['' if i == ' ' else i for i in "_".join([i[:-4] for i in nomMerge])]) + '.txt'
#        this line is the same as:
#        a = [i[:-4] for i in nomMerge] # remove file extensions
#        b = "_".join(a) # first join
#        c = ['' if i == ' ' else i for i in b] # remove white spaces
#        d = "_".join(c) # second join
#        e = 'Merge_' + d + '.txt'

        self.SaveTextCtrl.SetValue(self.nomMerge)
        self.pathChoosed = 0


#save merged file to txt new file
    def ChooseSaveFile(self, event):
        dlg = wx.FileDialog ( None, message='Save file as', wildcard='Text files (*.txt)|*.txt', style = wx.SAVE | wx.OVERWRITE_PROMPT )

        dlg.SetFilename(self.nomMerge)

        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            self.fullname = os.path.join(self.dirname, self.filename)
            self.SaveTextCtrl.SetValue(self.fullname)
            self.pathChoosed = 1
        else:
           pass

        dlg.Destroy()


#-----------------------------------------------------------------------------
# some stuff about selecting from a listbox are from here: 
# http://www.python-forum.org/pythonforum/viewtopic.php?f=2&t=10297&start=0&sid=231ce1cec401877a7c334fc8fbd94c69

    def onMergeData(self):

        val = self.ShowModal()

        azMerge = [] # dipdir or trend
        dpMerge = [] # dip or plunge
        trMerge = [] # trend of slickenside
        pgMerge = [] # plunge of slickenside
        snMerge = [] # sense of fault
        alphaMerge = [] # radii of small circle
        dataType = [] # datatype

        if val == wx.ID_OK:

            if self.pathChoosed == 1:   # choose a path (and maybe a different name) for the resulting file
                newname = self.fullname
                filename = self.filename
            else:                       # go with the default in the current directory
                newname = os.path.join(os.curdir, self.nomMerge)
                filename = self.nomMerge

            name_list = self.listbox.GetItems()
            pos_tuple = self.listbox.GetSelections()
            selected_list = []
            for pos in pos_tuple:
                selected_list.append(name_list[pos])
                
            for i in self.filesList: # check if it is planar, linear or small circle
                for j in range(len(i[0])): # all loaded files (P, L, F, or SC)
                    for k in selected_list:
                        if k == i[0][j]: # if file in selected_list is the same as the one in filesList
                            print k
                            print i[0][j][1]
                            if i[0][j][1] == 'S':  # small circle
                                #~ print 'small circle'
                                azMerge = azMerge + list(i[2][j]) # azim
                                dpMerge = dpMerge + list(i[3][j]) # dip
                                alphaMerge = alphaMerge + list(i[4][j]) # alpha
                                dataType = dataType + list(i[0][j][1]) # data type (planar, linear, fault, small circle..)
                            elif i[0][j][1] == 'F': 
                                #~ print 'fault'
                                azMerge = azMerge + list(i[2][j]) # azim
                                dpMerge = dpMerge + list(i[3][j]) # dip
                                trMerge = trMerge + list(i[4][j]) # trend
                                pgMerge = pgMerge + list(i[5][j]) # plunge
                                snMerge = snMerge + list(i[6][j]) # sense
                                dataType = dataType + list(i[0][j][1]) # data type (planar, linear, fault, small circle..)
                            elif i[0][j][1] == 'P' or i[0][j][1] == 'L': 
                                #~ print 'planar or linear'
                                azMerge = azMerge + list(i[2][j]) # azim
                                dpMerge = dpMerge + list(i[3][j]) # dip
                                dataType = dataType + list(i[0][j][1]) # data type (planar, linear, fault, small circle..)

            print azMerge, dpMerge, trMerge, pgMerge, snMerge


            return newname, filename, azMerge, dpMerge, trMerge, pgMerge, snMerge, alphaMerge, dataType, \
                    self.cb_append.GetValue(), self.cb_save.GetValue(), \
                    self.rb1.GetValue() , self.rb2.GetValue(), self.rb3.GetValue(), self.rb4.GetValue()

        else:
            return None

        dlg.Destroy()



    def onCloseTool(self, event):
        self.Destroy()










########################## Rotate data
class RotateData(wx.Dialog):
    """Creates a dialog to rotate files"""
    def __init__(self, parent, id, title, filesList):
        wx.Dialog.__init__(self, parent, id, title, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME, size=(200, 250))

        self.filesList = filesList
        self.pathChoosed = 0

        Panel = wx.Panel(self, -1)

        txt = wx.StaticText(Panel, -1, 'Select datasets:')
        self.listbox = wx.ListBox(Panel, -1, style=wx.LB_EXTENDED, size=(180, 150))
        self.Bind(wx.EVT_LISTBOX, self.OnSelect, self.listbox, filesList)

        mergeButton = wx.Button(Panel, wx.ID_OK, 'OK', size=(80, 30))
        closeButton = wx.Button(Panel, wx.ID_CANCEL, 'Cancel', size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.onCloseTool, id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_OK)
        self.SetEscapeId(wx.ID_CANCEL)

        txt2 = wx.StaticText(Panel, -1, 'Options:')
        self.cb_save = wx.CheckBox(Panel, -1, 'Save to disk')
        self.cb_save.SetValue(True)
        self.cb_append = wx.CheckBox(Panel, -1, 'Load rotated file:')
        self.cb_append.SetValue(True)

        self.rb1 = wx.RadioButton(Panel, -1, 'as planes (poles)', style=wx.RB_GROUP)
        self.rb2 = wx.RadioButton(Panel, -1, 'as lines')
        self.rb4 = wx.RadioButton(Panel, -1, 'as faults')
        self.rb3 = wx.RadioButton(Panel, -1, 'as small circles')

        txtRot = wx.StaticText(Panel, -1, 'Rotation Axis')
        txtAx = wx.StaticText(Panel, -1, 'Trend')
        self.spinAx = FS.FloatSpin(Panel, -1, size=(80, -1), value=0, min_val=0, max_val=360, increment=0.5, digits=1)
        txtDx = wx.StaticText(Panel, -1, 'Plunge')
        self.spinDx = FS.FloatSpin(Panel, -1, size=(80, -1), value=0, min_val=0, max_val=90, increment=0.5, digits=1)
        txtHx = wx.StaticText(Panel, -1, 'Rotation Angle')
        self.spinHx = FS.FloatSpin(Panel, -1, size=(80, -1), value=0, min_val=-360, max_val=360, increment=0.5, digits=1)

        self.Bind(wx.EVT_SPINCTRL, self.OnSelect, self.spinAx)
        self.Bind(wx.EVT_SPINCTRL, self.OnSelect, self.spinDx)
        self.Bind(wx.EVT_SPINCTRL, self.OnSelect, self.spinHx)

        txt3 = wx.StaticText(Panel, -1, 'Save file as:')
        SaveButton = wx.Button(Panel, wx.ID_SAVEAS, '...', size=(40, 25))
        self.Bind(wx.EVT_BUTTON, self.ChooseSaveFile, id=wx.ID_SAVEAS)
        self.SaveTextCtrl = wx.TextCtrl(Panel, -1)
        self.SaveTextCtrl.SetMinSize((270, -1))

    # populate listbox with names of opened files
        for i in filesList:
            for j in range(len(i[0])):
                self.listbox.Append(i[0][j])

    #layout
        # listbox
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(txt, 0, wx.LEFT, 5)
        vbox1.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 5)

        # options
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(txt2, 0, wx.LEFT, 5)
        vbox2.Add(self.cb_save, 0, wx.ALL, 5)
        vbox2.Add(self.cb_append, 0, wx.LEFT, 5)
        vbox2.Add(self.rb1, 0, wx.TOP | wx.LEFT, 5)
        vbox2.Add(self.rb2, 0, wx.TOP | wx.LEFT, 5)
        vbox2.Add(self.rb4, 0, wx.TOP | wx.LEFT, 5)
        vbox2.Add(self.rb3, 0, wx.TOP | wx.LEFT, 5)

        # listbox + options
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(vbox1, 1, wx.EXPAND) # listbox
        hbox1.Add(vbox2, 0, wx.ALL, 5) # options

        # rotation axis values
        grid1 = wx.FlexGridSizer(2, 3, 5, 5)

        grid1.Add(txtAx,0, wx.LEFT|wx.TOP, 5)
        grid1.Add(txtDx,0, wx.LEFT|wx.TOP, 5)
        grid1.Add(txtHx,0, wx.LEFT|wx.TOP, 5)
        grid1.Add(self.spinAx,0, wx.LEFT|wx.ALIGN_RIGHT, 5)
        grid1.Add(self.spinDx,0, wx.LEFT|wx.ALIGN_RIGHT, 5)
        grid1.Add(self.spinHx,0, wx.LEFT|wx.ALIGN_RIGHT, 5)

        axis_box = wx.BoxSizer(wx.VERTICAL)
        axis_box.Add(txtRot, 0, wx.LEFT, 5) #
        axis_box.Add(grid1,0)

        # 'save as' txtctrl and button
        hbox3  = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(self.SaveTextCtrl, 1, wx.EXPAND | wx.ALL, 5) # 'save as' txt ctrl
        hbox3.Add(SaveButton, 0, wx.LEFT | wx.RIGHT | wx.TOP, 5) # 'save as' button

        vbox4 = wx.BoxSizer(wx.VERTICAL)
        vbox4.Add(txt3, 0, wx.LEFT, 5)
        vbox4.Add(hbox3, 1, wx.EXPAND | wx.ALL, 0)  # 'save as' txtctrl and button

        # buttons (OK, Cancel)
        hbox2  = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(mergeButton, 0, wx.BOTTOM, 5)
        hbox2.Add(closeButton, 0, wx.LEFT | wx.BOTTOM , 5)

        # everything

        vbox5 = wx.BoxSizer(wx.VERTICAL)
        vbox5.Add(vbox4, 1, wx.ALL | wx.EXPAND, 5)  # 'save as' txt ctrl and buton
        vbox5.Add(hbox2, 0, wx.ALL | wx.ALIGN_CENTER, 5)  # buttons (OK, Cancel)

        vbox3 = wx.BoxSizer(wx.VERTICAL)
        vbox3.Add(hbox1, 1, wx.ALL | wx.EXPAND, 5)  # listbox + options
        vbox3.Add(axis_box, 0, wx.ALL | wx.EXPAND, 5) # rotation axis values
        vbox3.Add(vbox5, 0, wx.ALL | wx.EXPAND | wx.ALIGN_BOTTOM, 0)  # 

        Panel.SetSizer(vbox3)
        vbox3.Fit(Panel)
        vbox3.SetSizeHints(Panel)

        dlgbox = wx.BoxSizer(wx.VERTICAL) 
        dlgbox.Add(Panel, 1, wx.EXPAND, 0)
        self.SetSizer(dlgbox)
        dlgbox.Fit(self)
        dlgbox.SetSizeHints(self)

        self.SetFocus()


    def OnSelect(self, event):
        RotAz = self.spinAx.GetValue()
        RotDp = self.spinDx.GetValue()
        RotHx = self.spinHx.GetValue()

        nomRot = []
        self.name_list = self.listbox.GetItems()
        # for multiple and single item select use this ...
        self.pos_tuple = self.listbox.GetSelections()
        self.selected_list = []
        if len(self.pos_tuple) == 0:
            self.selected_list.append(self.name_list[0])
        else:

            for pos in self.pos_tuple:
                self.selected_list.append(self.name_list[pos])

        for i in self.filesList: # check if it is planar, linear or small circle
            for j in range(len(i[0])): # all loaded files (P, L, or SC)
                for k in self.selected_list:
                    if k == i[0][j]: # if file in selected_list is the same as the one in filesList
                        nomRot.append(i[0][j]) # names
                        if i[0][j][1] == 'P':
                                self.rb1.SetValue(True)
                        elif i[0][j][1] == 'L':
                                self.rb2.SetValue(True)
                        elif i[0][j][1] == 'S':
                                self.rb3.SetValue(True)
                        elif i[0][j][1] == 'F':
                                self.rb4.SetValue(True)                        
                        
                        
        # remove file extensions, and remove white spaces (all at once)
        name = "".join(['' if i == ' ' else i for i in "".join([i[:-4] for i in nomRot])])
        self.nomRotated = 'Rot_' + name + '_trd_' + str(RotAz) + '_plg_' + str(RotDp) + '_rot_' + str(RotHx) + '.txt' 

        self.SaveTextCtrl.SetValue(self.nomRotated)
        self.pathChoosed = 0


#save rotated file to txt new file
    def ChooseSaveFile(self, event):
        dlg = wx.FileDialog ( None, message='Save file as', wildcard='Text files (*.txt)|*.txt', style = wx.SAVE | wx.OVERWRITE_PROMPT )

        dlg.SetFilename(self.nomMerge)

        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            self.fullname = os.path.join(self.dirname, self.filename)
            self.SaveTextCtrl.SetValue(self.fullname)
            self.pathChoosed = 1
        else:
           pass

        dlg.Destroy()


    def sign(self,x): 
        return 1 if x > 0 else x and -1
        
    def DoRotation(self,azim,dip,azrot,diprot,rotang):
        # data
        n = len(azim)
        td = [0] * n
        xr = [0] * n
        yr = [0] * n
        zr = [0] * n
        azr = [0] * n
        dpr = [0] * n
        # direction cosines of line to be rotated
        xd,yd,zd = md.DirCosineRot(azim,dip)
#        print xd,yd,zd
        # direction cosines of rotation axis
        xa,ya,za =  md.DirCosineRot([azrot],[diprot])
        xa = xa[0]
        ya = ya[0]
        za = za[0]
#        print azrot,diprot,xa,ya,za
        # rotation angle
        hx = np.radians(rotang)
        for i in range(n):
            td[i] = (xd[i]*xa + yd[i]*ya + zd[i]*za) * (1 - np.cos(hx)) # dot product
            #flag
            flag = self.sign(np.cos(hx)*zd[i] + td[i]*za + (np.sin(hx)*(xa*yd[i] - ya*xd[i])))
            # rotation matrix
            xr[i] = (np.cos(hx) * xd[i]+td[i] * xa+(np.sin(hx)*(ya*zd[i] - za*yd[i]))) * flag
            yr[i] = (np.cos(hx) * yd[i]+td[i] * ya-(np.sin(hx)*(xa*zd[i] - za*xd[i]))) * flag
            zr[i] = (np.cos(hx) * zd[i]+td[i] * za+(np.sin(hx)*(xa*yd[i] - ya*xd[i]))) * flag

        for i in range(len(azim)):
            azr[i],dpr[i] = md.CalcSphereLow(xr[i],yr[i],zr[i])

        return azr,dpr





#-----------------------------------------------------------------------------
    def onRotateData(self):

#        filesList = [self.Pname, self.Pndata, self.Pazim, self.Pdip, \
#                    self.Lname, self.Lndata, self.Lazim, self.Ldip, \
#                    self.Scname, self.Scndata, self.Scazim, self.Scdip, self.Scalpha]

        val = self.ShowModal()

        if val == wx.ID_OK:

            if self.pathChoosed == 1:   # choose a path (and maybe a different name) for the resulting file
                newname = self.fullname
                filename = self.filename
            else:                       # go with the default in the current directory
                newname = os.path.join(os.curdir, self.nomRotated)
                filename = self.nomRotated

#            name_list = self.listbox.GetItems()
#            pos_tuple = self.listbox.GetSelections()
#            selected_list = []
#            for pos in pos_tuple:
#                selected_list.append(name_list[pos])

            azAx = self.spinAx.GetValue()
            dipAx = self.spinDx.GetValue()
            rotang = self.spinHx.GetValue()
            
            
            trRot = [] # dummy
            pgRot = [] # dummy
            sense = [] # dummy
            alpha =  [] # dummy alpha (radius of small circle)
            
            for i in self.filesList: # check if it is planar, linear or small circle
                for j in range(len(i[0])): # all loaded files (P, L, or SC)
                    for k in self.selected_list:
                        if k == i[0][j]: # if file in selected_list is the same as the one in filesList
                        
                            if i[0][j][1] == 'P': # Planar, we must rotate the _poles_ 
                                azim = i[2][j] # azim
                                azim = [az + 180.0 if az + 180.0 < 360.0 else az + 180.0 - 360.0 for az in azim] # pole azim
                                dip = i[3][j] # plane dip
                                dip = [90.0 - dp for dp in dip] # pole dip
                                dataType = i[0][j][1] # data type
                                
                                # rotate
                                azRot,dpRot = self.DoRotation(azim,dip,azAx,dipAx,rotang)
                                
                                 # planar, we must convert back from poles to dip direction of planes
                                azRot = [ar + 180.0 if ar + 180.0 < 360.0 else ar + 180.0 - 360.0 for ar in azRot]
                                dpRot = [90.0 - dr for dr in dpRot] 
                                
                                
                            elif i[0][j][1] == 'L': # Linear, don't need to change anything here                          
                                azim = i[2][j] # azim
                                dip = i[3][j] # dip
                                dataType = i[0][j][1] # data type
                                azRot,dpRot = self.DoRotation(azim,dip,azAx,dipAx,rotang)

                            elif i[0][j][1] == 'F': # Fault
                                azim = i[2][j] # azim
                                azim = [az + 180.0 if az + 180.0 < 360.0 else az + 180.0 - 360.0 for az in azim] # pole azim
                                dip = i[3][j] # plane dip
                                dip = [90.0 - dp for dp in dip] # pole dip
                                trend = i[4][j] # trend
                                plunge = i[5][j] # plunge                                
                                sense = i[6][j] # sense
                                dataType = i[0][j][1] # data type
                                
                                #planes
                                azRot,dpRot = self.DoRotation(azim,dip,azAx,dipAx,rotang)
                                azRot = [ar + 180.0 if ar + 180.0 < 360.0 else ar + 180.0 - 360.0 for ar in azRot]
                                dpRot = [90.0 - dr for dr in dpRot] 

                                #slickensides
                                trRot,pgRot = self.DoRotation(trend,plunge,azAx,dipAx,rotang)
                                
                            else: # small circle
                                azim = i[2][j] # azim
                                dip = i[3][j] # dip
                                alpha = i[4][j] # alpha
                                dataType = i[0][j][1] # data type



            return newname, filename, azRot, dpRot, trRot, pgRot, sense, alpha, dataType, \
                    self.cb_append.GetValue(), self.cb_save.GetValue(), \
                    self.rb1.GetValue() , self.rb2.GetValue(), self.rb3.GetValue(), self.rb4.GetValue()

        else:
            return None

        dlg.Destroy()



    def onCloseTool(self, event):
        self.Destroy()







