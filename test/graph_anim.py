import sys
from pathlib import Path

current_dir = Path(__file__).parent.absolute()
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir)) 
current_dir = str(current_dir)

import numpy as np
from scipy.spatial import ConvexHull
from matplotlib import colors
import matplotlib.pyplot as plt
import networkx as nx
import src.libgt.data.Sheaf as Sheaf
from test.sheaf import Test
import math
from src.libgt.data.Graph import Graph, GraphO, GraphM

def run(show = 0):
    scalefactor = 1
    dpi=80
    T, gp = Test.sierpinsky_2d()
    set_inc = set()
    set_ins = set()
    collected_match = set()
    collected_match_inc = set()
    cyan = "#3fdcc4ff"
    red = "#c54e4a"
    green = "#36992dff"
    blue = "#24499dff"
    orange = "#ea8400"

    def compute_center_n(nodes):
        nb_nodes = len(nodes)
        sumx = 0
        sumy = 0
        for n in nodes:
            sumx += n[0]
            sumy += n[1]
        return sumx/nb_nodes, sumy/nb_nodes
        
    def compute_center(gp):
        nb_nodes = len(gp.OC.g.nodes())
        sumx = 0
        sumy = 0
        for n in gp.OC.g.nodes():
            sumx += gp.ET[n][0]
            sumy += gp.ET[n][1]
        return sumx/nb_nodes, sumy/nb_nodes
    
    def scale(points, n):
        cx, cy = compute_center_n(points)
        return [((x - cx)*n+cx, (y - cy)*n+cy) for (x, y) in points]
    
    def distance_2d(p1, p2):
        return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
    
    def rotate_around_center(center, p, angle):
        s = math.sin(angle)
        c = math.cos(angle)
        # print(p)
        px = p[0] - center[0]
        py = p[1] - center[1]
        pxp = px * c - py * s
        pyp = px * s + py * c
        px = pxp + center[0]
        py = pyp + center[1]
        return [px, py]

    def save_fig(suffix="", width=25, height=10):
        fig = plt.gcf()
        plt.box(False)
        ax = plt.gca()
        # fig.patch.set_visible(False) # make transparent image
        ax.axis('off')
        fig.set_size_inches(width, height)
        # plt.savefig(current_dir+"/output_png/"+str(gp.cpt_global)+".png", format="PNG", bbox_inches='tight', pad_inches = 0, dpi=dpi)
        plt.savefig(current_dir+"/output_svg/"+suffix+".svg", format="SVG", bbox_inches='tight', pad_inches = 0, dpi=dpi)

    def draw(gp, alpha, color = "black", shiftx=0, shifty=0, scale=1, figure=1):
        plt.figure(figure)
        g, pos = gp.OC, gp.ET
        ec = colors.to_rgba(color)
        ec = ec[:-1] + (alpha,)
        # print(len(g.nodes))
        # print(pos)
        pos = { n:(pos[n][0]*scale+shiftx, pos[n][1]*scale+shifty, pos[n][2]) for n in g.g.nodes}
        nx.draw_networkx_nodes(g.g, pos=pos, node_color = color, node_size = 100*scalefactor, alpha = alpha)
        ax = plt.gca()
        # circle = plt.Circle(compute_center(gp), 0.01, color='r', lw=0.2)
        # ax.add_patch(circle)
        for e in g.g.edges:
            pe0 = (pos[e[0]][0], pos[e[0]][1])
            pe1 = (pos[e[1]][0], pos[e[1]][1])
            ax.annotate("",
                xy=pe0, xycoords='data',
                xytext=pe1, textcoords='data',
                arrowprops=dict(arrowstyle="-|>", lw=2*scalefactor, mutation_scale=20*scalefactor, color=ec,
                                shrinkA=8*scalefactor, shrinkB=8*scalefactor,
                                patchA=None, patchB=None,
                                connectionstyle="arc3,rad=rrr".replace('rrr',str(0.3*e[2])),
                                ),
            )

    def draw_step(gp):
        def draw_step_(big_result):
            plt.figure(1)
            plt.gca().set_aspect('equal', 'datalim')
            # draw(gp, 0.2)
            draw(gp, 0, shiftx=1.5) #dummy
            draw(big_result, 1)
            if(show == 2):
                plt.show()
            save_fig(suffix="step/"+str(gp.cpt_step)+"step")
            plt.clf()

            draw_comma_init(gp)
            draw_comma_objects()
            draw_comma_arrows()

            plt.figure(2)
            plt.gca().set_aspect('equal', 'datalim')
            save_fig(suffix="comma/"+str(gp.cpt_step)+"_match", width=10, height=10)
            plt.clf()

            plt.figure(3)
            plt.gca().set_aspect('equal', 'datalim')
            save_fig(suffix="commarhs/"+str(gp.cpt_step)+"_matchapp", width=10, height=10)
            plt.clf()

            draw(gp, 0.2, figure=4)

            draw_input_parts()
            plt.figure(4)
            plt.gca().set_aspect('equal', 'datalim')
            save_fig(suffix="input/"+str(gp.cpt_step))
            plt.clf()

            for ins in collected_match:
                ins.drawn_before = True

            gp.cpt_step += 1
        return draw_step_
    
    def draw_merge(gp):
        def draw_merge_(lm, uins_rhs, uins_col):
            plt.figure(1)
            plt.gca().set_aspect('equal', 'datalim')
            #draw(gp, 0.2)
            draw(gp, 0, shiftx=1.5)
            uins_res = {}
            l_rhs = []
            l_col = []
            res_col = None
            res_rhs = None
            print(len(lm))
            for ins in lm:
                l_rhs.append(uins_rhs[ins])
                l_col.append(uins_col[ins])
                if res_rhs is None:
                    res_rhs = uins_rhs[ins].cod
                if res_col is None:
                    res_col = uins_col[ins].cod
            draw(res_col, 1, color="black")
            draw(res_rhs, 1, shiftx=1.5, color=blue)
            for m in l_col:
                draw(m.dom, 1, color=orange)
            for m in l_rhs:
                draw(m.dom, 1, shiftx=1.5, color=orange)
            if(show == 2):
                plt.show()
            save_fig(suffix="step/"+str(gp.cpt_step)+"merge")
            plt.clf()

            draw_comma_init(gp)
            draw_comma_objects()
            draw_comma_arrows()
            for ins in lm:
                draw_comma_object(ins, color=orange)

            plt.figure(2)
            plt.gca().set_aspect('equal', 'datalim')
            save_fig(suffix="comma/"+str(gp.cpt_step)+"_match", width=10, height=10)
            plt.clf()

            plt.figure(3)
            plt.gca().set_aspect('equal', 'datalim')
            save_fig(suffix="commarhs/"+str(gp.cpt_step)+"_matchapp", width=10, height=10)
            plt.clf()

            draw(gp, 0.2, figure=4)

            draw_input_parts()
            plt.figure(4)
            plt.gca().set_aspect('equal', 'datalim')
            save_fig(suffix="input/"+str(gp.cpt_step))
            plt.clf()

            for ins in collected_match:
                ins.drawn_before = True

            gp.cpt_step += 1
        return draw_merge_

    def draw_comma_init(gp):
        center = compute_center(gp)
        for n in list(gp.OC.nodes()):
            gn = GraphO()
            gnn = gn.add_node()
            p = {gnn: gp.ET[n]}
            gnp = T.pfunctor.CS.TO()(gn, p)
            draw(gnp, 0, shiftx=(gp.ET[n][0]-center[0])*2+center[0], shifty=(gp.ET[n][1]-center[1])*2+center[1], figure=2)
            draw(gnp, 0, shiftx=(gp.ET[n][0]-center[0])*2+center[0], shifty=(gp.ET[n][1]-center[1])*2+center[1], figure=3)
    
    def collect_comma_arrow(m, up):
        if (m.rule_inc.lhs.dom, m.rule_inc.lhs.cod) in set_inc: #hack to draw less arrows
            return
        elif m.rule_inc.lhs.cod in set_ins and up:
            return
        else:
            set_inc.add((m.rule_inc.lhs.dom, m.rule_inc.lhs.cod))
            set_ins.add(m.rule_inc.lhs.cod)
        collected_match_inc.add(m.rule_inc)
    
    def draw_comma_arrows():
        for ri in collected_match_inc:
            draw_comma_arrow(ri)
    
    def draw_comma_arrow(ri):
        plt.figure(2)
        centerdom = compute_center(ri.lhs.dom)
        centercod = compute_center(ri.rhs.cod)
        posdom = ((centerdom[0]-center[0])*3+center[0]+0.5, (centerdom[1]-center[1])*3+center[1]+0.29)
        poscod = ((centercod[0]-center[0])*3+center[0]+0.5, (centercod[1]-center[1])*3+center[1]+0.29)
        l = distance_2d(posdom, poscod)
        plt.annotate("", xy=poscod, xytext=posdom,
            arrowprops=dict(arrowstyle="->", lw=2*scalefactor, mutation_scale=20*scalefactor, color=[0.3,0.3,0.3],
                            shrinkA=35*l, shrinkB=90*l,
                            patchA=None, patchB=None,
                            ),
        )
        gp.cpt_match+=1
        plt.figure(3)
        plt.annotate("", xy=poscod, xytext=posdom,
            arrowprops=dict(arrowstyle="->", lw=2*scalefactor, mutation_scale=20*scalefactor, color=[0.3,0.3,0.3],
                            shrinkA=35*l, shrinkB=90*l,
                            patchA=None, patchB=None,
                            ),
        )
    
    def draw_input_parts():
        for r in collected_match:
            draw_input_part(r)
    
    def draw_input_part(r):
        g = r.rule.lhs
        plt.figure(4)
        draw(g, 1, color="black", figure=4)

    def collect_comma_object(gpp):
        collected_match.add(gpp)
        gpp.drawn_before = False

    def draw_comma_objects():
        for r in collected_match:
            if r.drawn_before:
                draw_comma_object(r, color="black")
            else:
                draw_comma_object(r, color=blue)
    
    def draw_comma_object(r, color="black"):
        g = r.rule.lhs
        centerp = compute_center(g)
        if len(g.OC.nodes()) == 1:
            plt.figure(2)
            #nodes = scale([(g.ET[n][0], g.ET[n][1]) for n in list(g.OC.nodes())], 1.2)
            nodes = list(g.OC.nodes())
            shiftx=(g.ET[nodes[0]][0]-center[0])*2+center[0]
            shifty=(g.ET[nodes[0]][1]-center[1])*2+center[1]
            circle1 = plt.Circle((g.ET[nodes[0]][0]+shiftx, g.ET[nodes[0]][1]+shifty), 0.13/gp.cpt_big_step, color='gray', lw=1.5, linestyle="dashed", fill=False)
            plt.gca().add_artist(circle1)
            plt.figure(3)
            circle1 = plt.Circle((g.ET[nodes[0]][0]+shiftx, g.ET[nodes[0]][1]+shifty), 0.13/gp.cpt_big_step, color='gray', lw=1.5, linestyle="dashed", fill=False)
            plt.gca().add_artist(circle1)
        elif len(g.OC.nodes()) == 2:
            nodes = list(g.OC.nodes())
            l = distance_2d(g.ET[nodes[0]], g.ET[nodes[1]])
            p1 = rotate_around_center(centerp, g.ET[nodes[0]],  math.pi/16)
            p2 = rotate_around_center(centerp, g.ET[nodes[0]], -math.pi/16)
            p3 = rotate_around_center(centerp, g.ET[nodes[1]],  math.pi/16)
            p4 = rotate_around_center(centerp, g.ET[nodes[1]], -math.pi/16)
            lp = [p1, p2, p3, p4]
            lps = scale(lp, 1.2)#*4/(5*math.sqrt(scalefactor)))# + 0.1/(l*l))
            lps.append(lps[0])
            xs, ys = zip(*lps)
            shiftx=(centerp[0]-center[0])*2+center[0]
            shifty=(centerp[1]-center[1])*2+center[1]
            xs = [ x + shiftx for x in xs ]
            ys = [ y + shifty for y in ys ]
            plt.figure(2)
            plt.plot(xs, ys, "--", color="gray")
            plt.figure(3)
            plt.plot(xs, ys, "--", color="gray")
        else:
            nodes = [[g.ET[n][0], g.ET[n][1]] for n in list(g.OC.nodes())]
            lps = scale(nodes, 1.3)#*4/(5*math.sqrt(scalefactor)))# + 0.1/(l*l))
            lps.append(lps[0])
            xs, ys = zip(*lps)
            shiftx=(centerp[0]-center[0])*2+center[0]
            shifty=(centerp[1]-center[1])*2+center[1]
            xs = [ x + shiftx for x in xs ]
            ys = [ y + shifty for y in ys ]
            plt.figure(2)
            plt.plot(xs, ys, "--", color="gray")
            plt.figure(3)
            plt.plot(xs, ys, "--", color="gray")

        plt.figure(2)
        draw(g, 1, color=color, shiftx=(centerp[0]-center[0])*2+center[0], shifty=(centerp[1]-center[1])*2+center[1], figure=2)

        g = r.rule.rhs
        centerp = compute_center(g)
        plt.figure(3)
        draw(g, 1, color=color, shiftx=(centerp[0]-center[0])*2+center[0], shifty=(centerp[1]-center[1])*2+center[1], figure=3)

    center = compute_center(gp)

    plt.figure(1)
    plt.gca().set_aspect('equal', 'datalim')
    draw(gp, 1)
    draw(gp, 0, shiftx=1.5) #dummy
    if(show >= 1):
        plt.show()
    save_fig(suffix="bigstep/"+str(0))
    plt.clf()
    gp.cpt_step = 0
    gp.cpt_match = 0

    for gp.cpt_big_step in range(1, 4):
        collected_match = set()
        collected_match_inc = set()
        T.draw_step = draw_step(gp)
        T.draw_merge = draw_merge(gp)
        T.collect_comma_arrow = collect_comma_arrow
        T.collect_comma_object = collect_comma_object
        gpp = T.extend(gp)
        gpp.cpt_step = gp.cpt_step
        gpp.cpt_match = gp.cpt_match
        gpp.cpt_big_step = gp.cpt_big_step
        gp = gpp

        plt.figure(1)
        plt.gca().set_aspect('equal', 'datalim')
        draw(gp, 1)
        draw(gp, 0, shiftx=1.5) #dummy
        if(show == 1):
            plt.show()
        # fig = plt.gcf()
        save_fig(suffix="bigstep/"+str(gp.cpt_big_step))
        plt.clf()

if __name__ == "__main__":
    show = 0
    if len(sys.argv) > 1:
        if sys.argv[1] == "--show":
            show = 1
        elif sys.argv[1] == "--showall":
            show = 2
        else:
            print("Unknown argument :", "'"+sys.argv[1]+"'", "... Try '--show' or '--showall")
    run(show)
