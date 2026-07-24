#!/usr/bin/env python3
from pathlib import Path
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'python')); OUT=ROOT/'outputs'
from pardon_math.holonomy import dynamic_loop_deviation, triple_clock_product
from pardon_math.ssz_bridge import D_factor

def main():
    OUT.mkdir(exist_ok=True)
    radii=(1.2,2.5,8.0); prod=triple_clock_product(radii); t=np.linspace(0,2*np.pi,220); dyn=dynamic_loop_deviation(t)
    fig,(ax0,ax1)=plt.subplots(1,2,figsize=(11,5))
    pts=np.array([[0,1],[1.2,-.8],[-1.2,-.8],[0,1]])
    ax0.plot(pts[:,0],pts[:,1],lw=2,color='#1f78b4'); ax0.scatter(pts[:-1,0],pts[:-1,1],s=120,color='#e31a1c')
    for (x,y),r in zip(pts[:-1],radii): ax0.text(x,y+.16,f'r={r}\nD={D_factor(r):.3f}',ha='center')
    dot=ax0.scatter([],[],s=90,color='gold',edgecolor='black',zorder=5)
    ax0.set_aspect('equal'); ax0.axis('off'); ax0.set_title(f'static triple-clock product = {prod:.12f}')
    ax1.plot(t,dyn,color='#6a3d9a'); marker=ax1.scatter([],[],s=80,color='gold',edgecolor='black')
    ax1.axhline(1,color='black',ls='--',lw=1); ax1.set_title('toy dynamic loop deviation (not a claim)'); ax1.set_xlabel('phase'); ax1.set_ylabel('loop product')
    path=np.vstack([np.linspace(pts[i],pts[i+1],74) for i in range(3)])
    def update(frame):
        idx=frame%len(path); dot.set_offsets(path[idx]); j=frame%len(t); marker.set_offsets([[t[j],dyn[j]]]); return dot,marker
    fig.tight_layout(); fig.savefig(OUT/'holonomy_loop.png',dpi=170)
    FuncAnimation(fig,update,frames=220,interval=50).save(OUT/'holonomy_loop.gif',writer=PillowWriter(fps=20))
    plt.close(fig); print('wrote holonomy loop visualizations')
if __name__=='__main__': main()
