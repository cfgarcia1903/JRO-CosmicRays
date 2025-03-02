# Copyright (c) 2012-2021 Jicamarca Radio Observatory
# All rights reserved.
#
# Distributed under the terms of the BSD 3-clause license.
"""Classes to plot Spectra data

"""

import os
import numpy
import pickle
import numpy as np


def symmetry_hist(data, center=0, bin_num=None, bin_size=None,density=False):
    
    #data = np.asarray(data)[~np.isnan(data)]
    l= np.min(data)
    h= np.max(data)
    if bin_size:
        hn= int(np.ceil((h-center-bin_size/2)/bin_size))
        h_edges=[center+bin_size*(0.5 + n) for n in range(hn+1)]
        ln= int(np.ceil((center-l -bin_size/2)/bin_size))
        l_edges=[center-bin_size*(0.5 + n) for n in range(ln+1)]
        edges=np.array(sorted(l_edges + h_edges))

        hist,_=np.histogram(data, bins=edges,density=density)
        
        return edges,hist
    

def merge_hists(bins1,hist1,bins2,hist2):
    max_edge1=np.max(bins1)
    max_edge2=np.max(bins2)
    min_edge1=np.min(bins1)
    min_edge2=np.min(bins2)
    
    if np.all(bins1==bins2) :
        new_hist=hist1+hist2
        return bins1,new_hist
    else:
        max_edge= np.max((max_edge1,max_edge2))
        min_edge= np.min((min_edge1,min_edge2))
        bin_size= bins1[1] - bins1[0]  ## asuming constant and equal size 
        
        new_bins= np.arange(min_edge,max_edge+0.1*bin_size,bin_size)
        new_hist= np.zeros(len(new_bins)-1)
      
        #lo_index1=np.where(new_bins==bins1[0])[0][0]
        #hi_index1=np.where(new_bins==bins1[-1])[0][0]
        lo_index1=np.searchsorted(new_bins, bins1[0])
        hi_index1=np.searchsorted(new_bins, bins1[-1])

        new_hist[lo_index1:hi_index1]+=hist1

        #lo_index2=np.where(new_bins==bins2[0])[0][0]
        #hi_index2=np.where(new_bins==bins2[-1])[0][0]
        lo_index2=np.searchsorted(new_bins, bins2[0])
        hi_index2=np.searchsorted(new_bins, bins2[-1])
        
        new_hist[lo_index2:hi_index2]+=hist2    

        return new_bins,new_hist
        
        
from schainpy.model.graphics.jroplot_base import Plot, plt, log


