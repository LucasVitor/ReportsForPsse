# draft
import pprint
import os, sys,subprocess,collections 
import pssexplore34


clear = lambda: os. system('cls')                                   
clear()

cwd = os.getcwd() 

pythonCode = os.path.join(cwd, 'Scripts')

if os.path.isdir(pythonCode):
    if pythonCode not in sys.path:
        sys.path.insert(1, pythonCode)

if 'PYTHONCODE' not in os.environ:
    os.environ.update({'PYTHONCODE':pythonCode})

    

try:  os.system('taskkill/im FoxitPDFReader.exe /t /f')
except OSError:
    print('file not opened')


# Create a class to get file paths and check the system
outfile ='Outs\\savnw_faults_SB1_b152.out'
savfile ='Cases\\savnw.sav'
xlsxfile ='Outs\\exemplo.xlsx'
resultfile ='Outs\\resultpdf.pdf' 
outfile1 ='Outs\\savnw_faults_SB1_b152.out'

# Create a object study with all data from .out file
import dyntools

studyobj = dyntools.CHNF(outfile)
chanrange = studyobj.get_range()
short_title, chanid, chandata = studyobj.get_data()
#excelfile = studyobj.xlsout(xlsxfile)




from Channels import Channel
from Violations import Violation

#ch1 = Channel(chanid[109],chandata[109])
ch1 = Channel()
for i in chanid: 
    if i!= 'time': 
        ch1.init_channel(chanid[i],i)
        ch1.characterize()
mydict =ch1.get_dict4print()    

pprint.pprint(dict(mydict),width=1)

order = ['MACHINE','BUS']
import ReportManager
rep = ReportManager.ReportManager(order,mydict)
rep.get_chapter_list()
rep.get_subchapter_list()


quit()
# ------------------------------------------------
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, NextPageTemplate, PageBreak, PageTemplate, Flowable
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from matplotlib.backends.backend_pdf import PdfPages
from pdfrw import PdfReader, PdfDict
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.lib.pagesizes import A4
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

def on_first_page(canvas,doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',7)
    canvas.drawString(inch*7.5, 0.4 * inch, "Page %d" % doc.page)
    canvas.restoreState()

def on_remaining_pages(canvas,doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',7)
    canvas.drawString(inch*7.5, 0.4 * inch, "Page %d" % doc.page)
    canvas.restoreState()

# creation of the BaseDocTempalte. showBoundary=0 to hide the debug borders
marginsize=inch*0.5
doc = BaseDocTemplate(resultfile,pagesize = A4 , leftMargin=marginsize, rightMargin=marginsize, topMargin=marginsize, bottomMargin=marginsize,showBoundary=1)# ,showBoundary=1

# create the frames. Here you can adjust the margins
frame_first_page = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='first')
#frame_remaining_pages = Frame(doc.leftMargin + 1*inch, doc.bottomMargin + 1*inch, doc.width - 2*inch, doc.height - 2*inch, id='remaining')
frame_remaining_pages = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='remaining')
# add the PageTempaltes to the BaseDocTemplate. You can also modify those to adjust the margin if you need more control over the Frames.
doc.addPageTemplates([PageTemplate(id='first_page',frames=frame_first_page, onPage=on_first_page),
                      PageTemplate(id='remaining_pages',frames=frame_remaining_pages, onPage=on_remaining_pages),
                      ])

styles=getSampleStyleSheet()
# start the story...
Elements=[]

#Elements.append(Paragraph("Frame first page!",styles['Normal']))
#Elements.append(NextPageTemplate('remaining_pages'))  #This will load the next PageTemplate with the adjusted Frame. 
#Elements.append(PageBreak()) # This will force a page break so you are guarented to get the next PageTemplate/Frame

#Elements.append(Paragraph("Frame remaining pages!,  "*500,styles['Normal']))

#start the construction of the pdf
import matplotlib.pyplot as plt
order = ['MACHINE','BUS']

from Myploter import Ploter
plot = Ploter()


with PdfImageCache() as pdfcache:
    for i in range(3):
        img = pdfcache.savefig(plot.chart_object(), width=511, height=757)
        plt.close()
        Elements.append(img )
        Elements.append(NextPageTemplate('first_page')) 
        Elements.append(PageBreak())
doc.build(Elements)


s = subprocess.Popen('FoxitPDFReader %s'%resultfile, shell=True)