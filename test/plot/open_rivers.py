import sys
from pathlib import Path

current_dir = Path(__file__).parent.absolute()
root_dir = current_dir.parent.parent
sys.path.insert(0, str(root_dir)) 

import plotly.graph_objects as go
import networkx as nx
import numpy as np
from test.open import Test

T, gp = Test.rivers()

for i in range(0, 5):
    gp = T.extend(gp).LO[0]

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
triangles = []
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
        if t0i == 24:
            break
    if len(nodes) == 3:
        itri.append(nodes[0])
        jtri.append(nodes[1])
        ktri.append(nodes[2])
        triangles.append(t)

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

def iscolored(t, gp):
    de1 = t
    ce1 = gp.ET[(gp.OC.get_icell(1, de1), t)]
    de2 = gp.OC.alpha(1, gp.OC.alpha(0, de1))
    ce2 = gp.ET[(gp.OC.get_icell(1, de2), t)]
    de3 = gp.OC.alpha(1, gp.OC.alpha(0, de2))
    ce3 = gp.ET[(gp.OC.get_icell(1, de3), t)]
    return (ce1 != 0 and ce2 != 0) or (ce2 != 0 and ce3 != 0) or (ce3 != 0 and ce1 != 0)

edge_trace = go.Scatter3d(
    x=xedges, y=yedges, z=zedges,
    line= dict(width=1, color='#888'),
    hoverinfo='text',
    mode='lines')

fig = go.Figure(data=[node_trace,
    go.Mesh3d(
        x=xnodes,
        y=ynodes,
        z=znodes,
        colorbar_title='z',
        colorscale=[[0, 'green'], [1, 'blue']],
        intensity = [ 1 if iscolored(t, gp) else 0 for t in triangles ],
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