class SpectraPlot(Plot):
    '''
    Plot for Spectra data
    '''

    CODE = 'spc'
    colormap = 'jet'
    plot_type = 'pcolor'
    buffering = False

    def setup(self):
        self.nplots = len(self.data.channels)
        self.ncols = int(numpy.sqrt(self.nplots) + 0.9)
        self.nrows = int((1.0 * self.nplots / self.ncols) + 0.9)
        self.height = 2.6 * self.nrows
        self.cb_label = 'dB'
        if self.showprofile:
            self.width = 4 * self.ncols
        else:
            self.width = 3.5 * self.ncols
        self.plots_adjust.update({'wspace': 0.4, 'hspace':0.4, 'left': 0.1, 'right': 0.9, 'bottom': 0.08})
        self.ylabel = 'Range [km]'

    def update(self, dataOut):

        data = {}
        meta = {}
        spc = 10*numpy.log10(dataOut.data_spc/dataOut.normFactor)
        data['spc'] = spc
        data['rti'] = dataOut.getPower()
        data['noise'] = 10*numpy.log10(dataOut.getNoise()/dataOut.normFactor)
        extrapoints = spc.shape[1] % dataOut.nFFTPoints

        meta['xrange'] = (dataOut.getFreqRange(extrapoints)/1000., dataOut.getAcfRange(1), dataOut.getVelRange(extrapoints))
        
        if self.CODE == 'spc_moments':
            data['moments'] = dataOut.moments
            # data['spc'] = 10*numpy.log10(dataOut.data_pre[0]/dataOut.normFactor)
        if self.CODE == 'gaussian_fit':
            # data['moments'] = dataOut.moments
            data['gaussfit'] = dataOut.DGauFitParams
            # data['spc'] = 10*numpy.log10(dataOut.data_pre[0]/dataOut.normFactor)

        return data, meta 
    
    def plot(self):
        if self.xaxis == "frequency":
            x = self.data.xrange[0]
            self.xlabel = "Frequency (kHz)"
        elif self.xaxis == "time":
            x = self.data.xrange[1]
            self.xlabel = "Time (ms)"
        else:
            x = self.data.xrange[2]
            self.xlabel = "Velocity (m/s)"

        if (self.CODE == 'spc_moments') | (self.CODE == 'gaussian_fit'):
            x = self.data.xrange[2]
            self.xlabel = "Velocity (m/s)"

        self.titles = []

        y = self.data.yrange
        self.y = y

        data = self.data[-1]
        z = data['spc']

        for n, ax in enumerate(self.axes):
            noise = data['noise'][n]
            if self.CODE == 'spc_moments':
                mean = data['moments'][n, 1]
            if self.CODE == 'gaussian_fit': 
                # mean = data['moments'][n, 1]
                gau0 = data['gaussfit'][n][2,:,0]
                gau1 = data['gaussfit'][n][2,:,1]
            if ax.firsttime:
                self.xmax = self.xmax if self.xmax else numpy.nanmax(x)
                self.xmin = self.xmin if self.xmin else numpy.nanmin(x)#-self.xmax
                #self.xmin = self.xmin if self.xmin else -self.xmax
                #self.zmin = self.zmin if self.zmin else numpy.nanmin(z)
                #self.zmax = self.zmax if self.zmax else numpy.nanmax(z)
                if self.zlimits is not None:
                    self.zmin, self.zmax = self.zlimits[n]
                ax.plt = ax.pcolormesh(x, y, z[n].T,
                                       vmin=self.zmin,
                                       vmax=self.zmax,
                                       cmap=plt.get_cmap(self.colormap)
                                       )

                if self.showprofile:
                    ax.plt_profile = self.pf_axes[n].plot(
                        data['rti'][n], y)[0]
                    ax.plt_noise = self.pf_axes[n].plot(numpy.repeat(noise, len(y)), y,
                                                        color="k", linestyle="dashed", lw=1)[0]
                if self.CODE == 'spc_moments':
                    ax.plt_mean = ax.plot(mean, y, color='k', lw=1)[0]
                if self.CODE == 'gaussian_fit':
                    # ax.plt_mean = ax.plot(mean, y, color='k', lw=1)[0]
                    ax.plt_gau0 = ax.plot(gau0, y, color='r', lw=1)[0]
                    ax.plt_gau1 = ax.plot(gau1, y, color='y', lw=1)[0]
            else:
                ax.plt.set_array(z[n].T.ravel())
                if self.showprofile:
                    ax.plt_profile.set_data(data['rti'][n], y)
                    ax.plt_noise.set_data(numpy.repeat(noise, len(y)), y)
                if self.CODE == 'spc_moments':
                    ax.plt_mean.set_data(mean, y)
                if self.CODE == 'gaussian_fit':
                    # ax.plt_mean.set_data(mean, y)
                    ax.plt_gau0.set_data(gau0, y)
                    ax.plt_gau1.set_data(gau1, y)
            self.titles.append('CH {}: {:3.2f}dB'.format(n, noise))


