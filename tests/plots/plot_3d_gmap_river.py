import plotly.graph_objects as go
import networkx as nx
import numpy as np

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import tests_gmap

T, gp = tests_gmap.Test.rivers()

for i in range(0, 2):
    gp = tuple(T.extend(gp))[0].object
    if isinstance(gp, T.pfunctor.CD.TO()):
        gp = gp.force().obj

nodescorres = {}
nodes = []
xnodes = []
ynodes = []
znodes = []
for n in gp.OC.iter_icells(0):
    nodescorres[n] = len(nodes)
    nodes.append(n)
    xnodes.append(gp.ET[(0, n)][0])
    ynodes.append(gp.ET[(0, n)][1])
    znodes.append(gp.ET[(0, n)][2])

print(xnodes)
print(ynodes)
print(znodes)

xedgesb = []
yedgesb = []
zedgesb = []

xedgesn = []
yedgesn = []
zedgesn = []

nb_edges = 0

itri = []
jtri = []
ktri = []
for e in gp.OC.iter_icells(1):
    if gp.ET[(1,e)]:
        print("edge")
        print(e)
        ep0 = gp.OC.get_icell(0, e)
        xedgesb.append(gp.ET[(0, ep0)][0])
        yedgesb.append(gp.ET[(0, ep0)][1])
        zedgesb.append(gp.ET[(0, ep0)][2])
        print(ep0)
        print("x1, y1, z1", gp.ET[(0, ep0)])
        ep1 = gp.OC.get_icell(0, gp.OC.alpha(0, e))
        xedgesb.append(gp.ET[(0, ep1)][0])
        yedgesb.append(gp.ET[(0, ep1)][1])
        zedgesb.append(gp.ET[(0, ep1)][2])
        print(ep1)
        print("x2, y2, z2", gp.ET[(0, ep1)])
        xedgesb.append(None)
        yedgesb.append(None)
        zedgesb.append(None)
    else:
        print("edge")
        print(e)
        ep0 = gp.OC.get_icell(0, e)
        xedgesn.append(gp.ET[(0, ep0)][0])
        yedgesn.append(gp.ET[(0, ep0)][1])
        zedgesn.append(gp.ET[(0, ep0)][2])
        print(ep0)
        print("x1, y1, z1", gp.ET[(0, ep0)])
        ep1 = gp.OC.get_icell(0, gp.OC.alpha(0, e))
        xedgesn.append(gp.ET[(0, ep1)][0])
        yedgesn.append(gp.ET[(0, ep1)][1])
        zedgesn.append(gp.ET[(0, ep1)][2])
        print(ep1)
        print("x2, y2, z2", gp.ET[(0, ep1)])
        xedgesn.append(None)
        yedgesn.append(None)
        zedgesn.append(None)
    nb_edges += 1

colortri = []
for t in gp.OC.iter_icells(2):
    print(t)
    cont = True
    t0i = t
    nodes = [nodescorres[gp.OC.get_icell(0, t0i)]]
    cpt_color = 1 if gp.ET[(1, gp.OC.get_icell(1, t0i))] else 0
    while cont:
        t0ip = gp.OC.alpha(1, t0i)
        t0i = gp.OC.alpha(0, t0ip)
        if t == t0i:
            cont = False
        else:
            cpt_color += 1 if gp.ET[(1, gp.OC.get_icell(1, t0i))] else 0
            nodes.append(nodescorres[gp.OC.get_icell(0, t0i)])
    if len(nodes) == 3:
        print(nodes)
        if cpt_color >= 2:
            colortri.append(1)
        else:
            colortri.append(0)
        itri.append(nodes[0])
        jtri.append(nodes[1])
        ktri.append(nodes[2])

print("nodes : ", len(xnodes))
print("edges : ", nb_edges)
print("triangles : ", len(itri))
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

edge_traceb = go.Scatter3d(
    x=xedgesb, y=yedgesb, z=zedgesb,
    line= dict(width=10, color='#008'),
    hoverinfo='text',
    mode='lines',
    )

edge_tracen = go.Scatter3d(
    x=xedgesn, y=yedgesn, z=zedgesn,
    line= dict(width=10, color='#888'),
    hoverinfo='text',
    mode='lines',
    )

fig = go.Figure(data=[node_trace,
    go.Mesh3d(
        x=xnodes,
        y=ynodes,
        z=znodes,
        colorbar_title='z',
        colorscale=[[0, 'green'],
                    [1, 'blue']],
        # Intensity of each vertex, which will be interpolated and color-coded
        # intensity=[0, 0.33, 0.66, 1],
        intensity = colortri,#np.linspace(0, 1, len(itri), endpoint=True),
        intensitymode='cell',
        # i, j and k give the vertices of triangles
        # here we represent the 4 triangles of the tetrahedron surface
        i=itri,
        j=jtri,
        k=ktri,
        name='y',
        showscale=True
    ), edge_tracen, edge_traceb])

print(colortri, len(colortri))
fig.show()
