import cv2
import numpy as np
import time

cap = cv2.VideoCapture(r'C:\video\short.mp4')
whT = 320

classesFile = 'coco.names'
classNames = []
with open(classesFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')
print(classNames)

modelConfiguration = 'yolov3.cfg'
modelWeights = 'yolov3.weights'

net = cv2.dnn.readNetFromDarknet(modelConfiguration,modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

confTresh = 0.25
nmsTresh = 0.45
#reduce if want less boxes

def findObjects(outputs,img):
    hT,wT,cT = img.shape
    bbox = []
    classIds = []
    confs = []

    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confTresh:
                w,h = int(det[2]*wT), int(det[3]*hT)
                x,y = int((det[0]*wT) - w/2), int((det[1]*hT)-h/2)
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confs.append(float(confidence))
    # print(len(bbox))
    #non-max supr
    indx = cv2.dnn.NMSBoxes(bbox,confs,confTresh,nmsTresh)




    for i in indx:
        i = i[0]
        box = bbox[i]
        x,y,w,h = box[0],box[1],box[2],box[3]
        cv2.rectangle(img,(x,y),(x+w,y+h),(242,136,208),1)
        #cv2.putText(img,f'{round(confs[i],2)}',(x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
        cv2.putText(img,f'{classNames[classIds[i]]},{round(confs[i],2)}',(x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,220,0), 2)



while True:
    start = time.time()
    success,img = cap.read()

    blob = cv2.dnn.blobFromImage(img,1/255,(whT,whT),[0,0,0],1,crop = False)
    net.setInput(blob)

    layerNames = net.getLayerNames()
    #print(layerNames)
    #print(net.getUnconnectedOutLayers())

    outputNames =[layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]
    #print(outputNames)

    outputs = net.forward(outputNames)
    #print(outputs[0].shape)
    #300 bound boxes prod

    findObjects(outputs,img)
    end = time.time()
    print(f'Time: {end - start}')
    cv2.imshow("Image",img)

    if cv2.waitKey(33) == 13:
        break