class CrossSpectraPlot(Plot):

    CODE = 'cspc'
    colormap = 'jet'
    plot_type = 'pcolor'
    zmin_coh = None
    zmax_coh = None
    zmin_phase = None
    zmax_phase = None

    def setup(self):

        self.ncols = 4
        self.nplots = len(self.data.pairs) * 2
        self.nrows = int((1.0 * self.nplots / self.ncols) + 0.9)
        self.width = 3.1 * self.ncols
        self.height = 2.6 * self.nrows
        self.ylabel = 'Range [km]'
        self.showprofile = False
        self.plots_adjust.update({'left': 0.08, 'right': 0.92, 'wspace': 0.5, 'hspace':0.4, 'top':0.95, 'bottom': 0.08})

    def update(self, dataOut):

        data = {}
        meta = {}

        spc = dataOut.data_spc
        cspc = dataOut.data_cspc
        meta['xrange'] = (dataOut.getFreqRange(1)/1000., dataOut.getAcfRange(1), dataOut.getVelRange(1))
        meta['pairs'] = dataOut.pairsList

        tmp = []

        for n, pair in enumerate(meta['pairs']):
            out = cspc[n] / numpy.sqrt(spc[pair[0]] * spc[pair[1]])
            coh = numpy.abs(out)
            phase = numpy.arctan2(out.imag, out.real) * 180 / numpy.pi
            tmp.append(coh)
            tmp.append(phase)

        data['cspc'] = numpy.array(tmp)

        return data, meta 
    
    def plot(self):

        if self.xaxis == "frequency":
            x = self.data.xrange[0]
            self.xlabel = "Frequency (kHz)"
        elif self.xaxis == "time":
            x = self.data.xrange[1]
            self.xlabel = "Time (ms)"
        else:
            x = self.data.xrange[2]
            self.xlabel = "Velocity (m/s)"
        
        self.titles = []

        y = self.data.yrange
        self.y = y

        data = self.data[-1]
        cspc = data['cspc']

        for n in range(len(self.data.pairs)):
            pair = self.data.pairs[n]
            coh = cspc[n*2]
            phase = cspc[n*2+1]
            ax = self.axes[2 * n]
            if ax.firsttime:
                ax.plt = ax.pcolormesh(x, y, coh.T,
                                       vmin=0,
                                       vmax=1,
                                       cmap=plt.get_cmap(self.colormap_coh)
                                       )
            else:
                ax.plt.set_array(coh.T.ravel())
            self.titles.append(
                'Coherence Ch{} * Ch{}'.format(pair[0], pair[1]))
                                   
            ax = self.axes[2 * n + 1]
            if ax.firsttime:
                ax.plt = ax.pcolormesh(x, y, phase.T,
                                       vmin=-180,
                                       vmax=180,
                                       cmap=plt.get_cmap(self.colormap_phase) 
                                       )
            else:
                ax.plt.set_array(phase.T.ravel())
            self.titles.append('Phase CH{} * CH{}'.format(pair[0], pair[1]))


