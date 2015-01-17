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

import wx
from MainForm import MainFrame

class OpenStereo(wx.App):
    """ OpenStereoNet - Open-source, Multiplatform Stereonet Analysis """
    def OnInit(self):
        # wx.InitAllImageHandlers()
        MainWindow=MainFrame(None, -1, 'OpenStereoNet - Open-source, Multiplatform Stereonet Analysis', size=(800,550))
        self.SetTopWindow(MainWindow)
        MainWindow.Show()
        return True

if __name__ == '__main__':
    app=OpenStereo()
    app.MainLoop()
