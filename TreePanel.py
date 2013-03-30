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
#import wx.lib.agw.customtreectrl as CT
import customtreectrl as CT
from wx.lib.pubsub import Publisher as pub

import PropsDlgs as props

# import i18n
import i18n
_ = i18n.language.ugettext #use ugettext instead of getttext to avoid unicode errors

#---------------------------------------------------------------------------
# CustomTreeCtrl Implementation
#---------------------------------------------------------------------------
class CustomTreeCtrl(CT.CustomTreeCtrl):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.SUNKEN_BORDER,
                 ctstyle=CT.TR_HIDE_ROOT|
                 CT.TR_HAS_BUTTONS|
                 CT.TR_NO_LINES|
                 CT.TR_MULTIPLE|
                 CT.TR_HAS_VARIABLE_ROW_HEIGHT):


        CT.CustomTreeCtrl.__init__(self, parent, id, pos, size, style, ctstyle)

        self.mainframe = wx.GetTopLevelParent(self)
        self.root = self.AddRoot("The Root Item")
        self.itemStereo = self.AppendItem (self.root, 'Stereonet' ,0)
        self.SetItemPyData(self.itemStereo, [0,'stereonet'])

        self.gridSpin = wx.SpinCtrl(self, -1, '10', size=(60, -1), min=1, max=45)
        self.itemGrid = self.AppendItem (self.itemStereo, _('grid') , ct_type=1, wnd=self.gridSpin)
        self.SetItemPyData(self.itemGrid, [0,'grid'])
#        self.CheckItem(self.itemGrid, checked=True)

        gridType=['schmidt','wulff']
        self.gridCombo = wx.ComboBox(self, -1, value=gridType[0], choices=gridType, size=(100, -1), style=wx.CB_READONLY|wx.CB_DROPDOWN)
        subitem = self.AppendItem (self.itemStereo, '' , ct_type=0, wnd=self.gridCombo)
        self.CheckItem(subitem, checked=True)

        self.Expand(self.itemStereo)


        self.Bind(CT.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.OnItemCheck)
        self.Bind(CT.EVT_TREE_ITEM_CHECKING, self.OnItemCheck)
        self.Bind(CT.EVT_TREE_BEGIN_DRAG, self.OnBeginDrag)
        self.Bind(CT.EVT_TREE_END_DRAG, self.OnEndDrag)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_COMBOBOX, self.OnGridCombo,self.gridCombo)
        self.Bind(wx.EVT_SPINCTRL, self.OnGridSpin,self.gridSpin)


# subscriptions to pubsub
        pub.subscribe(self.__onReceivePlanarData, 'object.Plan_added_DDD') # from MainForm
        pub.subscribe(self.__onReceivePlanarData, 'object.Plan_added_RH') # from MainForm
        pub.subscribe(self.__onReceiveLinearData, 'object.Lin_added') # from MainForm
        pub.subscribe(self.__onReceiveSmallData, 'object.Sc_added') # from MainForm
        pub.subscribe(self.__onReceiveFaultData, 'object.Fault_added') # from MainForm
        pub.subscribe(self.__onReceivePProps, 'object.PProps') # from StereoPanel - Planar props
        pub.subscribe(self.__onReceiveLProps, 'object.LProps') # from StereoPanel - Linear props
        pub.subscribe(self.__onReceiveScProps, 'object.ScProps') # from StereoPanel - Smalll circle props
        pub.subscribe(self.__onReceiveFProps, 'object.FProps') # from StereoPanel - Fault props

# pubsub - retrieving planar data
    def __onReceivePlanarData(self, message):

        try:
            len(self.Pname) # dummy action just to see if self.Pname exists
        except:
            self.Pname=[]
            self.Pndata=[]
            self.PeigenList=[]
            self.PidxList=[]
            self.pobjs = ['poles to planes', 'eigenvectors', 'great circles', 'contours']

        for i in range(len(message.data)):
            self.Pname.append(message.data[i][1])
            self.Pndata.append(message.data[i][2])
            self.PeigenList.append(message.data[i][6])
            self.PidxList.append(message.data[i][7])

            if message.data[i][7].startswith('D'): # dip-dir data
                itemName = '[P(dd)] %s' % message.data[i][1]
            else: # right-hand data
                itemName = '[P(rh)] %s' % message.data[i][1]

            item = self.PrependItem (self.root, itemName , ct_type=1)
            self.SetItemPyData(item, [1,message.data[i][7]]) # message.data[i][7] = PidxList
            self.CheckItem(item, checked=True)
            for j in range(len(self.pobjs)):
                subitem = self.AppendItem (item, self.pobjs[j] , ct_type=1)
                self.SetItemPyData(subitem, message.data[i][7]) # message.data[i][7] = PidxList
                if j == 0:
                    self.CheckItem(subitem, checked=True)
            self.Expand(item)
            self.p_opt_dict = message.data[i][8]


