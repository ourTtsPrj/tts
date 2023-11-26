from fileinput import filename
from flask_restful import Api, Resource, abort
from flask import Flask
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import cv2,json



def arbortMsg() :
    abort(404,error="bad input")
def returnOk(par) :
    return {"code":200,"data":par}
    
def drawImageWithBox(fileName,resultList,cc,faceBox) :
    img = cv2.imread(f"iMgrAW/{fileName}")
    for result in resultList :
        faceBox[cc] = result['box']
        print(cc,result)
        x,y,w,h = result['box']
        cv2.rectangle(img, (x, y), (x+w, y+h), (240, 240, 14), 2)
        cv2.putText(img, str(cc), (x+10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (240, 240, 14), 2)
        cc += 1
        for key,value in result['keypoints'].items() :
            pass
            #cv2.circle(img,value,2,(240, 240, 14),-1)
    cv2.imwrite(f"iMgDeTECTfaCe/{fileName}",img)
    return [len(resultList),cc,faceBox]

class handel(Resource) :
    def get(self,method,query) :
        if method == "detect" :
            cc = 1
            allFace = 0
            fileInfo = {}
            for fileName in query.split(",") :
                if fileName :
                    faceBox = {}
                    #fileName = query
                    pixels = pyplot.imread(f"iMgrAW/{fileName}")
                    detector = MTCNN()
                    faces = detector.detect_faces(pixels)
                    rData = drawImageWithBox(fileName,faces,cc,faceBox)
                    fileInfo[fileName] = {"face":rData[0],"from":cc,"to":rData[1] - 1,"faceBox":{}}
                    cc = rData[1]
                    allFace += rData[0]
                    faceBox = rData[2]
                    fileInfo[fileName]["faceBox"] = faceBox
            return {"ok":True,"face":allFace,"info":fileInfo}


app = Flask(__name__)
api = Api(app)
api.add_resource(handel,"/<string:method>/<string:query>")
if __name__ == "__main__" :
    app.run(host="127.0.0.1",port=5000,debug=False)