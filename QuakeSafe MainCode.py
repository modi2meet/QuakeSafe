#target for building area
import cv2 as cv
import numpy as np
import math as m

pts = list()
X=list()
Y=list()
storedPoint = 0
areaabs=0
vol=0
h=0
area_length = []
height_length = []
cx=0
cy=0
shape=0
mass=0
zoom_distance = int(input("Enter Zoom Value from the map: "))

def getlineLength(pt1,pt2):
    length = round(m.sqrt((pt2[0] - pt1[0])**2+(pt2[1]-pt1[1])**2))
    return length

def draw_circle(event,x,y,flags,param):
    if event==cv.EVENT_LBUTTONDBLCLK:
        pts.append([x,y])
        X.append(x)
        Y.append(y)
        print(x,y)
        cv.circle(img,(x+thr,y+thr),5,(255,0,0),-1)

def findlength(img2, pts, color):
    for x in range(len(pts)):
        if (x >= (len(pts) -1)):
            l = getlineLength(pts[x],pts[0])
        else:
            l = getlineLength(pts[x],pts[x+1])
        print(l)
        area_length.append(round(l))
        
    pts = np.array(pts,np.int32)
    pts = pts.reshape((-1,1,2))
    img2 = cv.polylines(img2, [pts], True, color, 2)
    cv.imshow("OUT",img2)
    storedPoint = len(pts)

img=cv.imread("./Untitled (2)")
h,w,d=img.shape
print("H=",h,"W=",w)# h=768, w=1366

thr=190
a,b,c,d=thr,thr,w-thr,h-thr
crop=img[b:d, a:c]

img2 = np.zeros((d,c,3),"uint8")

cv.namedWindow('Crop')
cv.setMouseCallback('Crop',draw_circle)

def shoelace(X, Y, n):
    area = 0.0
    j = n - 1
    for i in range(0,n):
        area += (X[j] + X[i]) * (Y[j] - Y[i])
        j = i       
    #vertices = len(X)
    #print(shoelace(X, Y, vertices))   
    return abs((area / 2.0)/24)#constant for zoom value 20 is 24
        

while True:
    cv.imshow("Crop",crop)
    key = cv.waitKey(27)& 0xFF
    if key ==ord('a'):
        findlength(img2, pts, (0,255,0))
        #put function for finding area
        print(pts)
        print(X)
        print(Y)
        areaabs = shoelace(X, Y, 4)
        print("absoulte area is", areaabs,"m^2")
        print("Using average area technique:")
        a=(area_length[0]*area_length[1])/23.7
        a2=(area_length[2]*area_length[3])/23.7#if zoom distance is 20, zoom constant is 23.7
        area=(a2+a)/2
        print(area)
        cv.putText(img2, 'Area of roof is '+str(round(areaabs))+'m^2',pts[3],5,1,(255,255,255),1 ,2)
        cv.imshow("OUT",img2)
        shape=len(pts)
        if shape==3:
          cv.putText(img2, 'Shape is triangle',(100,100),5,1,(255,255,255),1 ,2)
        elif shape==4:
          cv.putText(img2, 'Shape is quadrilateral',(100,100),5,1,(255,255,255),1 ,2)
        elif shape==5:
          cv.putText(img2, 'Shape is pentagon',(100,100),5,1,(255,255,255),1 ,2)
        elif shape==6:
          cv.putText(img2, 'Shape is hexagon',(100,100),5,1,(255,255,255),1 ,2)
        elif shape==7:
          cv.putText(img2, 'Shape is heptagon',(100,100),5,1,(255,255,255),1 ,2)
        elif shape==8:
          cv.putText(img2, 'Shape is octagon',(100,100),5,1,(255,255,255),1 ,2)
        pts=list()
    elif key ==ord('h'):
        findlength(img2, pts, (0,0,255))
        h=area_length[0]
        print("height is",area_length[0]*0.375,"m")
        cv.putText(img2, 'Height (using shadow) is '+str(round(area_length[0]*0.375))+'m',pts[1],5,1,(255,255,255),1 ,2)
        cv.imshow("OUT",img2)
        # put function to find height and volume
        #constant of 0.375 for zoom value 20
        vol=area_length[0]*0.375*areaabs
        print("volume is",round(vol),"m^3")
        mass= vol*2400 #2400 is the density of normal concrete in kg/m^3
        print("mass of structure is", round(mass),"kg")
        cv.putText(img2, 'Volume is '+str(round(vol))+'m^3',pts[0],5,1,(255,255,255),1 ,2)
        cv.imshow("OUT",img2)
        pts=list()
    elif key ==ord('q'):
        #find midpoint of quadrilateral using formula
        for i in range(len(X)):
            cx=cx+X[i];
            cy=cy+Y[i];
        cv.circle(img2,(round(cx/4)-380,round(cy/4)-100),h,(255,0,0) ,2)
        cv.imshow("OUT",img2)
        print("safe area of building is {}".format(h*h*0.375*0.375*3.14),"m^2")
        pts=list() 
        break
    