class RTIPlot(Plot):
    '''
    Plot for RTI data
    '''

    CODE = 'rti'
    colormap = 'jet'
    plot_type = 'pcolorbuffer'

    def setup(self):
        self.xaxis = 'time'
        self.ncols = 1
        self.nrows = len(self.data.channels)
        self.nplots = len(self.data.channels)
        self.ylabel = 'Range [km]'
        self.xlabel = 'Time'
        self.cb_label = 'dB'
        self.plots_adjust.update({'hspace':0.8, 'left': 0.1, 'bottom': 0.08, 'right':0.95})
        self.titles = ['{} Channel {}'.format(
            self.CODE.upper(), x) for x in range(self.nrows)]

    def update(self, dataOut):

        data = {}
        meta = {}
        data['rti'] = dataOut.getPower()
        data['noise'] = 10*numpy.log10(dataOut.getNoise()/dataOut.normFactor)

        return data, meta

    def plot(self):
        self.x = self.data.times
        self.y = self.data.yrange
        self.z = self.data[self.CODE]
        self.z = numpy.ma.masked_invalid(self.z)

        if self.decimation is None:
            x, y, z = self.fill_gaps(self.x, self.y, self.z)
        else:
            x, y, z = self.fill_gaps(*self.decimate())

        with open('/home/pc-igp-173/Documentos/JRO-CosmicRays/with_modded_schainpy/takeout.pickle','rb') as file: #mine
            takeout=pickle.load(file)  #mine
    
        minHei=takeout['info']['minRange']  #mine
        minHei_index=np.where(y>=minHei)[0][0]  #mine
        bin_size=takeout['info']['binSize']  #mine
        scale=takeout['info']['scale'] 
        
        
        
        #takeout[0]+=list(z[0].T.flatten())
        #takeout[1]+=list(z[1].T.flatten())
        #takeout[2]+=list(z[2].T.flatten())
        #takeout[3]+=list(z[3].T.flatten())
        #with open('/home/pc-igp-173/Documentos/CosmicRays/out/out3/takeout.pickle', 'wb') as file:             
        #    pickle.dump(takeout, file)
        #with open('/home/pc-igp-173/Documentos/CosmicRays/out/out3/takeout_copy.pickle', 'wb') as file:             
        #    pickle.dump(takeout, file)
        #with open('/home/pc-igp-173/Documentos/CosmicRays/out/out3/takeout.txt', 'a') as file:  
        #    file.write(str(list(z[0].T.flatten())) + "\n")
        
        
        
        for n, ax in enumerate(self.axes):
            self.zmin = self.zmin if self.zmin else numpy.min(self.z)
            self.zmax = self.zmax if self.zmax else numpy.max(self.z)
            data = self.data[-1]
            db=z[n].T[minHei_index:,:].flatten()#mine
            if scale=='dB':
                takeoutdata=db
            elif scale=='linear':
                takeoutdata=10**(db.astype(np.float32)/10)#mine
            else:
                raise Exception("Only \'dB\' or \'linear\' scale allowed")
            #if n==1:
            #    with open('/home/pc-igp-173/Documentos/CosmicRays/out/out3/takeout_temp.pickle', 'wb') as file:             
            #        pickle.dump((x,y,z[n]), file)
            if ax.firsttime:
                #print(self.data.max_time)
                if takeout['data'][n]['start']: #mine
                    pass #mine
                else:
                    takeout['data'][n]['start']= self.data.max_time #mine
                     
                ax.plt = ax.pcolormesh(x, y, z[n].T,
                                       vmin=self.zmin,
                                       vmax=self.zmax,
                                       cmap=plt.get_cmap(self.colormap)
                                       )
                                       
                #print(y)
                takeout['data'][n]['bins'],takeout['data'][n]['hist']= symmetry_hist(takeoutdata, center=0, bin_size=bin_size) #mine
                
                if self.showprofile:
                    ax.plot_profile = self.pf_axes[n].plot(
                        self.data['rti'][n][-1], self.y)[0]
                    ax.plot_noise = self.pf_axes[n].plot(numpy.repeat(self.data['noise'][n][-1], len(self.y)), self.y,
                                                         color="k", linestyle="dashed", lw=1)[0]
            else:
                #print(self.data.max_time)
                takeout['data'][n]['end']=self.data.max_time  #mine
                ax.collections.remove(ax.collections[0])
                ax.plt = ax.pcolormesh(x, y, z[n].T,
                                       vmin=self.zmin,
                                       vmax=self.zmax,
                                       cmap=plt.get_cmap(self.colormap)
                                       )
                                       
                bins2,hist2=symmetry_hist(takeoutdata, center=0, bin_size=bin_size)  #mine
                bins1,hist1=takeout['data'][n]['bins'],takeout['data'][n]['hist'] #mine
                takeout['data'][n]['bins'],takeout['data'][n]['hist']= merge_hists(bins1,hist1,bins2,hist2) #mine
                
                if self.showprofile:
                    ax.plot_profile.set_data(self.data['rti'][n][-1], self.y)
                    ax.plot_noise.set_data(numpy.repeat(
                        self.data['noise'][n][-1], len(self.y)), self.y)
        with open('/home/pc-igp-173/Documentos/JRO-CosmicRays/with_modded_schainpy/takeout.pickle', 'wb') as file:       #mine       
            pickle.dump(takeout, file)   #mine


