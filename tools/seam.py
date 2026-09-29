import cv2,numpy as np,sys
cap=cv2.VideoCapture(sys.argv[1]); fr=[]
while True:
    ok,f=cap.read()
    if not ok: break
    fr.append(cv2.cvtColor(cv2.resize(f,(f.shape[1]//6,f.shape[0]//6)),cv2.COLOR_BGR2GRAY).astype(np.float32))
d=[np.abs(fr[i+1]-fr[i]).mean() for i in range(len(fr)-1)]
seam=np.abs(fr[0]-fr[-1]).mean()
print(sys.argv[1],'typical frame step %.2f (p95 %.2f)  loop seam step %.2f'%(np.median(d),np.percentile(d,95),seam))
