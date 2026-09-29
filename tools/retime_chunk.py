import cv2, numpy as np, subprocess, sys
src, end_s, out_s, dst = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
A,B=int(sys.argv[5]),int(sys.argv[6])
fps=24; m=np.load(src+'.flow.npy'); n=int(end_s*fps)
sp=m[:n-1]; k=np.exp(-np.linspace(-2,2,25)**2); k/=k.sum()
sp=np.convolve(np.pad(sp,12,mode='edge'),k,'valid'); C=np.concatenate([[0],np.cumsum(sp)])
N=int(round(out_s*fps)); sidx=np.interp(np.linspace(0,C[-1],N),C,np.arange(len(C)))
cap=cv2.VideoCapture(src); W=int(cap.get(3)); H=int(cap.get(4))
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r','24','-i','-',
 '-c:v','libx264','-preset','medium','-crf','12','-pix_fmt','yuv420p',dst],stdin=subprocess.PIPE)
frames={}; flows={}
sidx_all=sidx; sidx=sidx_all[A:B]
start=max(int(np.floor(sidx[0]))-1,0); cap.set(cv2.CAP_PROP_POS_FRAMES,start); cur=start-1
def get(i):
    global cur
    while cur<i:
        ok,fr=cap.read(); cur+=1; frames[cur]=fr
        for kk in [k for k in frames if k<cur-2]: del frames[kk]
    return frames[i]
S=0.5; gx,gy=np.meshgrid(np.arange(W,dtype=np.float32),np.arange(H,dtype=np.float32))
def flow(i):
    if i not in flows:
        a=cv2.cvtColor(cv2.resize(get(i),None,fx=S,fy=S),cv2.COLOR_BGR2GRAY)
        b=cv2.cvtColor(cv2.resize(get(i+1),None,fx=S,fy=S),cv2.COLOR_BGR2GRAY)
        p=dict(pyr_scale=0.5,levels=4,winsize=21,iterations=3,poly_n=7,poly_sigma=1.5,flags=0)
        fw=cv2.resize(cv2.calcOpticalFlowFarneback(a,b,None,**p),(W,H))/S
        bw=cv2.resize(cv2.calcOpticalFlowFarneback(b,a,None,**p),(W,H))/S
        flows.clear(); flows[i]=(fw,bw)
    return flows[i]
for s in sidx:
    i0=int(np.floor(s)); a=np.float32(s-i0)
    if a<0.03 or i0>=n-1: out=get(min(i0,n-1))
    elif a>0.97: out=get(i0+1)
    else:
        fw,bw=flow(i0); f0=get(i0); f1=get(i0+1)
        # backward-warp: pixel at t=a samples f0 at x - a*fw and f1 at x - (1-a)*bw
        w0=cv2.remap(f0,gx-a*fw[...,0],gy-a*fw[...,1],cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
        w1=cv2.remap(f1,gx-(1-a)*bw[...,0],gy-(1-a)*bw[...,1],cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
        out=np.clip((1-a)*w0.astype(np.float32)+a*w1.astype(np.float32),0,255).astype(np.uint8)
    enc.stdin.write(out.tobytes())
enc.stdin.close(); enc.wait(); print('done',dst)