class CoherencePlot(RTIPlot):
    '''
    Plot for Coherence data
    '''

    CODE = 'coh'

    def setup(self):
        self.xaxis = 'time'
        self.ncols = 1
        self.nrows = len(self.data.pairs)
        self.nplots = len(self.data.pairs)
        self.ylabel = 'Range [km]'
        self.xlabel = 'Time'
        self.plots_adjust.update({'hspace':0.6, 'left': 0.1, 'bottom': 0.1,'right':0.95})
        if self.CODE == 'coh':
            self.cb_label = ''
            self.titles = [
                'Coherence Map Ch{} * Ch{}'.format(x[0], x[1]) for x in self.data.pairs]
        else:
            self.cb_label = 'Degrees'
            self.titles = [
                'Phase Map Ch{} * Ch{}'.format(x[0], x[1]) for x in self.data.pairs]

    def update(self, dataOut):

        data = {}
        meta = {}
        data['coh'] = dataOut.getCoherence()
        meta['pairs'] = dataOut.pairsList

        return data, meta

class PhasePlot(CoherencePlot):
    '''
    Plot for Phase map data
    '''

    CODE = 'phase'
    colormap = 'seismic'

    def update(self, dataOut):

        data = {}
        meta = {}
        data['phase'] = dataOut.getCoherence(phase=True)
        meta['pairs'] = dataOut.pairsList

        return data, meta

class NoisePlot(Plot):
    '''
    Plot for noise 
    '''

    CODE = 'noise'
    plot_type = 'scatterbuffer'

    def setup(self):
        self.xaxis = 'time'
        self.ncols = 1
        self.nrows = 1
        self.nplots = 1
        self.ylabel = 'Intensity [dB]'
        self.xlabel = 'Time'
        self.titles = ['Noise']
        self.colorbar = False
        self.plots_adjust.update({'right': 0.85 })

    def update(self, dataOut):

        data = {}
        meta = {}
        data['noise'] = 10*numpy.log10(dataOut.getNoise()/dataOut.normFactor).reshape(dataOut.nChannels, 1)
        meta['yrange'] = numpy.array([])

        return data, meta

    def plot(self):

        x = self.data.times
        xmin = self.data.min_time
        xmax = xmin + self.xrange * 60 * 60
        Y = self.data['noise']

        if self.axes[0].firsttime:
            self.ymin = numpy.nanmin(Y) - 5
            self.ymax = numpy.nanmax(Y) + 5
            for ch in self.data.channels:
                y = Y[ch]
                self.axes[0].plot(x, y, lw=1, label='Ch{}'.format(ch))
            plt.legend(bbox_to_anchor=(1.18, 1.0))
        else:
            for ch in self.data.channels:
                y = Y[ch]
                self.axes[0].lines[ch].set_data(x, y)
                
                
class PowerHistPlot(Plot):

    CODE = 'pow_profile'
    plot_type = 'scatter'

    def setup(self):

        self.ncols = 1
        self.nrows = 1
        self.nplots = 1
        self.height = 4
        self.width = 3
        self.ylabel = 'Range [km]'
        self.xlabel = 'Intensity [dB]'
        self.titles = ['Power Profile']
        self.colorbar = False

    def update(self, dataOut):

        data = {}
        meta = {}
        data[self.CODE] = dataOut.getPower()

        return data, meta

    def plot(self):

        y = self.data.yrange
        self.y = y

        x = self.data[-1][self.CODE]
        
        if self.xmin is None: self.xmin = numpy.nanmin(x)*0.9
        if self.xmax is None: self.xmax = numpy.nanmax(x)*1.1
        
        if self.axes[0].firsttime:
            for ch in self.data.channels:
                self.axes[0].hist(x[ch], label='Ch{}'.format(ch))
            plt.legend()
        else:
            for ch in self.data.channels:
                self.axes[0].hist(x[ch], label='Ch{}'.format(ch))


        
class PowerProfilePlot(Plot):

    CODE = 'pow_profile'
    plot_type = 'scatter'

    def setup(self):

        self.ncols = 1
        self.nrows = 1
        self.nplots = 1
        self.height = 4
        self.width = 3
        self.ylabel = 'Range [km]'
        self.xlabel = 'Intensity [dB]'
        self.titles = ['Power Profile']
        self.colorbar = False

    def update(self, dataOut):

        data = {}
        meta = {}
        data[self.CODE] = dataOut.getPower()

        return data, meta

    def plot(self):

        y = self.data.yrange
        self.y = y

        x = self.data[-1][self.CODE]
        
        if self.xmin is None: self.xmin = numpy.nanmin(x)*0.9
        if self.xmax is None: self.xmax = numpy.nanmax(x)*1.1
        
        if self.axes[0].firsttime:
            for ch in self.data.channels:
                self.axes[0].plot(x[ch], y, lw=1, label='Ch{}'.format(ch))
            plt.legend()
        else:
            for ch in self.data.channels:
                self.axes[0].lines[ch].set_data(x[ch], y)