# pubsub - retrieving linear data
    def __onReceiveLinearData(self, message):

        try:
            len(self.Lname) # dummy action just to see if self.Lname exists
        except:
            self.Lname=[]
            self.Lndata=[]
            self.LeigenList=[]
            self.LidxList=[]
            self.lobjs = ['poles to lines', 'eigenvectors', 'contours']

        for i in range(len(message.data)):
            self.Lname.append(message.data[i][1])
            self.Lndata.append(message.data[i][2])
            self.LeigenList.append(message.data[i][6])
            self.LidxList.append(message.data[i][7])

            itemName = '[L] %s' % message.data[i][1]
            item = self.PrependItem (self.root, itemName , ct_type=1)
            self.SetItemPyData(item, [2,message.data[i][7]])  # message.data[i][7] = LidxList
            self.CheckItem(item, checked=True)
            for j in range(len(self.lobjs)):
                subitem = self.AppendItem (item, self.lobjs[j] , ct_type=1)
                self.SetItemPyData(subitem, message.data[i][7])  # message.data[i][7] = LidxList
                if j == 0:
                    self.CheckItem(subitem, checked=True)
            self.Expand(item)
            self.l_opt_dict = message.data[i][8]


# pubsub - retrieving small circle data
    def __onReceiveSmallData(self, message):

        try:
            len(self.Scname) # dummy action just to see if self.Scname exists
        except:
            self.Scname=[]
            self.Scndata=[]
            self.ScidxList=[]

        for i in range(len(message.data)):
            self.Scname.append(message.data[i][1])
            self.Scndata.append(message.data[i][2])
            self.ScidxList.append(message.data[i][6])

            itemName = '[SC] %s' % message.data[i][1]
            item = self.PrependItem (self.root, itemName , ct_type=1)
            self.SetItemPyData(item, [3,message.data[i][6]])  # message.data[i][6] = ScidxList
            self.CheckItem(item, checked=True)
            self.Expand(item)
            self.sc_opt_dict = message.data[i][7]


# pubsub - retrieving fault data
    def __onReceiveFaultData(self, message):

        try:
            len(self.Fname) # dummy action just to see if self.Fname exists
        except:
            self.Fname=[]
            self.Fndata=[]
            self.FidxList=[]
            self.fobjs = ['great circles', 'slickensides', 'slip']

        for i in range(len(message.data)):
            self.Fname.append(message.data[i][1])
            self.Fndata.append(message.data[i][2])
            self.FidxList.append(message.data[i][10])

            itemName = '[F] %s' % message.data[i][1]
            item = self.PrependItem (self.root, itemName , ct_type=1)
            self.SetItemPyData(item, [4,message.data[i][10]])  # message.data[i][10] = FidxList
            self.CheckItem(item, checked=True)
            for j in range(len(self.fobjs)):
                subitem = self.AppendItem (item, self.fobjs[j] , ct_type=1)
                self.SetItemPyData(subitem, message.data[i][10])  # message.data[i][10] = FidxList
                if j == 0 or j==1:
                    self.CheckItem(subitem, checked=True)
            self.Expand(item)
            self.f_opt_dict = message.data[i][11]

            #self.faultData.append([filetype,filename,n_data,dipdir,dip,strike,eigenList,trend,plunge,sense,F_idx,self.fplist]


# pubsub - retrieving planar properties list
    def __onReceivePProps(self, message):
        self.PPropsList = message.data

# pubsub - retrieving linear properties list
    def __onReceiveLProps(self, message):
        self.LPropsList = message.data

