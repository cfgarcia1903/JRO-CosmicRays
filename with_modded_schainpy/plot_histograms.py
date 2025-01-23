import pickle
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import datetime


path_in = '/home/pc-igp-173/Documentos/JRO-CosmicRays/with_modded_schainpy/takeout.pickle' ## PICKLE FILE   (input)

with open(path_in,'rb') as file:
    takeout=pickle.load(file)

print(takeout['info']['scale'])
if takeout['info']['scale'] == 'dB':
    xaxis_title = 'dB'
elif takeout['info']['scale'] == 'linear':
    xaxis_title = 'Arbitrary units (linear scale)'
else:
    raise Exception("Only \'dB\' or \'linear\' scale allowed")    

fig = make_subplots(rows=4, cols=1,
            subplot_titles=[f"Channel {i} | {datetime.datetime.fromtimestamp(takeout['data'][i]['start']).strftime('%Y-%m-%d %H:%M:%S')} ~ {datetime.datetime.fromtimestamp(takeout['data'][i]['end']).strftime('%Y-%m-%d %H:%M:%S')}" for i in range(4)],
            shared_xaxes=True,shared_yaxes=True)

for channel in range(4):
    bins, hist = takeout['data'][channel]['bins'], takeout['data'][channel]['hist']
    hist = np.log1p(hist)
    
    row = channel +1
    col = 1  
    
    fig.add_trace(
        go.Scatter(
            x=bins,
            y=hist,
            mode='lines',
            fill='tozeroy',
            name=f'Channel {channel}'
        ),
        row=row,
        col=col
    )
    fig.update_xaxes(title_text="Arbitrary units (linear scale)", row=row, col=col)
    fig.update_yaxes(title_text="Log(count+1)", row=row, col=col)

fig.update_layout(
    title=f"Power Logarithmic RTI-Histograms | Bin Size = {takeout['info']['binSize']} | Min Range = {takeout['info']['minRange']}",
    xaxis_title=xaxis_title,
    yaxis_title='Log(count+1)',
    template='plotly_white',
    width=1000,  
    height=800,
    showlegend=False
)

# Mostrar la figura
fig.show()