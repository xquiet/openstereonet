from distutils.core import setup
import py2exe
from glob import glob

# Remove the build folder, a bit slower but ensures that build contains the latest
import shutil
shutil.rmtree("build", ignore_errors=True)

# my setup.py is based on one generated with gui2exe, so data_files is done a bit differently
data_files = [("Microsoft.VC90.CRT", glob(r'c:\dev\*.*'))]

includes = ['wx', 'os', 'sys', 'csv', 're', 'floatspin', 'scrolledpanel', 'customtreectrl',
            'wx.lib.expando', 'wx.lib.pubsub', 'wx.lib.embeddedimage', 'wx.lib.wordwrap', 'types',
            'matplotlib', 'matplotlib.pyplot', 'matplotlib.axes', 'matplotlib.figure',
            'matplotlib.backends.backend_wxagg', 'mpl_toolkits.axes_grid.axislines', 'mpl_toolkits.axes_grid',
            'matplotlib.patches', 'matplotlib.lines', 'matplotlib.text', 'matplotlib.mlab', 'matplotlib.nxutils',
            'matplotlib.collections', 'matplotlib.font_manager', 'numpy', 'numpy.ma', 'numpy.linalg', 'math'
            ]

#, 'scipy.interpolate'            
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter', 'pydoc', 'doctest', 'test', 'sqlite3',
            'bsddb', 'curses', 'email','_fltkagg', '_gtk', '_gtkcairo',
            '_agg2', '_cairo', '_cocoaagg', 'matplotlib.backends.backend_qt4agg','matplotlib.backends.backend_qt4',
            'PyQt4', 'PyQt4.QtGui', 'PyQt4.QtCore'
            ]

packages = ['encodings','pytz']#,'scipy']

dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll', 'tk84.dll',
                'libgdk_pixbuf-2.0-0.dll', 'libgtk-win32-2.0-0.dll', 'libglib-2.0-0.dll',
                'libcairo-2.dll', 'libpango-1.0-0.dll', 'libpangowin32-1.0-0.dll', 'libpangocairo-1.0-0.dll',
                'libglade-2.0-0.dll', 'libgmodule-2.0-0.dll', 'libgthread-2.0-0.dll', 'QtGui4.dll', 'QtCore.dll',
                'QtCore4.dll'
                ]
                
icon_resources = [(0,'openstereo.ico')]
bitmap_resources = []
other_resources = []

# add the mpl mpl-data folder and rc file
#import matplotlib as mpl
#data_files += mpl.get_py2exe_datafiles()

 # Save matplotlib-data to mpl-data ( It is located in the matplotlib\mpl-data 
# folder and the compiled programs will look for it in \mpl-data
# note: using matplotlib.get_mpldata_info
data_files += [(r'mpl-data', glob(r'C:\Python26\Lib\site-packages\matplotlib\mpl-data\*.*')),
                    # Because matplotlibrc does not have an extension, glob does not find it (at least I think that's why)
                    # So add it manually here:
                  (r'mpl-data', [r'C:\Python26\Lib\site-packages\matplotlib\mpl-data\matplotlibrc']),
                  (r'mpl-data\images', glob(r'C:\Python26\Lib\site-packages\matplotlib\mpl-data\images\*.png')),
                  (r'mpl-data\fonts\afm', glob(r'C:\Python26\Lib\site-packages\matplotlib\mpl-data\fonts\afm\phvr8a.afm')),
                  (r'mpl-data\fonts\pdfcorefonts', glob(r'C:\Python26\Lib\site-packages\matplotlib\mpl-data\fonts\pdfcorefonts\Helvetica.afm')),
                  (r'mpl-data\fonts\pdfcorefonts', glob(r'C:\Python26\Lib\site-packages\matplotlib\mpl-data\fonts\pdfcorefonts\readme.txt')),
                  (r'mpl-data\fonts\ttf', glob(r'C:\Python26\Lib\site-packages\matplotlib\mpl-data\fonts\ttf\Vera.ttf')),
                  (r'mpl-data\fonts\ttf', glob(r'C:\Python26\Lib\site-packages\matplotlib\mpl-data\fonts\ttf\COPYRIGHT.TXT')),
                  (r'mpl-data\fonts\ttf', glob(r'C:\Python26\Lib\site-packages\matplotlib\mpl-data\fonts\ttf\LICENSE_STIX')),
                  (r'mpl-data\fonts\ttf', glob(r'C:\Python26\Lib\site-packages\matplotlib\mpl-data\fonts\ttf\README.TXT')),
                  (r'mpl-data\fonts\ttf', glob(r'C:\Python26\Lib\site-packages\matplotlib\mpl-data\fonts\ttf\RELEASENOTES.TXT')),
                  ]
                  
setup(
    windows=[{ "script":'OpenStereo.py',
                "icon_resources": icon_resources}],
                          # compressed and optimize reduce the size
    options = {"py2exe": {"compressed": 2, 
                          "optimize": 2,
                          "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          # using 2 to reduce number of files in dist folder
                          # using 1 is not recommended as it often does not work
                          "bundle_files": 2,
                          "dist_dir": 'dist',
                          "xref": False,
                          "skip_archive": False,
                          "ascii": False,
                          "custom_boot_script": '',
                         }
              },

    # using zipfile to reduce number of files in dist
    zipfile = r'lib\library.zip',

    data_files=data_files
)