# pubsub - retrieving small circle properties list
    def __onReceiveScProps(self, message):
        self.ScPropsList = message.data

# pubsub - retrieving fault properties list
    def __onReceiveFProps(self, message):
        self.FPropsList = message.data


# refresh list of selected itens when spinctrl (grid step) changes
    def OnGridSpin(self, event):
        self.OnItemCheck(event)
#        print self.gridSpin.GetValue()
        event.Skip()

# refresh list of selected itens when combobox (schmidt/wulff) selection changes
    def OnGridCombo(self, event):
        self.OnItemCheck(event)
#        print self.gridCombo.GetValue()
        event.Skip()


# function to retrieve list of checked items, from Andrea Gavana with fixes by Robin Dunn
# http://groups.google.com/group/wxPython-users/browse_thread/thread/e29af467cfe6dfa?hl=en

    def GetCheckedItems(self, itemParent=None, checkedItems=None):

        if itemParent is None:
            itemParent = self.GetRootItem()
        if checkedItems is None:
            checkedItems = []

        child, cookie = self.GetFirstChild(itemParent)

        while child:
            if self.IsItemChecked(child):
                checkedItems.append(child)

            checkedItems = self.GetCheckedItems(child, checkedItems)
            child, cookie = self.GetNextChild(itemParent, cookie)

        return checkedItems 

# action on check/uncheck items - returns list of checked items via pubsub
    def OnItemCheck(self, event):
        checked = self.GetCheckedItems()
        namesList = [] # checked files - names
        itemsList = [] # checked files - memory adresses

        for i in checked: # get the data files that are checked
            itemName = self.GetItemText(i)
            pdata = self.GetItemPyData(i)
        #   itemIdx = pdata

            if self.GetItemParent(i) == self.GetRootItem() and pdata[0] == 1: # 1 == self.itemPlanar:
                namesList.append([pdata[1],1]) #itemIdx = pdata[1]
                itemsList.append(i)

            elif self.GetItemParent(i) == self.GetRootItem() and pdata[0] == 2: # 2 == self.itemLinear:
                namesList.append([pdata[1],2])
                itemsList.append(i)

            elif self.GetItemParent(i) == self.GetRootItem() and pdata[0] == 3: # 3 == self.itemSmall:
                namesList.append([pdata[1],3])
                itemsList.append(i)

            elif self.GetItemParent(i) == self.GetRootItem() and pdata[0] == 4: # 4 == self.itemFault:
                namesList.append([pdata[1],4])
                itemsList.append(i)

            # see if stereonet grid is checked (must be last item on checked list)
            elif self.GetItemParent(i) == self.itemStereo: # and pdata[0] == 0: # 0 == self.itemGrid:
                namesList.append([pdata[1],0])
                itemsList.append(i)

        # properties of stereonet: draw grid lines, Schmidt/Wulff
        pub.sendMessage('object.grid', [self.gridSpin.GetValue(),self.gridCombo.GetValue()]) # send to StereoPanel


        for i in checked: # get the options that are checked for each checked data file
            for j in itemsList:
                indx_i = checked.index(i)
                indx_j = itemsList.index(j)
                itemName = self.GetItemText(i)
                if self.GetItemParent(i) == j and namesList[indx_j][1] == 1: # 1 == self.itemPlanar:
                    namesList[indx_j].append(self.pobjs.index(itemName)+10)
                elif self.GetItemParent(i) == j and namesList[indx_j][1] == 2: # 2 == self.itemLinear:
                    namesList[indx_j].append(self.lobjs.index(itemName)+10)
                elif self.GetItemParent(i) == j and namesList[indx_j][1] == 4: # 4 == self.itemFault:
                    namesList[indx_j].append(self.fobjs.index(itemName)+10)

        pub.sendMessage('object.checked', namesList) # send to StereoPanel
        event.Skip()



