import glob,os,time
import cv2
from emailing import send_email
from threading import Thread

video=cv2.VideoCapture(0,cv2.CAP_DSHOW)
time.sleep(1)

first_frame=None
status_list=[]
sent_image=[]
count=0

def clean_dir():
    images=glob.glob("images/*.png")
    for image in images:
        os.remove(image)

while True:
    status=0
    check,frame=video.read()
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame_gauss=cv2.GaussianBlur(gray_frame,(21,21),0)

    if first_frame is None:
        first_frame=gray_frame_gauss

    delta_frame=cv2.absdiff(first_frame,gray_frame_gauss)
    thres_frame=cv2.threshold(delta_frame,60,255,cv2.THRESH_BINARY)[1]
    dil_frame=cv2.dilate(thres_frame,None,iterations=2)

    contours,check=cv2.findContours(dil_frame,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x,y,h,w=cv2.boundingRect(contour)
        rectangle=cv2.rectangle(frame,(x,y), (x+w,y+h), (0,255,0),3)
        if rectangle.any():
            status=1
            cv2.imwrite(f"images/{count}.png",frame)
            count=count+1
            all_images=glob.glob("images/*.png")
            sorted_images=sorted(all_images,key=os.path.getmtime)
            index=int(len(sorted_images)/2)
            image_with_object=sorted_images[index]



    status_list.append(status)
    status_list=status_list[-2:]

    if status_list[0]==1 and status_list[1]==0:
        if image_with_object not in sent_image:
            sent_image.append(image_with_object)
            email_thread=Thread(target=send_email,args=(image_with_object, ))
            email_thread.daemon=True
            email_thread.start()

    cv2.imshow("Video",frame)

    key=cv2.waitKey(1)
    if key==ord("q"):
        break

video.release()

print("Folder cleaning started")
clean_thread = Thread(target=clean_dir())
clean_thread.daemon = True
clean_thread.start()
clean_thread.join()
print("Folder cleaning ended")
# array=cv2.imread("image.png")
# print(array)