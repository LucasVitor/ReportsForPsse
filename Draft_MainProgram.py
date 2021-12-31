# draft
import pprint
import os, sys,subprocess


#Create a function to reset the screen and close opened pdf files.
clear = lambda: os. system('cls')                                   # Limpa a tela ao iniciar o programa
clear()

cwd = os.getcwd() 

pythonCode = os.path.join(cwd, 'Scripts')

if os.path.isdir(pythonCode):
    if pythonCode not in sys.path:
        sys.path.insert(1, pythonCode)

if 'PYTHONCODE' not in os.environ:
    os.environ.update({'PYTHONCODE':pythonCode})

    

#try:  os.system('taskkill/im FoxitPDFReader.exe /t /f')
#except OSError:
#    print('file not opened')


# Create a class to get file paths and check the system
outfile ='C:\\Users\\Lucas\\Google Drive\\23 - Job Seeking Engineer\\1 - Preparation Material\\16_Git_Projects\\1_Report_Psse\\OUTs\\savnw_faults_SB1_b152.out'
savfile ='C:\\Users\\Lucas\\Google Drive\\23 - Job Seeking Engineer\\1 - Preparation Material\\16_Git_Projects\1_Report_Psse\\CASEssavnw.sav'
xlsxfile ='C:\\Users\\Lucas\\Google Drive\\23 - Job Seeking Engineer\\1 - Preparation Material\\16_Git_Projects\\1_Report_Psse\\OUTs\\exemplo.xlsx'
resultfile ='C:\\Users\\Lucas\\Google Drive\\23 - Job Seeking Engineer\\1 - Preparation Material\\16_Git_Projects\\1_Report_Psse\\OUTs\\resultpdf.pdf' 

# Create a object study with all data from .out file
import dyntools
studyobj = dyntools.CHNF(outfile)
chanrange = studyobj.get_range()
short_title, chanid, chandata = studyobj.get_data()


#print (short_title,chanid)
#excelfile = studyobj.xlsout(xlsxfile)

from Channels import Channel

#ch1 = Channel(chanid[109],chandata[109])
ch1 = Channel("VOLT 3001 [MINE 230.00]",chandata[109],debug=True)
ch1.characterize()

quit()
#Create an object with all data from .sav file
import caspy
casedata = caspy.Savecase(savfile)
 
# connecting channel with element .out to .sav

#pprint.pprint(dict(chanrange), width=1)
#quit()

pprint.pprint(dict(casedata.pssbrn), width=1)
#print('L38',type(casedata))
#pprint.pprint(dict(casedata.pssbus), width=1)
#print('\n')

#busname ={}
#for i in casedata.pssbus['NAME']:
#    print i
#pprint.pprint(dict(busname), width=1)



#from i in 


time = chandata['time']
chan1 = chandata[3]
chan2 = chandata[4]
chan3 = chandata[5]
chan4 = chandata[6]
#print(short_title)
#print(chanid)
#excelfile = chnfobj.xlsout(xlsxfile)

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.gridspec as gridspec

fig = plt.figure()
gs  = gridspec.GridSpec(2, 2, figure=fig)



ax1 = fig.add_subplot(gs[0,0])
ax1.plot(time, chan1)
ax1.plot(time, chan2)
ax1.set_xlabel('time [s]')
ax1.set_ylabel('Channel1')
ax1.legend(['Legenda 1'])



"""
line1, = ax.plot([1, 2, 3], label='label1')
line2, = ax.plot([1, 2, 3], label='label2')
ax.legend(handles=[line1, line2])
"""

ax2 = fig.add_subplot(gs[0,1])
ax2.plot(time, chan2)
ax2.set_xlabel('time [s]')
ax2.set_ylabel('Channel1')

ax3 = fig.add_subplot(gs[1,0])
ax3.plot(time, chan3)
ax3.set_xlabel('time [s]')
ax3.set_ylabel('Channel1')

ax4 = fig.add_subplot(gs[1, 1])
ax4.plot(time, chan4)
ax4.set_xlabel('time [s]')
ax4.set_ylabel('Channel1')

#fig.set_figwidth(10)
#fig.set_figheight(6)

"""
ax4 = fig.add_subplot(gs[2, 2])
ax4.plot(time, chan3)
ax4.set_xlabel('time [s]')
ax4.set_ylabel('Channel1')
#gs1 = gridspec.GridSpec(2,1,)
#gs1 = gridspec.GridSpec(2,1)
#fig, (ax0, ax1) = plt.subplots(2, 1)

fig.set_figwidth(10)
fig.set_figheight(6)
#ax0.plot(time,chan1)
#ax0.plot(time, chan3)
#ax1.plot(time,chan2)
"""
fig.tight_layout()
#plt.show()

#fig_width, fig_height = plt.gcf().get_size_inches()
#print(fig_width, fig_height)

figsize = plt.gcf()
size = figsize.get_size_inches()*figsize.dpi

# 595 x 842
#2480 pixels x 3508 pixels (print resolution)
#595 pixels x 842 pixels (screen resolution)