class SpectraCutPlot(Plot):

    CODE = 'spc_cut'
    plot_type = 'scatter'
    buffering = False

    def setup(self):

        self.nplots = len(self.data.channels)
        self.ncols = int(numpy.sqrt(self.nplots) + 0.9)
        self.nrows = int((1.0 * self.nplots / self.ncols) + 0.9)
        self.width = 3.4 * self.ncols + 1.5
        self.height = 3 * self.nrows
        self.ylabel = 'Power [dB]'
        self.colorbar = False
        self.plots_adjust.update({'left':0.1, 'hspace':0.3, 'right': 0.75, 'bottom':0.08})

    def update(self, dataOut):

        data = {}
        meta = {}
        spc = 10*numpy.log10(dataOut.data_pre[0]/dataOut.normFactor)
        data['spc'] = spc
        meta['xrange'] = (dataOut.getFreqRange(1)/1000., dataOut.getAcfRange(1), dataOut.getVelRange(1))
        if self.CODE == 'cut_gaussian_fit':
            data['gauss_fit0'] = 10*numpy.log10(dataOut.GaussFit0/dataOut.normFactor)
            data['gauss_fit1'] = 10*numpy.log10(dataOut.GaussFit1/dataOut.normFactor)
        return data, meta

    def plot(self):
        if self.xaxis == "frequency":
            x = self.data.xrange[0][1:]
            self.xlabel = "Frequency (kHz)"
        elif self.xaxis == "time":
            x = self.data.xrange[1]
            self.xlabel = "Time (ms)"
        else:
            x = self.data.xrange[2][:-1]
            self.xlabel = "Velocity (m/s)"
        
        if self.CODE == 'cut_gaussian_fit':
            x = self.data.xrange[2][:-1]
            self.xlabel = "Velocity (m/s)"

        self.titles = []

        y = self.data.yrange
        data = self.data[-1]
        z = data['spc']

        if self.height_index:
            index = numpy.array(self.height_index)
        else:
            index = numpy.arange(0, len(y), int((len(y))/9))

        for n, ax in enumerate(self.axes):
            if self.CODE == 'cut_gaussian_fit': 
                gau0 = data['gauss_fit0']
                gau1 = data['gauss_fit1']
            if ax.firsttime:
                self.xmax = self.xmax if self.xmax else numpy.nanmax(x)
                self.xmin = self.xmin if self.xmin else -self.xmax
                self.ymin = self.ymin if self.ymin else numpy.nanmin(z)
                self.ymax = self.ymax if self.ymax else numpy.nanmax(z)
                ax.plt = ax.plot(x, z[n, :, index].T, lw=0.25)
                if self.CODE == 'cut_gaussian_fit':
                    ax.plt_gau0 = ax.plot(x, gau0[n, :, index].T, lw=1, linestyle='-.')
                    for i, line in enumerate(ax.plt_gau0):
                        line.set_color(ax.plt[i].get_color())    
                    ax.plt_gau1 = ax.plot(x, gau1[n, :, index].T, lw=1, linestyle='--')
                    for i, line in enumerate(ax.plt_gau1):
                        line.set_color(ax.plt[i].get_color())  
                labels = ['Range = {:2.1f}km'.format(y[i]) for i in index]
                self.figures[0].legend(ax.plt, labels, loc='center right')
            else:
                for i, line in enumerate(ax.plt):
                    line.set_data(x, z[n, :, index[i]].T)
                for i, line in enumerate(ax.plt_gau0):
                    line.set_data(x, gau0[n, :, index[i]].T)
                    line.set_color(ax.plt[i].get_color())
                for i, line in enumerate(ax.plt_gau1):
                    line.set_data(x, gau1[n, :, index[i]].T)
                    line.set_color(ax.plt[i].get_color())
            self.titles.append('CH {}'.format(n))


