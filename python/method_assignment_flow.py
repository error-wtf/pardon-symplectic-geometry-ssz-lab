#!/usr/bin/env python3
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'outputs'

def main():
    OUT.mkdir(exist_ok=True)
    items=[('Clock/redshift','Xi/D direct','#33a02c'),('Light path','PPN (1+gamma)','#1f78b4'),('Orbit/precession','PPN beta/gamma + Hamiltonian','#ff7f00'),('Geodesic integration','Lagrange/Hamilton + invariant drift tests','#6a3d9a')]
    fig,ax=plt.subplots(figsize=(11,5)); ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,5)
    boxes=[]
    ax.text(5,4.5,'SSZ Prime Directive: Observable -> Class -> Method -> Scope -> Then calculate',ha='center',fontsize=13,weight='bold')
    for i,(a,b,c) in enumerate(items):
        y=3.6-i*.85
        rect=plt.Rectangle((.5,y-.25),3.0,.5,color=c,alpha=.85); ax.add_patch(rect); boxes.append(rect)
        ax.text(2,y,a,ha='center',va='center',color='white',weight='bold')
        ax.annotate('',xy=(6.0,y),xytext=(3.6,y),arrowprops=dict(arrowstyle='->',lw=2))
        ax.text(7.8,y,b,ha='center',va='center',bbox=dict(boxstyle='round',fc='white',ec=c,lw=2))
    pulse=plt.Circle((.5,3.6),.12,color='red'); ax.add_patch(pulse)
    def update(frame):
        idx=frame%len(items); y=3.6-idx*.85; pulse.center=(.5+((frame%20)/20)*3.0,y); return (pulse,)
    fig.tight_layout(); fig.savefig(OUT/'method_assignment_flow.png',dpi=170)
    FuncAnimation(fig,update,frames=80,interval=80).save(OUT/'method_assignment_flow.gif',writer=PillowWriter(fps=12))
    plt.close(fig); print('wrote method assignment flow visualizations')
if __name__=='__main__': main()
