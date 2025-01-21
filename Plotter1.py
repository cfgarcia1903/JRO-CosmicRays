#!/usr/bin/env python
'''
Created on Jul 7, 2014

@author: roj-idl71
'''
import os
import sys
 

from schainpy.controller import Project

from os.path import join

 


path= ''

local=''
 
 
#minuto=2
 
 



  
dpath = '/home/pc-igp-173/Documentos/CosmicRays/out/out2'

 
if __name__ == '__main__':
     
     #Dia 9 6:15 a 6:50
     #Dia 8 7:00 a 7:50
    
     #Grupo ofical 
     #Dia 9 -> 6 am a 9:30 am
        
        desc = "MLT experiment "
        filename = "schain.xml"
        startDate ='2023/06/05'
        endDate = '2023/06/05'
        startTime = '00:00:00'
        endTime = '23:00:00'
        dpath =dpath
        figpath = "/media/arx/83fc24b6-cce4-46e4-a060-1525d0b03904/soporte/armando/files/saves"
        #procpath = "/mnt/sdb1/mlt/hdf5/main"
        remotefolrepositoryder = "/home/wmaster/graficos"
        db_range = ['25', '60']
        tiempo = ['7.0', '8.0']
 
        velocity = ['-80', '80']
        period = 60
 
        channels = '0,1,2'
        profiles = '(0, 2499)'
 

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
        
        op = spectra.addOperation(name='SpectraPlot')
        op.addParameter(name='wintitle', value='Spectra', format='str')

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
