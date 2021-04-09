import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)

import plotly.graph_objects as go
import networkx as nx
import src.libgt.data.Sheaf as Sheaf
from test.sheaf import Test

T, gp = Test.triangle_mesh_refinement()
gp = T.extend(gp)
gp = T.extend(gp)
gp = T.extend(gp)
gp = T.extend(gp)

print()

edge_x = []
edge_y = []
edge_z = []

for n0, n1 in gp.OC.g.edges():
    x0, y0, z0 = gp.ET[n0]#G.nodes[edge[0]]['pos']
    x1, y1, z1 = gp.ET[n1]#G.nodes[edge[1]]['pos']
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
    line= dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
node_z = []
for node in gp.OC.g.nodes():
    x, y, z = gp.ET[node]#G.nodes[node]['pos']
    node_x.append(x)
    node_y.append(y)
    node_z.append(z)
    
node_trace = go.Scatter3d(
    x=node_x, y=node_y, z=node_z,
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
                #annotations=[ dict(
                #    text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                #    showarrow=False,
                #    xref="paper", yref="paper",
                #    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

fig.show()
