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
 
 



  
dpath = '/home/pc-igp-173/Documentos/Cosmic Rays/data_test/'
path_out = '/home/pc-igp-173/Documentos/Cosmic Rays/out/'
 
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

        readUnitConfObj1 = controllerObj.addReadUnit(datatype='VoltageReader',
                                                    path=dpath,
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

        code = '[[1,1,1,1,1,-1,-1,1,1,-1,1,-1,1]]'

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
                
        controllerObj.start()
        
        
        
        #del controllerObj
