

from schainpy.model import *

dpath =  '/home/pc-igp-173/Documentos/JRO-CosmicRays/processed_data/d2023156/'
startDate ='2023/06/05'
endDate = '2023/06/05'
startTime = '00:00:00'
endTime = '23:00:00'


ReaderObj = SpectraReader()
ProcObj = SpectraProc()
#spectraPlot = SpectraPlot()
ReaderObj.name = 'SpectraReader'
ReaderObj.setup(path=dpath,
                    startDate=startDate,
                    endDate=endDate,
                    startTime=startTime,
                    endTime=endTime,
                    online=0,
                    walk=0,
                    expLabel='',
                    delay=5)

while(True):
    ReaderObj.getData()
    if ReaderObj.flagNoMoreFiles:
        break
    
#    print(ReaderObj.dataOut.datatime)
#    print(ReaderObj.dataOut.data)

#     print 'do something else with dataOut.data...'

print('task completed successfully')