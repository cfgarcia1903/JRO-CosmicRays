'''
Created on Jul 7, 2014

@author: roj-idl71
'''

from schainpy.controller import Project

 
path_in = '/home/pc-igp-173/Documentos/JRO-CosmicRays/with_modded_schainpy/raw_data'  ## RAW DATA DIRECTORY   (input)
path_out = '/home/pc-igp-173/Documentos/JRO-CosmicRays/with_modded_schainpy/pdata'  ##   P DATA DIRECTORY  (output)

 
if __name__ == '__main__':


    desc = "MLT experiment "
    filename = "schain.xml"
    startDate ='2023/06/05'
    endDate = '2023/06/05'
    startTime = '00:00:00'
    endTime = '23:00:00'
    channels = '0,1,2'
    code = '[[1,1,1,1,1,-1,-1,1,1,-1,1,-1,1]]'

    controllerObj = Project()
    controllerObj.setup(id='191', name='MLT meteors', description=desc)

    readUnitConfObj1 = controllerObj.addReadUnit(datatype='VoltageReader',
                                                path=path_in,
                                                startDate=startDate,
                                                endDate=endDate,
                                                startTime=startTime,
                                                endTime=endTime,
                                                online=0,
                                                walk=0,
                                                expLabel='',
                                                delay=5)

#---------------------------------------Voltage---------------------------------------
    voltage=controllerObj.addProcUnit(datatype='VoltageProc', inputId=readUnitConfObj1.getId())


    opObj11 = voltage.addOperation(name='selectChannels')
    opObj11.addParameter(name='channelList', value=channels, format='int')

    opObj11 = voltage.addOperation(name='Decoder', optype='other')
    opObj11.addParameter(name='code', value=code, format='floatlist')
    opObj11.addParameter(name='nCode', value='1', format='int')
    opObj11.addParameter(name='nBaud', value='13', format='int')

    nCohInt=2
    CohInt = voltage.addOperation(name='CohInt', optype='other')
    CohInt.addParameter(name='n', value=nCohInt, format='int')

#---------------------------------------Spectra---------------------------------------
    spectra = controllerObj.addProcUnit(datatype='Spectra', inputId=readUnitConfObj1.getId())
    spectra.addParameter(name='nFFTPoints', value='64')
    
    op = spectra.addOperation(name='removeDC')
    
#---------------------------------------Writer---------------------------------------
    opObj12 = spectra.addOperation(name='SpectraWriter', optype='other')
    opObj12.addParameter(name='path', value=path_out)
    opObj12.addParameter(name='blocksPerFile', value='120', format='int')
            

#---------------------------------------Start---------------------------------------
    controllerObj.start()
    
    
    
    #del controllerObj
