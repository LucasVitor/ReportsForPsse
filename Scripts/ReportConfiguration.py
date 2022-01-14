from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, NextPageTemplate, PageBreak, PageTemplate, Flowable, Spacer
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet
from matplotlib.backends.backend_pdf import PdfPages
from pdfrw import PdfReader, PdfDict
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.lib.pagesizes import A4
from io import BytesIO
import matplotlib.pyplot as plt
from Myploter import Ploter
import os
from reportlab.lib.utils import ImageReader

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

class MakeReport(object):

    def __init__(self,file,reptitle):
        self.__resultfile = file
        self.__reporttitle =reptitle

    def setupreport(self):
        def on_cover_page(canvas,doc):
            filename ='C:\\Users\\Lucas\\Google Drive\\23 - Job Seeking Engineer\\1 - Preparation Material\\16_Git_Projects\\1_Report_Psse\\AuxDev\\7.jpg'
            canvas.saveState()
            canvas.drawInlineImage(filename, 0.0, 0.0,8.26*inch,11.69*inch)
            #canvas.drawImage(backimage, 8.26*inch,11.69*inch) #, mask='auto'
            canvas.restoreState()

        def on_remaining_pages(canvas,doc):
            canvas.saveState()
            canvas.setFont('Times-Italic',7)
            canvas.drawString(inch*7.5, 0.35 * inch, "Page %d" % (doc.page-1))
            canvas.line(doc.leftMargin, doc.bottomMargin, doc.width + 0.5*inch, doc.bottomMargin)
            canvas.line(doc.leftMargin, doc.height+0.5*inch, doc.width + 0.5*inch, doc.height+0.5*inch)
            canvas.setFont('Times-Italic',9)
            canvas.drawString(doc.leftMargin, doc.height+0.5*inch + 5,"Stability Report: %s" %self.__reporttitle)
            canvas.restoreState()

        marginsize=inch*0.5
        doc = BaseDocTemplate(self.__resultfile,pagesize = A4 , leftMargin=marginsize, rightMargin=marginsize, topMargin=marginsize, bottomMargin=marginsize,showBoundary=0)# ,showBoundary=1
        
        frame_page = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='first',showBoundary=0)

        doc.addPageTemplates([PageTemplate(id ='cover_page',frames=frame_page,onPage = on_cover_page),
                              PageTemplate(id ='remaining_pages',frames=frame_page, onPage = on_remaining_pages)])

        styles=getSampleStyleSheet()

        Elements=[]
        
        plot = Ploter()
        
        repstyle  = ParagraphStyle('yourtitle',
                       fontName='Times-Italic',
                       fontSize=46,
                       parent=styles['Normal'],
                       leftIndent = 4.8*inch, 
                       textColor = colors.Color(0,0,0,1),
                       spaceAfter=24)
        
        titlestyle = ParagraphStyle('yourtitle',
                       fontName='Helvetica-Oblique',
                       fontSize=28,
                       parent=styles['Normal'],
                       leftIndent = 0.25*inch, 
                       textColor = colors.Color(256,256,256,1),  #(0,102,255,1)
                       alignment=0,
                       spaceAfter=12)

        chapterstyle = ParagraphStyle('yourtitle',
                       fontName='Times-Roman',
                       fontSize =14,
                       parent=styles['Normal'],
                       leftIndent = 0, 
                       spaceAfter=6)

        subchapstyle = ParagraphStyle('yourtitle',
                       fontName='Times-Roman',
                       fontSize=12,
                       parent=styles['Normal'],
                       leftIndent = 0.5*inch, 
                       spaceAfter=6)


        with PdfImageCache() as pdfcache:

            Elements.append(Spacer(7.2*inch,10.69*inch*0.2))
            Elements.append(Paragraph('Stability',repstyle))
            Elements.append(Paragraph('Report',repstyle))
            Elements.append(Spacer(7.2*inch,10.69*inch*0.63))
            Elements.append(Paragraph(self.__reporttitle,titlestyle))
            Elements.append(NextPageTemplate('remaining_pages')) 
            Elements.append(PageBreak())

            for i in range(3):
                if i == 0: 
                    Elements.append(Paragraph('Chapter',chapterstyle))    
                    Elements.append(Paragraph('Subchapter',subchapstyle)) 
                    img = pdfcache.savefig(plot.chart_object(), width=511*0.9, height=757*0.9)
                    plt.close()
                    Elements.append(img )
                    Elements.append(PageBreak())
                else:
                    img = pdfcache.savefig(plot.chart_object(),width=511*0.9, height=757*0.9)
                    plt.close()
                    Elements.append(Spacer(7.2*inch,inch*0.50))
                    Elements.append(img )
                    Elements.append(PageBreak())                
        doc.build(Elements)        
        
