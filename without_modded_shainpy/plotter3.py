import datetime

from schainpy.model import *

path = '/home/pc-igp-173/Documentos/JRO-CosmicRays/processed_data/d2023156/'
startDate ='2023/06/05'
endDate = '2023/06/05'
startTime = '00:00:00'
endTime = '23:00:00'


rawdataObj = SpectraReader()
rawdataObj.name='SpectraReader'
spectraObj = SpectraProc()
#spectraPlot = SpectraPlot()

while not(rawdataObj.flagNoMoreFiles):
    rawdataObj.run(path = path,
                startDate=startDate,
                endDate=endDate,
                startTime=startTime,
                endTime=endTime,
                walk = 0)
    
    print(rawdataObj.dataOut.datatime)
    print(rawdataObj.dataOut.data)

#     print 'do something else with dataOut.data...'

print('task completed successfully')