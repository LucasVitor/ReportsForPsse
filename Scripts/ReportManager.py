import pprint
import math

class ReportManager(object):
    
    def __init__(self, order,channelsdict):
        
        self.__chapterlist     = order
        self.__channelsdict    = channelsdict
        self.__chartsperpage   = 4
        self.__nrows           = None
        self.__ncols           = None 
        self.__reportindex     = {}
        self.__subchapterlist  = []
        self.__totalpage       = 0
    
    def get_chapter_list(self):
        self.__reportindex['CHAPTERS']= self.__chapterlist
        #pprint.pprint(dict(self.__reportindex),width=1)

#    def append_dictionary(self,,**kwargs):
#        self.__reportindex[kwargs['CHAPTERS']] +={kwargs['SUBCHAPTERS']
        
    def get_subchapter_list(self):
        heigthprop = 1 
        for chapter in self.__chapterlist:
            print chapter,':'
            for subchapter, values in self.__channelsdict[chapter].items():
                charts = len(values)
                fullpages  = math.trunc(charts//self.__chartsperpage)
                fractpages = charts/float(self.__chartsperpage) - fullpages
                if fractpages > 0:
                    heigthprop = fractpages
                    fractpages = 1    
                self.__nrows = 4
                self.__ncols = 1
                gridspec = [self.__nrows,self.__ncols]
                height = 7.2
                width = 10.6
                figuresizefull  = [ height , width]   
                figuresizefract = [height*heigthprop,width]
                self.__totalpage  +=fullpages + fractpages 
                print '     ',subchapter,charts,fullpages,figuresizefull,fractpages,figuresizefract
        print 'Total page:',self.__totalpage    
            