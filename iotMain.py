from tkinter import *
from tkinter import ttk
import cv2 
import numpy as np
import face_recognition
import os
from PIL import Image
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import pandas as pd
import json,requests,math
from datetime import datetime
from PIL import Image, ImageTk
import requests
from datetime import datetime

root = Tk()
root.title('Device Security Panel')
root.geometry("520x500")
#root.iconbitmap('lock.ico')
root.configure(bg='#FF8C00')
my_notebook = ttk.Notebook(root)
my_notebook.pack(pady=15)

my_frame1 = Frame(my_notebook, width=500, height = 500, bg='#000000')#dashboard
my_frame2 = Frame(my_notebook, width=500, height = 500, bg='#000000')#Console
my_frame3 = Frame(my_notebook, width=500, height = 500, bg='#000000')#auth
my_frame4 = Frame(my_notebook, width=500, height = 500, bg='#000000')#CAMERA
my_frame5 = Frame(my_notebook, width=500, height = 500, bg='#000000')#FPS
my_frame6 = Frame(my_notebook, width=500, height = 500, bg='#000000')#RFID


my_frame1.pack(fill="both", expand=1)
my_frame2.pack(fill="both", expand=1)
my_frame3.pack(fill="both", expand=1)
my_frame4.pack(fill="both", expand=1)
my_frame5.pack(fill="both", expand=1)
my_frame6.pack(fill="both", expand=1)

load = Image.open('res/bbg.jpg')
render = ImageTk.PhotoImage(load)
img = Label(my_frame1,image = render)
img.place(x=70, y=10)

my_notebook.add(my_frame1, text="Dashboard")
my_notebook.add(my_frame2, text="Console")
my_notebook.add(my_frame3, text="Authenticate")
my_notebook.add(my_frame4, text="CAMERA")
my_notebook.add(my_frame5, text="FPS")
my_notebook.add(my_frame6, text="RFID")

my_notebook.hide(my_frame2)
my_notebook.hide(my_frame3)
my_notebook.hide(my_frame4)
my_notebook.hide(my_frame5)
my_notebook.hide(my_frame6)

def exit_window():
    root.destroy()
    exit()

def show_logs():
    my_notebook.select(1)
    
def show_auth():
    my_notebook.select(2)
    
def show_camera():
    my_notebook.select(3)
    
def show_FPS():
    my_notebook.select(4)


def get_devStatus():
    col_list = ["Name", "MacID"]
    df = pd.read_csv("res/f.csv", usecols=col_list)
    for i in df.MacID:
        response = requests.get('http://iotrest.herokuapp.com/api/statusfetcher?macid='+i)
        if(response!=None):
            print("proceed\n")
            return i
        else:
            print("u can't proceed ")
    
def post_devStatus(Mid):
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    
    response = requests.post('http://iotrest.herokuapp.com/api/statusfetcher', json={
        "macId" : Mid,
        "statusTime" : current_time,
        "statusCode" : True
    })
    
    print("Status code: \n", response.status_code)
    print("Printing Entire Post Request\n")
    print(response.json())


def show_RFID():
    my_notebook.select(5)
    
e = Entry(my_frame6, width = 50)   
 
def WriteRfid_Done():
    dataLabel = Label(my_frame6, text = "Data Received:"+ e.get())
    dataLabel.grid(row=3 ,column=3)
    
def Write_RFID():    
    e.grid(row=1 ,column=2)
      