# action on select item (single-click) - print stats in textCtrl (actual printing in StatsPanel.py)
    def OnSelChanged(self, event):

        item = event.GetItem()
        itemName = self.GetItemText(item)
        pdata = self.GetItemPyData(item)

        if self.GetItemParent(item) == self.GetRootItem() and pdata[0] == 1: # 1 == self.itemPlanar:
            i = self.PidxList.index(pdata[1])
            namedata = {"itemName":itemName,"dtype":1,"ndata":self.Pndata[i]}
            eigen = self.PeigenList[i]
            namedata.update(eigen)
            pub.sendMessage('object.selected', i) # send to StatsPanel
            pub.sendMessage('object.selected_vals',namedata)

        elif self.GetItemParent(item) == self.GetRootItem() and pdata[0] == 2: # 2 == self.itemLinear:
            i = self.LidxList.index(pdata[1])
            namedata = {"itemName":itemName,"dtype":2, "ndata":self.Lndata[i]}
            eigen = self.LeigenList[i]
            namedata.update(eigen)
            pub.sendMessage('object.selected', i) # send to StatsPanel
            pub.sendMessage('object.selected_vals', namedata)

        elif self.GetItemParent(item) == self.GetRootItem() and pdata[0] == 3: # 3 == self.itemSmall:
            i = self.ScidxList.index(pdata[1])
            pub.sendMessage('object.selected', i) # send to StatsPanel
            pub.sendMessage('object.selected_vals', {"itemName":itemName,"dtype":3, "ndata":self.Scndata[i]})

        elif self.GetItemParent(item) == self.GetRootItem() and pdata[0] == 4: # 4 == self.itemFault:
            i = self.FidxList.index(pdata[1])
            pub.sendMessage('object.selected', i) # send to StatsPanel
            pub.sendMessage('object.selected_vals', {"itemName":itemName,"dtype":4, "ndata":self.Fndata[i]})

        elif self.GetItemParent(item) == self.GetRootItem() and pdata[0] == 0:
            pass

        event.Skip()

# ---------------------

# left click down, select item
    def OnLeftDown(self, event):
        pt = event.GetPosition()
        item, flags = self.HitTest(pt)
        if item:
            self.item = item
        else:
            self.UnselectAll()

        event.Skip()


# right click down, select item
    def OnRightDown(self, event):
        pt = event.GetPosition()
        item, flags = self.HitTest(pt)
        if item:
            self.item = item
#            print 'right DOWN!!!'
#            self.SelectItem(item)
        event.Skip()

#right click up, perform action (open pop-up menu)
    def OnRightUp(self, event):
        item = self.item
        pdata = self.GetItemPyData(item)

        if not item:
            event.Skip()
            return

        menu = wx.Menu()
        propsdlg = menu.Append(-1, "Properties")
        delitem = menu.Append(-1, "Delete item")

        self.Bind(wx.EVT_MENU, self.OnItemDelete, delitem)

        menu2 = wx.Menu()
        propsdlg2 = menu2.Append(-1, "Properties")

        if self.GetItemParent(item) == self.GetRootItem() and pdata[0] == 1: # 1 == self.itemPlanar:
            self.Bind(wx.EVT_MENU, self.OnProps_childPlanar, propsdlg)
            self.PopupMenu(menu, event.GetPosition())
            menu.Destroy()
        elif self.GetItemParent(item) == self.GetRootItem() and pdata[0] == 2: # 2 == self.itemLinear:
            self.Bind(wx.EVT_MENU, self.OnProps_childLinear, propsdlg)
            self.PopupMenu(menu, event.GetPosition())
            menu.Destroy()
        elif self.GetItemParent(item) == self.GetRootItem() and pdata[0] == 3: # 3 == self.itemSmall:
            self.Bind(wx.EVT_MENU, self.OnProps_childSmall, propsdlg)
            self.PopupMenu(menu, event.GetPosition())
            menu.Destroy()
        elif self.GetItemParent(item) == self.GetRootItem() and pdata[0] == 4: # 4 == self.itemFault:
            self.Bind(wx.EVT_MENU, self.OnProps_childFault, propsdlg)
            self.PopupMenu(menu, event.GetPosition())
            menu.Destroy()
        event.Skip()

#left double click, call properties dlg
    def OnLeftDClick(self, event):

        try:
            pt = event.GetPosition()
            item, flags = self.HitTest(pt)
    #        self.item = item
            pdata = self.GetItemPyData(item)
        except:
            pass

        if not item:
            # no item hit
            return

        if self.GetItemParent(item) == self.GetRootItem() and pdata[0] == 1: # 1 == self.itemPlanar:
            self.OnProps_childPlanar(pt)
        elif self.GetItemParent(item) == self.GetRootItem() and pdata[0] == 2: # 2 == self.itemLinear:
            self.OnProps_childLinear(pt)
        elif self.GetItemParent(item) == self.GetRootItem() and pdata[0] == 3: # 3 == self.itemSmall:
            self.OnProps_childSmall(pt)
        elif self.GetItemParent(item) == self.GetRootItem() and pdata[0] == 4: # 4 == self.itemSmall:
            self.OnProps_childFault(pt)

