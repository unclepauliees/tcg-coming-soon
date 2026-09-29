import cv2, numpy as np, sys
f=sys.argv[1]; cap=cv2.VideoCapture(f); prev=None; mags=[]
while True:
    ok,fr=cap.read()
    if not ok: break
    g=cv2.cvtColor(cv2.resize(fr,(fr.shape[1]//6,fr.shape[0]//6)),cv2.COLOR_BGR2GRAY)
    if prev is not None:
        fl=cv2.calcOpticalFlowFarneback(prev,g,None,0.5,3,15,3,5,1.2,0)
        m=np.linalg.norm(fl,axis=2); mags.append(np.median(m[m>np.percentile(m,50)]))
    prev=g
m=np.array(mags); np.save(f+'.flow.npy',m)
print(f)
for s in range(0,len(m),48): print(f"{s/24:4.0f}-{(s+48)/24:.0f}s speed {m[s:s+48].mean():.3f}")
print('median',np.median(m),'spikes',[round(i/24,2) for i,v in enumerate(m) if v>5*np.median(m)])
