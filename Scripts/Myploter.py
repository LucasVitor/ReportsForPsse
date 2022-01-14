import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

class Ploter(object):
    
    def __init__(self):
        self.__y = [1,	4,	9,	16,	25,	36,	49,	64,	81,	100]
        self.__x = [1,	2,	3,	4,	5,	6,	7,	8,	9,	10]
        self.__nrows  = 3
        self.__ncols  = 2
        self.__height = 7.0#2
        self.__width  = 10.0#6
        self.__xlabel = 'x label'
        self.__ylabel = 'y label'
        self.__curvelabel = 'quadratic'
        self.__pagetitle = 'Overlapping Gridspecs'

    def get_data(self):
        pass

    def chart_object(self):
        fig = plt.figure(figsize=[self.__height, self.__width], constrained_layout=True) #, constrained_layout=True
        gs0 = gridspec.GridSpec(self.__nrows,self.__ncols, figure=fig)
        for row in range(self.__nrows):
            for col in range(self.__ncols):
                ax = fig.add_subplot(gs0[row,col])
                ax.plot( self.__x,self.__y,label = self.__curvelabel,linewidth=1.0,linestyle =  (0, (1, 1)))  #https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
                ax.set_xlabel(self.__xlabel, fontsize=8)  # Add an x-label to the axes.
                ax.set_ylabel(self.__ylabel,fontsize=8)  # Add a y-label to the axes.
                #ax.set_title("Simple Plot",fontsize=10)  # Add a title to the axes.
                ax.legend(fontsize=8)
        fig.suptitle(self.__pagetitle,fontsize=12)
        #plt.show()
        #fig.tight_layout()
        return fig  