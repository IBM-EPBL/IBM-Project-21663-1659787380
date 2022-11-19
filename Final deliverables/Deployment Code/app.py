import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask,render_template,request
from twilio.rest import Client
#import cv2
#from playsound import playsound
#from flask import Flask, render_template

app=Flask(__name__)

model=load_model("forestfire.h5")
  
@app.route('/')
def index():
    return render_template("index.html")
text=''
@app.route('/predict',methods=['GET','POST'])
def upload():
    if request.method=='POST':
        f=request.files['image']
        filepath=os.path.join('static/',f.filename)
        f.save(filepath)
        img=image.load_img(filepath,target_size=(128,128))
        x=image.img_to_array(img)
        x = np.expand_dims(x,axis=0)
        pred = model.predict(x)
        y = int(pred[0][0])
        if(pred==1):
            account_sid = "ACb8327485cef89b8ed3adbe5cb710752f"
            auth_token = "d5489734f7ae8d28e412447a3881661e"

            client = Client(account_sid, auth_token)
            message = client.messages.create(
            body="Forest Fire detected , Stay safe!!!",
            from_=("+18087364790"),
            to=("+917358598519")
            )
            print(message.sid)
          
            text='FIRE DETECTED!!! SMS SENT!!'
            #playsound('alarm.mp3')
        else:
            text='NO FIRE'
    return text

if __name__=='__main__':
    app.run(debug=True)
