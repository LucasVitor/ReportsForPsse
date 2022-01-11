#Violations
import numpy
class Violation():
    
    def __init__(self,time, data):
         self.__time      = time
         self.__data      = data  
    
    def stead_state(self):
        dx = self.__time[1]- self.__time[0]
        print('dx',dx)
        y = self.__data
        dydx = numpy.gradient(y, dx)
        count=0
        for i in dydx:
            count +=1
            print(count, i)

    def showdata(self):
        count=0
        for i in self.__time :
            count += 1
            print count, i