def ReadRfid():
    instLabel = Label(my_frame6, text = "Please place your card!")
    instLabel.grid(row=4 ,column=2, padx=10, pady=10)    
    #label_id = Label( my_frame6, textvariable=id, relief=RAISED )
    #label_text = Label( my_frame6, textvariable=text, relief=RAISED )
    #label_id.grid(row=6 ,column=2)
    #label_text.grid(row=6 ,column=3)
    reader = SimpleMFRC522()
    
    try:
        id, text = reader.read()
        whitecard = "512344609911"
        bluetag = "111066076445"
        dataLabel = Label(my_frame6, text = "Data Received:"+ text)
        dataLabel.grid(row=5 ,column=2, padx=10, pady=10)
        
      #  if str(id) == bluetag :
        if bluetag == bluetag :
            label_rfidRes = Label(my_frame6, text = "Accepted")
            label_rfidRes.grid(row=7 ,column=1, padx=10, pady=10)
            print('Accepted')
            post_devStatus()
            BleLabel = Label(my_frame6, text = "Please Connect Bluetooth Device"+ text)
            BleLabel.grid(row=6 ,column=2, padx=10, pady=10)
        else:
            label_rfidRes = Label(my_frame6, text = "Invalid User")
            label_rfidRes.grid(row=7 ,column=1, padx=10, pady=10)
            print('Invalid User')
            
    finally:
        GPIO.cleanup()
           
def on_start():
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    current_time = current_time.split(":")
    #print(current_time)
    #print("########")
    
    col_list = ["Name", "MacID"]
    df = pd.read_csv("f.csv", usecols=col_list)
    response = requests.get('http://iotrest.herokuapp.com/api/devicefetcher')
    # print(response.json())
    macid = ''
    for i in response.json():
        loginTime = i["loginTime"].split(":")
        print(loginTime) 
        totalLogTime = int(loginTime[0])*3600 + int(loginTime[1])*60 + int(loginTime[2])
        totalCurrentTime = int(current_time[0])*3600 + int(current_time[1])*60 + int(current_time[2])
        if abs(totalCurrentTime-totalLogTime) <= 600:
            Mid = i["macId"]
            
    
    count = 0
    for j in df.MacID:
        if j == Mid:
            print("proceed\n"+Mid)
            post_devStatus(Mid)
            break
        else:
            count += 1
    
    if count == len(df):
        print("Abort Process\n")
    
    

Cam_instLabel = Label(my_frame4, text = "Please place your face infront of the camera and then proceed!\nClick Space to capture.")
Cam_instLabel.grid(row=1 ,column=0, padx=10, pady=10)
    
def cam_capture():
     
    cam = cv2.VideoCapture(0)
    
    count = 0
    
    while True:
        ret, img = cam.read()
    
        cv2.imshow("Test", img)
    
        if not ret:
            break
    
        k=cv2.waitKey(1)
    
        if k%256==27:
            #For Esc key
            print("Close")
            break
        elif k%256==32:
            #For Space key
    
            print("Image "+str(count)+"saved")
            cam_saved = Label(my_frame4, text = "Imged Saved!")
            cam_saved.grid(row=2 ,column=0, padx=50, pady=10)
            file='faces/'+str(count)+'.jpg'
            cv2.imwrite(file, img)
            count +=1
    
    cam.release
    cv2.destroyAllWindows()

#face recognition for face_result button
def face_Result():

        #Load the jpg files into numpy arrays
    biden_image = face_recognition.load_image_file("rohit.jpg")
    obama_image = face_recognition.load_image_file("suraj.jpeg")
    unknown_image = face_recognition.load_image_file("faces/0.jpg")
    
    # Get the face encodings for each face in each image file
    # Since there could be more than one face in each image, it returns a list of encodings.
    # But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
    try:
        biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
        obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
    except IndexError:
        print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
        retry_Cam_Label = Label(my_frame4, text = "there is less light on your face!")
        retry_Cam_Label.grid(row=4 ,column=0, padx=50, pady=10)
    
    known_faces = [
        biden_face_encoding,
        obama_face_encoding
    ]
    
    # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
    results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
    
    print("Is the unknown face a picture of Biden? {}".format(results[0]))
    print("Is the unknown face a picture of Suraj? {}".format(results[1]))
    print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))
    
    if results[0] or results[1]:
      print("You can proceed now!")
      Cam_instLabel = Label(my_frame4, text = "Face Recognized.\nYou can proceed now!")
      Cam_instLabel.grid(row=4 ,column=0, padx=50, pady=10)
      
      post_devStatus(get_devStatus())

    else :
      print("Sorry! You can't proceed")
      Cam_instLabel = Label(my_frame4, text = "Face Not Recognized.\nSorry! You can't proceed.")
      Cam_instLabel.grid(row=4 ,column=0, padx=10, pady=10)


