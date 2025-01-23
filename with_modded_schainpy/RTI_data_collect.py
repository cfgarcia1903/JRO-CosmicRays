'''
Created on Jul 7, 2014

@author: roj-idl71
'''

import pickle
from schainpy.controller import Project


path_in = '/home/pc-igp-173/Documentos/JRO-CosmicRays/with_modded_schainpy/pdata/d2023156'                 ##   P DATA DIRECTORY   (input)
path_out= '/home/pc-igp-173/Documentos/JRO-CosmicRays/with_modded_schainpy/takeout.pickle'  ##        PICKLE FILE  (output)

takeout ={'data':[{'bins':None,'hist':None,'start':None,'end':None},{'bins':None,'hist':None,'start':None,'end':None},{'bins':None,'hist':None,'start':None,'end':None},{'bins':None,'hist':None,'start':None,'end':None}],
          'info':{'minRange':7.5,'binSize':1,'scale': 'dB' }}


with open(path_out, 'wb') as file:             
    pickle.dump(takeout, file)

if __name__ == '__main__':
    

    desc = "MLT experiment "
    startDate ='2023/06/05'
    endDate = '2023/06/05'
    startTime = '00:00:00'
    endTime = '23:00:00'
    
    controllerObj = Project()
    controllerObj.setup(id='191', name='MLT meteors', description=desc)

    readUnitConfObj1 = controllerObj.addReadUnit(datatype='SpectraReader',
                                                path=path_in,
                                                startDate=startDate,
                                                endDate=endDate,
                                                startTime=startTime,
                                                endTime=endTime,
                                                online=0,
                                                walk=0,
                                                expLabel='',
                                                delay=5)


#---------------------------------------Spectra---------------------------------------
    
    spectra = controllerObj.addProcUnit(datatype='Spectra', inputId=readUnitConfObj1.getId())
    print(readUnitConfObj1.getId())
    
    op = spectra.addOperation(name='RTIPlot')
    op.addParameter(name='wintitle', value='RTI', format='str')
    op.addParameter(name='xmin',value=19.99)
    op.addParameter(name='xmax',value=20.5)
    op.addParameter(name='ymin',value=7.5)


    controllerObj.start()
    
    
    
    #del controllerObj
