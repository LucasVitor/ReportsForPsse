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
mydict = ch1.get_dict4print()    

pprint.pprint(dict(mydict),width=1)

order = ['MACHINE','BUS']
import ReportManager
rep = ReportManager.ReportManager(order,mydict)
rep.get_chapter_list()
rep.get_subchapter_list()


reptitle = 'savnw_faults_SB1_b152.out' 
import ReportConfiguration
report = ReportConfiguration.MakeReport(resultfile,reptitle )
report.setupreport()


s = subprocess.Popen('FoxitPDFReader %s'%resultfile, shell=True)

