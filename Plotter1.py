#!/usr/bin/env python
'''
Created on Jul 7, 2014

@author: roj-idl71
'''

from schainpy.controller import Project

  
dpath = '/home/pc-igp-173/Documentos/JRO-CosmicRays/processed_data/d2023156/'

 
if __name__ == '__main__':
     

        desc = "MLT experiment "
        startDate ='2023/06/05'
        endDate = '2023/06/05'
        startTime = '00:00:00'
        endTime = '23:00:00'
        dpath =dpath
        
        controllerObj = Project()
        controllerObj.setup(id='191', name='MLT meteors', description=desc)

        readUnitConfObj1 = controllerObj.addReadUnit(datatype='SpectraReader',
                                                    path=dpath,
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
        
        #op = spectra.addOperation(name='SpectraPlot')
        #op.addParameter(name='wintitle', value='Spectra', format='str')

        # op = spectra.addOperation(name='CoherencePlot')
        # op.addParameter(name='wintitle', value='Coherence', format='str')


        # op = spectra.addOperation(name='PhasePlot')
        # op.addParameter(name='wintitle', value='Phase', format='str')


        # op = spectra.addOperation(name='CrossSpectraPlot')
        # op.addParameter(name='wintitle', value='CrossSpectraPlot', format='str')


        op = spectra.addOperation(name='RTIPlot')
        op.addParameter(name='wintitle', value='RTI', format='str')
        op.addParameter(name='xmin',value=19.99)
        op.addParameter(name='xmax',value=20.05)
        
        controllerObj.start()
        
        
        
        #del controllerObj