fig_width  = figsize.get_figwidth()*100
fig_height = figsize.get_figheight()*100
freewidth =595.06
freeheigth =841.71


if fig_width > freewidth:
    newwidth = freewidth
    newheigth = (freewidth/fig_width)*fig_height 
    fig_width  = newwidth
    fig_height = newheigth
else: 
    newwidth = fig_width
    newheigth = fig_height    
if fig_height > freeheigth:
    newheight = freeheigth
    newwidth  = (freeheigth/fig_height)*fig_width
    fig_width  = newwidth
    fig_height = newheigth 
else:
    newwidth = fig_width
    newheigth = fig_height




from reportlab.rl_config import defaultPageSize
PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]

# 1 pixel (X)	0.0264583333 cm






from matplotlib.backends.backend_pdf import PdfPages
from reportlab.platypus import Paragraph,BaseDocTemplate, SimpleDocTemplate, Spacer, Flowable
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from pdfrw import PdfReader, PdfDict
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO


class PdfImage(Flowable):
    """
    Generates a reportlab image flowable for matplotlib figures. It is initialized
    with either a matplotlib figure or a pointer to a list of pagexobj objects and
    an index for the pagexobj to be used.
    """
    def __init__(self, fig=None, width=200, height=200, cache=None, cacheindex=0):
        self.img_width = width
        self.img_height = height
        if fig is None and cache is None:
            raise ValueError("Either 'fig' or 'cache' must be provided")
        if fig is not None:
            imgdata = BytesIO()
            fig.savefig(imgdata, format='pdf')
            imgdata.seek(0)
            page, = PdfReader(imgdata).pages
            image = pagexobj(page)
            self.img_data = image
        else:
            self.img_data = None
        self.cache = cache
        self.cacheindex = cacheindex

    def wrap(self, width, height):
        return self.img_width, self.img_height

    def drawOn(self, canv, x, y, _sW=0):
        if _sW > 0 and hasattr(self, 'hAlign'):
            a = self.hAlign
            if a in ('CENTER', 'CENTRE', TA_CENTER):
                x += 0.5*_sW
            elif a in ('RIGHT', TA_RIGHT):
                x += _sW
            elif a not in ('LEFT', TA_LEFT):
                raise ValueError("Bad hAlign value " + str(a))
        canv.saveState()
        if self.img_data is not None:
            img = self.img_data
        else:
            img = self.cache[self.cacheindex]
        if isinstance(img, PdfDict):
            xscale = self.img_width / img.BBox[2]
            yscale = self.img_height / img.BBox[3]
            canv.translate(x, y)
            canv.scale(xscale, yscale)
            canv.doForm(makerl(canv, img))
        else:
            canv.drawImage(img, x, y, self.img_width, self.img_height)
        canv.restoreState()



class PdfImageCache(object):
    """
    Saves matplotlib figures to a temporary multi-page PDF file using the 'savefig'
    method. When closed the images are extracted and saved to the attribute 'cache'.
    The temporary PDF file is then deleted. The 'savefig' returns a PdfImage object
    with a pointer to the 'cache' list and an index for the figure. Use of this
    cache reduces duplicated resources in the reportlab generated PDF file.

    Use is similar to matplotlib's PdfPages object. When not used as a context
    manager, the 'close()' method must be explictly called before the reportlab
    document is built.
    """
    def __init__(self):
        self.pdftempfile = '_temporary_pdf_image_cache_.pdf'
        self.pdf = PdfPages(self.pdftempfile)
        self.cache = []
        self.count = 0

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self, *args):
        self.pdf.close()
        pages = PdfReader(self.pdftempfile).pages
        pages = [pagexobj(x) for x in pages]
        self.cache.extend(pages)
        os.remove(self.pdftempfile)

    def savefig(self, fig, width=200, height=200):
        self.pdf.savefig(fig)
        index = self.count
        self.count += 1
        return PdfImage(width=width, height=height, cache=self.cache, cacheindex=index)

styles = getSampleStyleSheet()
style = styles['Normal']

pixelcm=0.0352777777777778  # pixel/cm

#Height of A4 format: 297 mm = 29,7 cm
#Width of A4 format: 210 mm = 21,0 cm


doc = SimpleDocTemplate(resultfile,pagesize=A4, rightMargin=pixelcm*3, leftMargin=pixelcm*3, topMargin=pixelcm*2.5, bottomMargin=pixelcm*2.5)

story = []
  
   
"""
with PdfImageCache() as pdfcache:
    img = pdfcache.savefig(fig, width=fig_width, height=fig_height)
    print(dir(img))
    print(img.img_height,img.img_height)
    plt.close()
    story.append(img)
"""

img = PdfImage(fig, width=newwidth, height = newheigth)
plt.close()
story.append(img)
doc.build(story)


s = subprocess.Popen('FoxitPDFReader %s'%resultfile, shell=True)

print('tudo certo ate aqui')    

from StudyPsse import channel

ch = channel(name='potencia1', type='pot')
ch.channel_data()