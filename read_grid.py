import cv2
import numpy as np
import pytesseract
import operator
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def readGrid():
    methode = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
    grid=[[0 for _ in range(9)] for _ in range(9)]
    marge=5
    case=50+2*marge
    taille_grille=9*case

    stopSearching=False #We have found a sudoku
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        #frame=cv2.imread("Sudoku00.png")
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray=cv2.GaussianBlur(gray,(5,5),0)
        thresh=cv2.adaptiveThreshold(gray,255,methode,cv2.THRESH_BINARY,9,2)
        cv2.imshow("Corrected image",thresh)

        contour_sudoku=None
        maxArea=0 #Find the biggest square on the image
        contours, hierarchy=cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            area=cv2.contourArea(c)
            if area>25000:# and area<(len(frame)-5)*len(frame[0]-5):
                peri=cv2.arcLength(c,True)
                polygone=cv2.approxPolyDP(c,0.01*peri,True)
                if area>maxArea and len(polygone)==4:
                    maxAre=area
                    contour_sudoku=polygone
        if not stopSearching:
            if contour_sudoku is not None:
                #cv2.drawContours(frame,[contour_sudoku],0,(0,255,0),2)
                ###Code found on github
                points=np.vstack(contour_sudoku).squeeze()
                points=sorted(points, key=operator.itemgetter(1))
                if points[0][0]<points[1][0]:
                    if points[3][0]<points[2][0]:
                        pts1=np.float32([points[0], points[1], points[3], points[2]])
                    else:
                        pts1=np.float32([points[0], points[1], points[2], points[3]])
                else:
                    if points[3][0]<points[2][0]:
                        pts1=np.float32([points[1], points[0], points[3], points[2]])
                    else:
                        pts1=np.float32([points[1], points[0], points[2], points[3]])
                pts2=np.float32([[0, 0], [taille_grille, 0], [0, taille_grille], [taille_grille, taille_grille]])
                M=cv2.getPerspectiveTransform(pts1, pts2)
                grille=cv2.warpPerspective(frame, M, (taille_grille, taille_grille))
        else:
            for x in range(9):
                for y in range(9):
                    img=grille[y*case+6:y*case+case-4,x*case+7:x*case+case-5]
                    img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    img=cv2.GaussianBlur(img,(5,5),0)
                    img=cv2.adaptiveThreshold(img,255,methode,cv2.THRESH_BINARY,11,3)
                    cv2.imshow("img", img)
                    ttt=pytesseract.image_to_string(img,config="--psm 7 digits")
                    print(ttt)

                    key=cv2.waitKey(1)&0xFF
                    try:
                        grid[y][x]=int(ttt)
                    except:
                        grid[y][x]=0
            break
        if contour_sudoku is not None or stopSearching:
            cv2.imshow("Grid",grille)

        cv2.imshow("frame", frame)

        key=cv2.waitKey(1)&0xFF
        if key==ord('q'):
            break
        if key==ord('k'):
            stopSearching=True
        
                
    cap.release()
    cv2.destroyAllWindows()
    print(np.array(grid))
    return grid


#grid=readGrid()
#print(np.array(grid))