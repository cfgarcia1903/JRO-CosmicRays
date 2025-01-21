import datetime

from schainpy.model import *

dpath = '/home/pc-igp-173/Documentos/CosmicRays/out/out2/'
startDate ='2023/06/05'
endDate = '2023/06/05'
startTime = '00:00:00'
endTime = '23:00:00'


pdataObj = SpectraReader()
#spectraObj = SpectraProc()
#spectraPlot = SpectraPlot()
pdataObj.name = 'SpectraReader'
pdataObj.setup(path=dpath,
                                                    startDate=startDate,
                                                    endDate=endDate,
                                                    #startTime=startTime,
                                                    #endTime=endTime,
                                                    online=0,
                                                    walk=0,
                                                    expLabel='',
                                                    delay=5)

#while(True):
#    pdataObj.getData()
#    print("read")
#   if pdataObj.flagNoMoreFiles:
#        break

#    print("a")
    
#    print(pdataObj.dataOut.datatime)
#    print(pdataObj.dataOut.data)

#     print 'do something else with dataOut.data...'

print('task completed successfully')