#        event.Skip()



# props of planar children
    def OnProps_childPlanar(self, event):

        try:
            itemName = self.GetItemText(self.item)
            pdata = self.GetItemPyData(self.item)
            i = self.PidxList.index(pdata[1])

            try:
                opt_dict = self.PPropsList[i]
            except:
                opt_dict = self.p_opt_dict

            dlg = props.PlanarOptions(self, -1, 'Display Options - Planes', opt_dict)

            try: # default properties are defined in MainForm
                PolColor, symbPoles, polespin,\
                CircColor, styleCirc, circspin, \
                cb_eigen_gc1, CircGirdColor1, styleGirdCirc1, circGirdspin1, \
                cb_eigen_p1, PolGirdColor1, symbGirdPoles1, poleGirdspin1, \
                cb_eigen_gc2, CircGirdColor2, styleGirdCirc2, circGirdspin2, \
                cb_eigen_p2, PolGirdColor2, symbGirdPoles2, poleGirdspin2, \
                cb_eigen_gc3, CircGirdColor3, styleGirdCirc3, circGirdspin3, \
                cb_eigen_p3, PolGirdColor3, symbGirdPoles3, poleGirdspin3, \
                cntNodes, percent, interpol, gridSpin, \
                contStyle, contColor, contFill, contLws, colormap, contcolormap, addedges, \
                rbsc, rbcm, antial, minmax, zeromax, numcontours, custom, customcont, \
                rbcossum, expSpin, rbfisher, kSpin, rbscarea, areaSpin, \
                rbscangle, angleSpin, conCircSty, conCircColor, conspin, cb_conf = dlg.onPlanProps()
#epsilSpin, smootSpin, 

                propsPList = {"pdata":pdata[1], "itemName":itemName, \
                    "PolColor":PolColor, "PoleSymb":symbPoles, "polespin":polespin, \
                    "CircColor":CircColor, "CircSty":styleCirc, "circspin":circspin, \
                    "cb_eigen_gc1":cb_eigen_gc1, "CircGirdColor1":CircGirdColor1, "styleGirdCirc1":styleGirdCirc1, "circGirdspin1":circGirdspin1, \
                    "cb_eigen_p1":cb_eigen_p1, "PolGirdColor1":PolGirdColor1, "symbGirdPoles1":symbGirdPoles1, "poleGirdspin1":poleGirdspin1, \
                    "cb_eigen_gc2":cb_eigen_gc2, "CircGirdColor2":CircGirdColor2, "styleGirdCirc2":styleGirdCirc2, "circGirdspin2":circGirdspin2, \
                    "cb_eigen_p2":cb_eigen_p2, "PolGirdColor2":PolGirdColor2, "symbGirdPoles2":symbGirdPoles2, "poleGirdspin2":poleGirdspin2, \
                    "cb_eigen_gc3":cb_eigen_gc3, "CircGirdColor3":CircGirdColor3, "styleGirdCirc3":styleGirdCirc3, "circGirdspin3":circGirdspin3, \
                    "cb_eigen_p3":cb_eigen_p3, "PolGirdColor3":PolGirdColor3, "symbGirdPoles3":symbGirdPoles3, "poleGirdspin3":poleGirdspin3, \
                    "count_nodes":cntNodes, "percent":percent, "interpolation":interpol, "gridSpin":gridSpin, \
                    "contStyle":contStyle, "contColor":contColor, "contFill":contFill, "contLws":contLws, "colormap":colormap, \
                    "contcolormap":contcolormap, "addedges":addedges, "rbsc":rbsc, "rbcm":rbcm, "antiAliased":antial, "minmax":minmax, "zeromax":zeromax, \
                    "numcontours":numcontours, "custom":custom, "customcont":customcont, "rbcossum":rbcossum, "expSpin":expSpin, "rbfisher":rbfisher, \
                    "kSpin":kSpin, "rbscarea":rbscarea, "areaSpin":areaSpin, "rbscangle":rbscangle, "angleSpin":angleSpin, \
                    "conCircSty":conCircSty, "conCircColor":conCircColor, "conspin":conspin, "cb_conf":cb_conf}
