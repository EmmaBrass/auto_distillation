import cv2
import time
import os

RTMP_URL = "rtmp://10.236.65.56/bcs/channel1935_main.bcs?channel=1935&stream=0&user=admin&password=Reolink5"
RTSP_URL = "rtsp://admin:Reolink5@10.236.65.56:554/h264Preview_01_main"
#os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'
#cap = cv2.VideoCapture(RTSP_URL)

def resize(input_image):
    h, w = input_image.shape[:2]
    aspect = h/w
    new_width = 600
    new_height = int(new_width*aspect)
    output_image = cv2.resize(input_image, dsize=(new_width,new_height))
    return output_image

time.sleep(2)
while True:
    cap = cv2.VideoCapture(RTSP_URL)
    print('waiting 4 sec')
    time.sleep(4)
    print("taking picture")
    ret, frame = cap.read() # take a picture with the camera
    print(ret)
    new_image = resize(frame)
    cv2.imshow("image", new_image)
    cv2.waitKey(4000)
    cv2.destroyAllWindows()
    cap.release()