#exit Button
exit_button = Button(
        my_frame1,
        width=20,
        height=2,
        text="Exit!",
        command=exit_window,
        padx=2,
        pady=2,
        bg='#FF8C00',
        relief=RAISED)
exit_button.grid(row=0 ,column=1, padx=10, pady=300)


AccessLog_button = Button(
        my_frame1,
        width=20,
        height=2,
        text="Start",
        command=on_start,
        padx=2,
        pady=2,
        bg='#FF8C00',
        relief=RAISED)
AccessLog_button.grid(row=0 ,column=2, padx=10, pady=300)


Authinticate_button = Button(
        my_frame1,
        width=20,
        height=2,
        text="Authinticate",
        command=show_auth,
        padx=2,
        pady=2,
        bg='#FF8C00',
        relief=RAISED)
Authinticate_button.grid(row=0 ,column=3, padx=10, pady=300)


Camera_button = Button(
        my_frame3,
        width=20,
        height=2,
        text="Camera",
        command=show_camera,
        padx=2,
        pady=2,
        bg='#FF8C00',
        relief=RAISED)
Camera_button.grid(row=0 ,column=1, padx=70, pady=100)


RFID_button = Button(
        my_frame3,
        width=20,
        height=2,
        text="RFID",
        command=show_RFID,
        padx=2,
        pady=2,
        bg='#FF8C00',
        relief=RAISED)
RFID_button.grid(row=0 ,column=2, padx=10, pady=100)

FPS_button = Button(
        my_frame3,
        width=20,
        height=2,
        text="FPS",
        command=show_FPS,
        padx=2,
        pady=2,
        bg='#FF8C00',
        relief=RAISED)
FPS_button.grid(row=1 ,column=1, padx=10, pady=10)

Bluetooth_button = Button(
        my_frame3,
        width=20,
        height=2,
        text="Connect Bluetooth",
        command=show_auth,
        padx=2,
        pady=2,
        bg='#FF8C00',
        relief=RAISED)
Bluetooth_button.grid(row=1 ,column=2, padx=50, pady=10)


CamCapture_button = Button(
        my_frame4,
        width=20,
        height=2,
        text="Click to Capture!",
        command=cam_capture,
        padx=2,
        pady=2,
        bg='#FF8C00',
        relief=RAISED)
CamCapture_button.grid(row=0 ,column=0, padx=50, pady=30)

FaceResult_button = Button(
        my_frame4,
        width=20,
        height=2,
        text="Result!",
        command=face_Result,
        padx=2,
        bg='#FF8C00',
        pady=2,
        relief=RAISED)
FaceResult_button.grid(row=3 ,column=0, padx=50, pady=30)
    
READ_button = Button(
        my_frame6,
        width=20,
        height=2,
        text="READ",  
        command=ReadRfid,
        padx=2,
        pady=2,
        bg='#FF8C00',
        relief=RAISED)
READ_button.grid(row=0,column=1, padx=10, pady=10)


WRITE_button = Button(
        my_frame6,
        width=20,
        height=2,
        text="WRITE",
        command=Write_RFID,
        padx=2,
        pady=2,
        bg='#FF8C00',
        relief=RAISED)
WRITE_button.grid(row=1 ,column=1, padx=10, pady=10)

WriteRfid_done_button = Button(
        my_frame6,
        width=20,
        height=2,
        text="Write data",
        command=WriteRfid_Done,
        padx=2,
        pady=2,
        bg='#FF8C00',
        relief=RAISED)
WriteRfid_done_button.grid(row=3 ,column=2, padx=10, pady=10)

root.mainloop()