# "epsilon":epsilSpin, "smoothing":smootSpin, \

                pub.sendMessage('object.PropsPlanReceiv', propsPList) # send to StereoPanel and StatsPanel
            except:
                pass
        except AttributeError:
            pass

# props of linear children
    def OnProps_childLinear(self, event):

        try:

            itemName = self.GetItemText(self.item)
            pdata = self.GetItemPyData(self.item)
            i = self.LidxList.index(pdata[1])

            try:
                opt_dict = self.LPropsList[i]
            except:
                opt_dict = self.l_opt_dict

            dlg = props.LinearOptions(self, -1, 'Display Options - Lineations', opt_dict)

            try: # default properties are defined in MainForm
                LinColor, LineSymb, linespin, \
                cb_eigen_gc1, CircGirdColor1, styleGirdCirc1, circGirdspin1, \
                cb_eigen_p1, PolGirdColor1, symbGirdPoles1, poleGirdspin1, \
                cb_eigen_gc2, CircGirdColor2, styleGirdCirc2, circGirdspin2, \
                cb_eigen_p2, PolGirdColor2, symbGirdPoles2, poleGirdspin2, \
                cb_eigen_gc3, CircGirdColor3, styleGirdCirc3, circGirdspin3, \
                cb_eigen_p3, PolGirdColor3, symbGirdPoles3, poleGirdspin3, \
                cntNodes, percent, interpol, gridSpin, \
                contStyle, contColor, contFill, contLws, colormap, contcolormap, addedges, \
                rbsc, rbcm, antial, minmax, zeromax, numcontours, custom, customcont, \
                rbcossum, expSpin, rbfisher, kSpin, rbscarea, areaSpin, \
                rbscangle, angleSpin, conCircSty, conCircColor, conspin, cb_conf = dlg.onLinProps()
#epsilSpin, smootSpin, 

                propsLList = {"pdata":pdata[1], "itemName":itemName, \
                    "LinColor":LinColor, "LineSymb":LineSymb, "linespin":linespin,\
                    "cb_eigen_gc1":cb_eigen_gc1, "CircGirdColor1":CircGirdColor1, "styleGirdCirc1":styleGirdCirc1, "circGirdspin1":circGirdspin1, \
                    "cb_eigen_p1":cb_eigen_p1, "PolGirdColor1":PolGirdColor1, "symbGirdPoles1":symbGirdPoles1, "poleGirdspin1":poleGirdspin1, \
                    "cb_eigen_gc2":cb_eigen_gc2, "CircGirdColor2":CircGirdColor2, "styleGirdCirc2":styleGirdCirc2, "circGirdspin2":circGirdspin2, \
                    "cb_eigen_p2":cb_eigen_p2, "PolGirdColor2":PolGirdColor2, "symbGirdPoles2":symbGirdPoles2, "poleGirdspin2":poleGirdspin2, \
                    "cb_eigen_gc3":cb_eigen_gc3, "CircGirdColor3":CircGirdColor3, "styleGirdCirc3":styleGirdCirc3, "circGirdspin3":circGirdspin3, \
                    "cb_eigen_p3":cb_eigen_p3, "PolGirdColor3":PolGirdColor3, "symbGirdPoles3":symbGirdPoles3, "poleGirdspin3":poleGirdspin3, \
                    "count_nodes":cntNodes, "percent":percent, "interpolation":interpol, "gridSpin":gridSpin, \
                    "contStyle":contStyle, "contColor":contColor, "contFill":contFill, "contLws":contLws, "colormap":colormap, \
                    "contcolormap":contcolormap, "addedges":addedges, "rbsc":rbsc, "rbcm":rbcm, "antiAliased":antial, "minmax":minmax, "zeromax":zeromax, \
                    "numcontours":numcontours, "custom":custom, "customcont":customcont, "rbcossum":rbcossum, "expSpin":expSpin, "rbfisher":rbfisher, \
                    "kSpin":kSpin, "rbscarea":rbscarea, "areaSpin":areaSpin, "rbscangle":rbscangle, "angleSpin":angleSpin, \
                    "conCircSty":conCircSty, "conCircColor":conCircColor, "conspin":conspin, "cb_conf":cb_conf}
