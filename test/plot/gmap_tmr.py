import sys
from pathlib import Path

current_dir = Path(__file__).parent.absolute()
root_dir = current_dir.parent.parent
sys.path.insert(0, str(root_dir)) 

import plotly.graph_objects as go
import networkx as nx
import numpy as np
from test.gmap import Test

T, gp = Test.sheaf_nodes()

for i in range(0, 4):
    gp = T.extend(gp)

nodescorres = {}
nodes = []
xnodes = []
ynodes = []
znodes = []
for n in gp.OC.iter_icells(0):
    nodescorres[n] = len(nodes)
    nodes.append(n)
    xnodes.append(gp.ET[n][0])
    ynodes.append(gp.ET[n][1])
    znodes.append(gp.ET[n][2])

xedges = []
yedges = []
zedges = []

itri = []
jtri = []
ktri = []
for e in gp.OC.iter_icells(1):
    ep0 = gp.OC.get_icell(0, e)
    xedges.append(gp.ET[ep0][0])
    yedges.append(gp.ET[ep0][1])
    zedges.append(gp.ET[ep0][2])
    ep1 = gp.OC.get_icell(0, gp.OC.alpha(0, e))
    xedges.append(gp.ET[ep1][0])
    yedges.append(gp.ET[ep1][1])
    zedges.append(gp.ET[ep1][2])
    xedges.append(None)
    yedges.append(None)
    zedges.append(None)

for t in gp.OC.iter_icells(2):
    cont = True
    t0i = t
    nodes = [nodescorres[gp.OC.get_icell(0, t0i)]]
    while cont:
        t0ip = gp.OC.alpha(1, t0i)
        t0i = gp.OC.alpha(0, t0ip)
        if t == t0i:
            cont = False
        else:
            nodes.append(nodescorres[gp.OC.get_icell(0, t0i)])
    assert len(nodes) == 3
    itri.append(nodes[0])
    jtri.append(nodes[1])
    ktri.append(nodes[2])

node_trace = go.Scatter3d(
    x=xnodes, y=ynodes, z=znodes,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale = 'YlGnBu',
        reversescale=True,
        color = [],
        size = 3,
        colorbar = dict(
            thickness = 15,
            title = 'connect',
            xanchor = 'left',
            titleside = 'right'
        ),
        line_width=2
    )
)

edge_trace = go.Scatter3d(
    x=xedges, y=yedges, z=zedges,
    line= dict(width=10, color='#888'),
    hoverinfo='text',
    mode='lines')

fig = go.Figure(data=[node_trace,
    go.Mesh3d(
        x=xnodes,
        y=ynodes,
        z=znodes,
        colorbar_title='z',
        colorscale=[[0, 'gold'],
                    [0.5, 'mediumturquoise'],
                    [1, 'magenta']],
        intensity = np.linspace(0, 1, len(itri), endpoint=True),
        intensitymode='cell',
        # i, j and k give the vertices of triangles
        # here we represent the 4 triangles of the tetrahedron surface
        i=itri,
        j=jtri,
        k=ktri,
        name='y',
        showscale=True
    ), edge_trace])

fig.show()
