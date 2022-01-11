# see slice, strip and split

import os, re
class Channel(object):
    """ Class Channel 
             ________________________________________________________________________________
            |                                                                                |
            |  ATENTION : This Class works only with 'Channels identifiers' as specified  in |
            |    'Program Operation Manual (PSSE 34.2)':'Table 15-2. Activity CHAN Summary'. | 
            |                                                                                | 
            |               ONLY WITH DEFAULT CHANNELS IDENTIFIERS!                          |    
            |________________________________________________________________________________|    
            
            This class takes the channels identifiers and breaks them into Instance Attributes that can be used to link
                the channel data to the .sav file.
            
            The Instance Attribues are:     

            Instance Attributes: to pass to instance the class: 
            
                - Channel identifier (chanidentifier): a string following the Table 15-2. 
            
            Instance Attributes calculates in the class:
            
                - Type of data - magnitude:'ANGL',   'POWR', 'VARS', 'ETRM', 'EFD',  'PMEC', 
                                           'SPD',    'IFD',  'ECMP', 'AUX',  'VREF', 'VUEL',
                                           'VOEL',   'ITRM', 'APPR', 'GREF', 'LCRF', 'WVEL',
                                           'WTSP',   'WPCH', 'WAET', 'WRTV', 'WRTI', 'WPCM',
                                           'WQCM',	 'WAUX', 'APPX',  'FREQ', 'VOLT', 'ANGL',
                                           'VAR' ,   'STATE','PLOD','QLOD',  'POWR', 'MVA',
                                           'APPR',   'APPX', 'VARS' . Type: string 
                
                - The element type (element): 'BUSLOAD','MACHINE','BRANCH',and 'BUS'.Type: string
                - Channel's name patter(pattertitle) :'XX''YY''NN''VV' 'ZZ'.Type string. See POM.pdf - Table 15-2  
                - Machine id (machineid): positive natural number as string
                - Bus number (busnumber): positive natural number as string
                - Bus name (busname): bus name + space + base kV. Type string
                - Load id (loadid): positive natural number as string
                - Bus from (busfrom):positive natural number as string
                - Bus to (busto): positive natural number as string
                - Circuit identifier (ckt): positive natural number as string
                - State or Var number (sttvarnumber): positive natural number fom the .sav file allocated as string 
            

            
            Class attributes:
                Defaut configuration of the channel's name (defautconfig). 
                    A dictionary with the patter id ['XX''YY''NN''VV' 'ZZ'] and respective magnitudes 
                    
           
            Notes of name patter from Table 15-2:    
                xx      Contains the bus number, the extended bus name, and the machine identifier.
                yy      Contains the bus number, and the extended bus name.
                zz      Contains the from bus number, to bus number or, for a three-winding transformer, 
                         the string 3W: followed by the transformer name, and the circuit identifier.
                nn      Is the VAR or STATE index.
                vv      Contains the bus number, load identifier, and the extended bus name.
           
    """

    defautconfig = {'XX':['ANGL','POWR','VARS','ETRM','EFD','PMEC',\
                        'SPD','IFD','ECMP','AUX','VREF','VUEL',\
                        'VOEL','ITRM','APPR','GREF','LCRF','WVEL',\
                        'WTSP','WPCH','WAET','WRTV','WRTI','WPCM',\
                        'WQCM',	'WAUX','APPX'],
                    'YY':['FREQ','VOLT','ANGL'],
                    'NN':['VAR' ,'STATE'],
                    'VV':['PLOD','QLOD'],
                    'ZZ':['POWR','MVA','APPR','APPX','VARS']}
    init_channel_id = 0
    characterize_id = 0
    
    
    def __init__(self):
        """def __init__(self,chanidentifier,debug = False ):
        """
        self.__magnitude      = None
        self.__element        = None
        self.__patterntitle   = None
        self.__machineid      = None
        self.__busnumber      = None
        self.__busname        = None
        self.__loadid         = None 
        self.__busfrom        = None
        self.__busto          = None     
        self.__ckt            = None 
        self.__sttvarnumber   = None    
        self.__chanidentifier = None
        self.__chanid         = None
        self.__debug          = False
        self.__dict4print = {'MACHINE':{'ANGL':[],'POWR':[],'VARS':[],'ETRM':[],'EFD':[],'PMEC':[],'SPD':[],'IFD':[],
                            'ECMP':[],'AUX':[],'VREF':[],'VUEL':[],'VOEL':[],'ITRM':[],'APPR':[],'GREF':[],
                            'LCRF':[],'WVEL':[],'WTSP':[],'WPCH':[],'WAET':[],'WRTV':[],'WRTI':[],'WPCM':[],
                            'WQCM':[],'WAUX':[],'APPX':[]},
                            'BUSLOAD' :{'PLOD':[],'QLOD': []},
                            'STATEVAR':{'VAR':[],'STATE':[]},
                            'BUS'     :{'FREQ':[],'VOLT':[],'ANGL':[]},
                            'BRANCH'  :{'POWR':[],'MVA':[],'APPR':[],'APPX':[],'VARS':[]}} 


    def init_channel(self,chanidentifier,chanidnumber,debug = False ):
        if chanidentifier == 'Time(s)':
            raise ValueError ("'Time(s)' is not a valid channel")
            return
        else:
            try:
                self.__chanid = int(chanidnumber)
                self.__chanidentifier = chanidentifier
                self.__debug          = debug
            except:
                raise ValueError('chanidnumber is not an integer!')
                return    
            
            Channel.init_channel_id += 1
        
    def __check_magnitude(self,**kwargs):
        """ def __check_magnitude():
            This method verify if the magnitude found is consisten to the default patter, returning a string
            with 4 characters as specified in defautconfig. 
        """
        x =[j  for j in Channel.defautconfig[kwargs['iddict']] if j == kwargs['magnitude']]
        return x[0]

    def __get_bus_number(self,strg):
        return re.search("\s(.*?)\[", strg).group(1).replace('[',"").strip() 

    def __get_bus_name(self,strg):
        return re.search("\[(.*?)\]", strg).group(1)

    def __get_channel_ids(self):  
        strg = self.__chanidentifier
        magn = str(re.split("\s", strg)[0]).strip()
        if ' TO ' in strg:
            aux =re.split("\s", strg)
            self.__element ='BRANCH'
            self.__patterntitle ='ZZ'
            self.__magnitude = Channel.__check_magnitude(self, iddict ='ZZ', magnitude = magn)
            self.__busfrom = str(aux[1]).strip() 
            self.__busto   = str(aux[3]).strip() 
            self.__ckt     = re.search("\'(.*?)\'", strg).group(1).strip() 
        else:
            try: id = re.findall(r"]\d*.", strg)[0].replace(']',"").replace('[',"").strip()
            except: id =''
            if id == '':
                aux = re.split("\s", strg)
                if magn in Channel.defautconfig['YY']:
                    self.__element = 'BUS'
                    self.__patterntitle ='YY'
                    self.__magnitude = Channel.__check_magnitude(self, iddict ='YY', magnitude = magn)
                    self.__busnumber = str(aux[1]).strip() 
                    self.__busname   = re.search("\[(.*?)\]", strg).group(1)    
                elif magn in Channel.defautconfig['NN']: 
                    self.__element = 'STATEVAR'
                    self.__patterntitle ='NN'
                    self.__magnitude = Channel.__check_magnitude(self, iddict ='NN', magnitude = magn)
                    self.__sttvarnumber = str(aux[1]).strip()   
            else:
                if magn in self.defautconfig['VV']:
                    self.__element = 'BUSLOAD'
                    self.__patterntitle ='VV'
                    self.__magnitude = Channel.__check_magnitude(self, iddict ='VV', magnitude = magn)
                    self.__loadid = id
                    self.__busnumber = Channel.__get_bus_number(self,strg) 
                    self.__busname   = Channel.__get_bus_name(self,strg)                   
                elif magn in self.defautconfig['XX']:
                    self.__element = 'MACHINE'
                    self.__patterntitle ='XX'
                    self.__magnitude = Channel.__check_magnitude(self, iddict ='XX', magnitude = magn)                 
                    self.__machineid = id
                    self.__busnumber = Channel.__get_bus_number(self,strg)
                    self.__busname   = Channel.__get_bus_name(self,strg)

    def __dict4print(self):
        self.__dict4print[self.__element][self.__magnitude].append(self.__chanid)

    def characterize(self):
        """def characterize(self)
            This method is the connection between other programns and the class. 
             It must be THE FIRST METHOD TO BE CALLED because it is reposponsable to instance
             all channel's variables and to verify if the result is consist. 
        """
        if Channel.characterize_id == (Channel.init_channel_id -1):  
            error1 = "\n\n      Channel Identifier (chanidentifier) does not match any default pattern!\n\
                      \n      The string in the  argument 'chanidentifier' must follow the patter especified in 'Program Operation Manual (PSSE 34.2)':'Table 15-2. Activity CHAN Summary'."
            try: self.__get_channel_ids()
            except: raise ValueError(error1)
            
            if self.__busnumber == None and self.__busfrom == None:     
                if self.__sttvarnumber == None: raise ValueError(error1)
           
            if self.__debug:
               print '\n' 
               print ' Channel name              :',self.__chanidentifier,'\n' 
               print '         Magnitude         =', self.__magnitude      
               print '         Element           =',self.__element        
               print '         Pattern Title     =',self.__patterntitle    
               print '         Machine           =',self.__machineid      
               print '         Bus number        =',self.__busnumber
               print '         Bus name          =',self.__busname     
               print '         Load Id           =',self.__loadid         
               print '         Bus From          =',self.__busfrom
               print '         Bus to            =',self.__busto       
               print '         Circuit Id        =',self.__ckt
               print '         Status/Var number =',self.__sttvarnumber
               print '         Channel ID        =',self.__chanid    
            Channel.__dict4print(self)
            
            Channel.characterize_id += 1
        else:
            print "Error in Characterize. Channel 'Time(s)' not accepted in step %s "% Channel.init_channel_id
            return

    def get_dict4print(self):
        for key1, dict1 in self.__dict4print.items():
            for key2, value2 in dict1.items():
                if value2 == [] : dict1.pop(key2)

        for key1, dict1 in self.__dict4print.items():
            if dict1 == {}: self.__dict4print.pop(key1)
        
        return self.__dict4print