# "epsilon":epsilSpin, "smoothing":smootSpin, \

                pub.sendMessage('object.PropsLinReceiv', propsLList)   # send to StereoPanel and StatsPanel
            except:
                pass
        except AttributeError:
            pass

# props of small circle children
    def OnProps_childSmall(self, event):

        try:
            itemName = self.GetItemText(self.item)
            pdata = self.GetItemPyData(self.item)
            i = self.ScidxList.index(pdata[1])

            try:
                opt_dict = self.ScPropsList[i]
            except:
                opt_dict = self.sc_opt_dict

            dlg = props.SmallOptions(self, -1, 'Display Options - Small Circles', opt_dict)

            try:
                ScColor, ScSty, ScSpin = dlg.onSmallProps()
                propsScList = {"pdata":pdata[1],"itemName":itemName,"ScColor":ScColor,"ScSty":ScSty,"ScSpin":ScSpin, "ScFull":False}
                pub.sendMessage('object.PropsScReceiv', propsScList)    #send to StereoPanel
            except:
                pass
        except AttributeError:
            pass


# props of fault children
    def OnProps_childFault(self, event):

#        try:
        itemName = self.GetItemText(self.item)
        pdata = self.GetItemPyData(self.item)
        i = self.FidxList.index(pdata[1])

        try:
            opt_dict = self.FPropsList[i]
        except:
            opt_dict = self.f_opt_dict

        dlg = props.FaultOptions(self, -1, 'Display Options - Fault Data', opt_dict)

#        try:
        FaultCircColor, FaultCircSty, FaultCircSpin, \
        SlickPlotPoles, SlickPoleColor, SlickPoleSymb, SlickPoleSpin, \
        SlickArrowSpin, SlickArrowColor, SlickArrowWidthSpin, \
        DisplacePlotPoles, DisplacePoleColor, DisplacePoleSymb, DisplacePoleSpin, \
        DisplaceArrowSpin,DisplaceArrowColor,DisplaceArrowWidthSpin,footwall = dlg.onFaultProps()
        propsFList = {"pdata":pdata[1],"itemName":itemName, \
            "FaultCircColor":FaultCircColor, "FaultCircSty":FaultCircSty, "FaultCircSpin":FaultCircSpin, \
            "SlickPlotPoles":SlickPlotPoles, "SlickPoleColor":SlickPoleColor, "SlickPoleSymb":SlickPoleSymb, "SlickPoleSpin":SlickPoleSpin, \
            "SlickArrowSpin":SlickArrowSpin, "SlickArrowColor":SlickArrowColor, "SlickArrowWidthSpin":SlickArrowWidthSpin, \
            "DisplacePlotPoles":DisplacePlotPoles, "DisplacePoleColor":DisplacePoleColor, "DisplacePoleSymb":DisplacePoleSymb, "DisplacePoleSpin":DisplacePoleSpin, \
            "DisplaceArrowSpin":DisplaceArrowSpin, "DisplaceArrowColor":DisplaceArrowColor, "DisplaceArrowWidthSpin":DisplaceArrowWidthSpin, "footwall":footwall}

        pub.sendMessage('object.PropsFReceiv', propsFList)   # send to StereoPanel
#        except:
#            pass
#        except AttributeError:
#            pass


