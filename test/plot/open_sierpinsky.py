import sys
from pathlib import Path

current_dir = Path(__file__).parent.absolute()
root_dir = current_dir.parent.parent
sys.path.insert(0, str(root_dir)) 

import time
import random
import plotly.graph_objects as go
import networkx as nx
import src.libgt.data.Sheaf as Sheaf
from test.open import Test

def iterT(gp, T):
    gpLO = T.extend(gp).LO
    if len(gpLO) > 1:
        r = random.randrange(len(gpLO))
        gp = gpLO[r]
    else:
        gp = gpLO[0]
    return gp

T, gp = Test.sierpinsky()
gp = iterT(gp, T)
gp = iterT(gp, T)
gp = iterT(gp, T)
gp = iterT(gp, T)
gp = iterT(gp, T)
gp = iterT(gp, T)
gp = iterT(gp, T)
gp = iterT(gp, T)

edge_x = []

edge_x = []
edge_y = []
edge_z = []

for n0, n1 in gp.OC.g.edges():
    x0, y0, z0 = gp.ET[n0]
    x1, y1, z1 = gp.ET[n1]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)
    edge_z.append(z0)
    edge_z.append(z1)
    edge_z.append(None)

edge_trace = go.Scatter3d(
    x=edge_x, y=edge_y, z=edge_z,
    line= dict(width=2, color='#888'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
node_z = []
for node in gp.OC.g.nodes():
    x, y, z = gp.ET[node]
    node_x.append(x)
    node_y.append(y)
    node_z.append(z)
    
node_trace = go.Scatter3d(
    x=node_x, y=node_y, z=node_z,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale = 'Bluered',
        reversescale=True,
        color = [],
        size = 0.5,
        colorbar = dict(
            thickness = 15,
            title = 'connect',
            xanchor = 'left',
            titleside = 'right'
        ),
        line_width=2
    )
)

node_adjacencies = []
node_text = []
for node, adjacencies in enumerate(gp.OC.g.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    node_text.append('# of connections: '+str(len(adjacencies[1])))

node_trace.marker.color = node_adjacencies
node_trace.text = node_text

fig = go.FigureWidget(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Subdivised planar graph ' + str(len(gp.OC.g.nodes)) + " nodes and " + str(len(gp.OC.g.edges)) + " edges",
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

fig.show()