class BeaconPhase(Plot):

    __isConfig = None
    __nsubplots = None

    PREFIX = 'beacon_phase'

    def __init__(self):
        Plot.__init__(self)
        self.timerange = 24*60*60
        self.isConfig = False
        self.__nsubplots = 1
        self.counter_imagwr = 0
        self.WIDTH = 800
        self.HEIGHT = 400
        self.WIDTHPROF = 120
        self.HEIGHTPROF = 0
        self.xdata = None
        self.ydata = None

        self.PLOT_CODE = BEACON_CODE

        self.FTP_WEI = None
        self.EXP_CODE = None
        self.SUB_EXP_CODE = None
        self.PLOT_POS = None

        self.filename_phase = None

        self.figfile = None

        self.xmin = None
        self.xmax = None

    def getSubplots(self):

        ncol = 1
        nrow = 1

        return nrow, ncol

    def setup(self, id, nplots, wintitle, showprofile=True, show=True):

        self.__showprofile = showprofile
        self.nplots = nplots

        ncolspan = 7
        colspan = 6
        self.__nsubplots = 2

        self.createFigure(id = id,
                          wintitle = wintitle,
                          widthplot = self.WIDTH+self.WIDTHPROF,
                          heightplot = self.HEIGHT+self.HEIGHTPROF,
                          show=show)

        nrow, ncol = self.getSubplots()

        self.addAxes(nrow, ncol*ncolspan, 0, 0, colspan, 1)

    def save_phase(self, filename_phase):
        f = open(filename_phase,'w+')
        f.write('\n\n')
        f.write('JICAMARCA RADIO OBSERVATORY - Beacon Phase \n')
        f.write('DD MM YYYY  HH MM SS   pair(2,0) pair(2,1) pair(2,3) pair(2,4)\n\n' )
        f.close()

    def save_data(self, filename_phase, data, data_datetime):
        f=open(filename_phase,'a')
        timetuple_data = data_datetime.timetuple()
        day = str(timetuple_data.tm_mday)
        month = str(timetuple_data.tm_mon)
        year = str(timetuple_data.tm_year)
        hour = str(timetuple_data.tm_hour)
        minute = str(timetuple_data.tm_min)
        second = str(timetuple_data.tm_sec)
        f.write(day+' '+month+' '+year+'  '+hour+' '+minute+' '+second+'   '+str(data[0])+'   '+str(data[1])+'   '+str(data[2])+'   '+str(data[3])+'\n')
        f.close()

    def plot(self):
        log.warning('TODO: Not yet implemented...')

    def run(self, dataOut, id, wintitle="", pairsList=None, showprofile='True',
            xmin=None, xmax=None, ymin=None, ymax=None, hmin=None, hmax=None,
            timerange=None,
            save=False, figpath='./', figfile=None, show=True, ftp=False, wr_period=1,
            server=None, folder=None, username=None, password=None,
            ftp_wei=0, exp_code=0, sub_exp_code=0, plot_pos=0):

        if dataOut.flagNoData:         
            return dataOut

        if not isTimeInHourRange(dataOut.datatime, xmin, xmax):
            return

        if pairsList == None:
            pairsIndexList = dataOut.pairsIndexList[:10]
        else:
            pairsIndexList = []
            for pair in pairsList:
                if pair not in dataOut.pairsList:
                    raise ValueError("Pair %s is not in dataOut.pairsList" %(pair))
                pairsIndexList.append(dataOut.pairsList.index(pair))

        if pairsIndexList == []:
            return

 #         if len(pairsIndexList) > 4:
 #             pairsIndexList = pairsIndexList[0:4]

        hmin_index = None
        hmax_index = None

        if hmin != None and hmax != None:
            indexes = numpy.arange(dataOut.nHeights)
            hmin_list = indexes[dataOut.heightList >= hmin]
            hmax_list = indexes[dataOut.heightList <= hmax]

            if hmin_list.any():
                hmin_index = hmin_list[0]

            if hmax_list.any():
                hmax_index = hmax_list[-1]+1

        x = dataOut.getTimeRange()

        thisDatetime = dataOut.datatime

        title = wintitle + " Signal Phase" # : %s" %(thisDatetime.strftime("%d-%b-%Y"))
        xlabel = "Local Time"
        ylabel = "Phase (degrees)"

        update_figfile = False

        nplots = len(pairsIndexList)
        #phase = numpy.zeros((len(pairsIndexList),len(dataOut.beacon_heiIndexList)))
        phase_beacon = numpy.zeros(len(pairsIndexList))
        for i in range(nplots):
            pair = dataOut.pairsList[pairsIndexList[i]]
            ccf = numpy.average(dataOut.data_cspc[pairsIndexList[i], :, hmin_index:hmax_index], axis=0)
            powa = numpy.average(dataOut.data_spc[pair[0], :, hmin_index:hmax_index], axis=0)
            powb = numpy.average(dataOut.data_spc[pair[1], :, hmin_index:hmax_index], axis=0)
            avgcoherenceComplex = ccf/numpy.sqrt(powa*powb)
            phase = numpy.arctan2(avgcoherenceComplex.imag, avgcoherenceComplex.real)*180/numpy.pi

            if dataOut.beacon_heiIndexList:
                phase_beacon[i] = numpy.average(phase[dataOut.beacon_heiIndexList])
            else:
                phase_beacon[i] = numpy.average(phase)

        if not self.isConfig:

            nplots = len(pairsIndexList)

            self.setup(id=id,
                       nplots=nplots,
                       wintitle=wintitle,
                       showprofile=showprofile,
                       show=show)

            if timerange != None:
                self.timerange = timerange

            self.xmin, self.xmax = self.getTimeLim(x, xmin, xmax, timerange)

            if ymin == None: ymin = 0
            if ymax == None: ymax = 360

            self.FTP_WEI = ftp_wei
            self.EXP_CODE = exp_code
            self.SUB_EXP_CODE = sub_exp_code
            self.PLOT_POS = plot_pos

            self.name = thisDatetime.strftime("%Y%m%d_%H%M%S")
            self.isConfig = True
            self.figfile = figfile
            self.xdata = numpy.array([])
            self.ydata = numpy.array([])

            update_figfile = True

            #open file beacon phase
            path = '%s%03d' %(self.PREFIX, self.id)
            beacon_file = os.path.join(path,'%s.txt'%self.name)
            self.filename_phase = os.path.join(figpath,beacon_file)
            #self.save_phase(self.filename_phase)


        #store data beacon phase
        #self.save_data(self.filename_phase, phase_beacon, thisDatetime)

        self.setWinTitle(title)


        title = "Phase Plot %s" %(thisDatetime.strftime("%Y/%m/%d %H:%M:%S"))

        legendlabels = ["Pair (%d,%d)"%(pair[0], pair[1]) for pair in dataOut.pairsList]

        axes = self.axesList[0]

        self.xdata = numpy.hstack((self.xdata, x[0:1]))

        if len(self.ydata)==0:
            self.ydata = phase_beacon.reshape(-1,1)
        else:
            self.ydata = numpy.hstack((self.ydata, phase_beacon.reshape(-1,1)))


        axes.pmultilineyaxis(x=self.xdata, y=self.ydata,
                    xmin=self.xmin, xmax=self.xmax, ymin=ymin, ymax=ymax,
                    xlabel=xlabel, ylabel=ylabel, title=title, legendlabels=legendlabels, marker='x', markersize=8, linestyle="solid",
                    XAxisAsTime=True, grid='both'
                    )

        self.draw()

        if dataOut.ltctime >= self.xmax:
            self.counter_imagwr = wr_period
            self.isConfig = False
            update_figfile = True

        self.save(figpath=figpath,
                  figfile=figfile,
                  save=save,
                  ftp=ftp,
                  wr_period=wr_period,
                  thisDatetime=thisDatetime,
                  update_figfile=update_figfile)

        return dataOut