# delete item from tree
    def OnItemDelete(self, event):

        item = self.item
        pdata = self.GetItemPyData(item)
        i = j = k = v = None

        if self.GetItemParent(item) == self.GetRootItem() and pdata[0] == 1: # 1 == self.itemPlanar:
            i = self.PidxList.index(pdata[1])

        elif self.GetItemParent(item) == self.GetRootItem() and pdata[0] == 2: # 2 == self.itemLinear:
            j = self.LidxList.index(pdata[1])

        elif self.GetItemParent(item) == self.GetRootItem() and pdata[0] == 3: # 3 == self.itemSmall:
            k = self.ScidxList.index(pdata[1])

        elif self.GetItemParent(item) == self.GetRootItem() and pdata[0] == 4: # 4 == self.itemSmall:
            v = self.FidxList.index(pdata[1])


        dlg = wx.MessageDialog(None, 'Delete item?', 'Deleting Item', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        if dlg.ShowModal() in [wx.ID_NO, wx.ID_CANCEL]: #== wx.ID_NO: #
            dlg.Destroy()
            return
        dlg.Destroy()

        self.DeleteChildren(item)
        self.Delete(item)
        self.item = None
        self.OnItemCheck(event)
        pub.sendMessage('object.ItemDelete', event)   # send to StereoPanel, to redraw stereonet
        pub.sendMessage('object.IdxItemsDeleted', [i,j,k,v])   # send to Mainform
        event.Skip()        
        try:
            self.OnItemCheck(CT.EVT_TREE_ITEM_CHECKED)
        except AttributeError:
            pass




    def OnBeginDrag(self, event):

        self.item = event.GetItem()
        if self.item:
#            print "Beginning Drag..." + "\n"


            pdata = self.GetItemPyData(self.item)

            event.Allow()
            event.Skip()




    def OnEndDrag(self, event):

        self.item = event.GetItem()
        if self.item:
#            print "Ending Drag!" + "\n"

            event.Skip()            

#        


#    def OnBeginDrag(self, event):
#        '''Allow drag-and-drop for leaf nodes.'''
#        self.log.WriteText("OnBeginDrag")
#        if self.tree.GetChildrenCount(event.GetItem()) == 0:
#            event.Allow()
#            self.dragItem = event.GetItem()
#        else:
#            self.log.WriteText("Cant drag a node that has children")


#    def OnEndDrag(self, event):
#        '''Do the re-organization if possible'''

#        self.log.WriteText("OnEndDrag")
#       #If we dropped somewhere that isn't on top of an item, ignore the event
#        if not event.GetItem().IsOk():
#            return

#        # Make sure this memeber exists.
#        try:
#            old = self.dragItem
#        except:
#            return

#        # Get the other IDs that are involved
#        new = event.GetItem()
#        parent = self.tree.GetItemParent(new)
#        if not parent.IsOk():
#            return

#        # Move 'em
#        text = self.tree.GetItemText(old)
#        self.tree.Delete(old)
#        self.tree.InsertItem(parent, new, text)






##pos = wx.GetMousePosition()
##treePosition = self.treeCtrl.GetScreenPosition()
##treeSize = self.treeCtrl.GetSize()
##if pos[0]<treePosition[0] or pos[0]>treePosition[0]+treeSize[0] or
##pos[1]<treePosition[1] or pos[1]>treePosition[1]+treeSize[1]:
##         print "out of bounds"
##         return 
















    def OnToolTip(self, event):

        item = event.GetItem()
        if item:
            event.SetToolTip(wx.ToolTip(self.GetItemText(item)))


    def OnItemMenu(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnItemMenu: %s" % self.GetItemText(item) + "\n")
    
        event.Skip()
        
        
    def OnActivate(self, event):
        
        if self.item:
            self.log.write("OnActivate: %s" % self.GetItemText(self.item) + "\n")

        event.Skip()


    def OnItemPrepend(self, event):

        dlg = wx.TextEntryDialog(self, "Please Enter The New Item Name", 'Item Naming', 'Python')

        if dlg.ShowModal() == wx.ID_OK:
            newname = dlg.GetValue()
            newitem = self.PrependItem(self.current, newname)
            self.EnsureVisible(newitem)

        dlg.Destroy()
        event.Skip()


    def OnItemAppend(self, event):

        dlg = wx.TextEntryDialog(self, "Please Enter The New Item Name", 'Item Naming', 'Python')

        if dlg.ShowModal() == wx.ID_OK:
            newname = dlg.GetValue()
            newitem = self.AppendItem(self.current, newname)
            self.EnsureVisible(newitem)

        dlg.Destroy()
        event.Skip()
        


    def OnItemExpanded(self, event):
        
        item = event.GetItem()
        if item:
            self.log.write("OnItemExpanded: %s" % self.GetItemText(item) + "\n")



        
    def OnItemCollapsed(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnItemCollapsed: %s" % self.GetItemText(item) + "\n")
            


