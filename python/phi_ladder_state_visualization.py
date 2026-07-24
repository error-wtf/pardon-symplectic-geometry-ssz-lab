#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'python'))
from pardon_math.ssz_bridge import PHI
from pardon_math.ssz_state import phi_ladder, regime_label, state_vector
OUT=ROOT/'outputs'

def main():
    OUT.mkdir(exist_ok=True)
    ks=np.arange(-3,7)
    xs=phi_ladder(-3,6)
    st=state_vector(xs)
    fig,axs=plt.subplots(2,2,figsize=(12,8))
    labels=[regime_label(float(x)) for x in xs]
    ax=axs[0,0]
    ax.plot(ks, xs, marker='o', color='#1f78b4')
    ax.set_yscale('log'); ax.set_title('phi ladder x_k = phi^k'); ax.set_xlabel('k'); ax.set_ylabel('r/r_s')
    for k,x,l in zip(ks,xs,labels): ax.text(k,x,l,fontsize=7,rotation=25)
    axs[0,1].plot(xs, st['Xi'], marker='o', color='#6a3d9a', label='Xi')
    axs[0,1].plot(xs, st['D'], marker='s', color='#33a02c', label='D')
    axs[0,1].set_xscale('log'); axs[0,1].set_title('Xi and D on phi ladder'); axs[0,1].legend(); axs[0,1].grid(True,alpha=.25)
    axs[1,0].plot(xs, st['N_eff'], marker='o', color='#ff7f00'); axs[1,0].set_xscale('log'); axs[1,0].set_title("effective segment count N'=4s"); axs[1,0].grid(True,alpha=.25)
    axs[1,1].plot(xs, st['nu'], marker='o', color='#e31a1c'); axs[1,1].set_xscale('log'); axs[1,1].set_title('local phi-level nu=log(s)/log(phi)'); axs[1,1].grid(True,alpha=.25)
    marker=[a.axvline(xs[0],color='black',lw=2,alpha=.45) for a in [axs[0,1],axs[1,0],axs[1,1]]]
    text=axs[0,0].text(.02,.95,'',transform=axs[0,0].transAxes,va='top')
    def update(i):
        idx=i%len(xs)
        for m in marker: m.set_xdata([xs[idx],xs[idx]])
        text.set_text(f"k={ks[idx]}\nx={xs[idx]:.4f}\nregime={labels[idx]}\nphi={PHI:.6f}")
        return (*marker,text)
    update(0); fig.tight_layout(); fig.savefig(OUT/'phi_ladder_state.png',dpi=170)
    FuncAnimation(fig,update,frames=len(xs)*8,interval=220).save(OUT/'phi_ladder_state.gif',writer=PillowWriter(fps=6))
    plt.close(fig); print('wrote phi ladder state visualizations')
if __name__=='__main__': main()
