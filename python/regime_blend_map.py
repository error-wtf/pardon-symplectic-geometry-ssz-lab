#!/usr/bin/env python3
from pathlib import Path
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'python')); OUT=ROOT/'outputs'
from pardon_math.ssz_bridge import D_factor, xi_canonical, xi_strong, xi_weak

def main():
    OUT.mkdir(exist_ok=True); x=np.linspace(.2,12,600)
    fig,ax=plt.subplots(figsize=(11,5)); ax.plot(x,xi_canonical(x),label='Xi operative',lw=3,color='#6a3d9a'); ax.plot(x,xi_weak(x),ls='--',label='weak formula',color='#1f78b4'); ax.plot(x,xi_strong(x),ls=':',label='saturation g2',color='#e31a1c')
    spans=[(.2,1.8,'g2'),(1.8,2.2,'C2 blend'),(2.2,3,'photon sphere context'),(3,10,'strong context/g1 formula'),(10,12,'weak')]
    colors=['#fb9a99','#fdbf6f','#cab2d6','#b2df8a','#a6cee3']
    for (a,b,l),c in zip(spans,colors): ax.axvspan(a,b,color=c,alpha=.22); ax.text((a+b)/2,.92,l,ha='center',fontsize=8,transform=ax.get_xaxis_transform())
    marker=ax.axvline(.2,color='black',lw=2); txt=ax.text(.02,.9,'',transform=ax.transAxes,va='top')
    ax.set_xlabel('x=r/r_s'); ax.set_ylabel('Xi'); ax.set_title('SSZ formula domains vs physical regimes'); ax.legend(); ax.grid(True,alpha=.25)
    def update(frame):
        val=x[frame%len(x)]; marker.set_xdata([val,val]); txt.set_text(f'x={val:.2f}\nXi={xi_canonical(val):.4f}\nD={D_factor(val):.4f}'); return marker,txt
    fig.tight_layout(); fig.savefig(OUT/'regime_blend_map.png',dpi=170)
    FuncAnimation(fig,update,frames=len(x),interval=25).save(OUT/'regime_blend_map.gif',writer=PillowWriter(fps=25))
    plt.close(fig); print('wrote regime blend map visualizations')
if __name__=='__main__': main()
