from datetime import datetime
from time import time
import numpy as np
import cv2, sys

rotatelist={ # list cv2 option
    "Rotate_90":cv2.ROTATE_90_CLOCKWISE,
    "Rotate_270":cv2.ROTATE_90_COUNTERCLOCKWISE,
    "Rotate_180":cv2.ROTATE_180,
}

class VideoCamera(object):
    def __init__(self, url, rotate=""):
        self.rotate = rotatelist.get(rotate)
        self.video = cv2.VideoCapture(url)

    def __del__(self):
        self.video.release()

    def isOpened(self):
        return self.video.isOpened()

    def get_fps(self):
        result = self.video.get(cv2.CAP_PROP_FPS)
        if result > 60 or result < 1: 
            result = None
        return result

    def get_frame(self):
        rc = self.video.grab()
        success, image = self.video.retrieve()
        if image is None:
            return None
        nowtime = time()
        image = self.gamma_correction(image, gamma=0.5)
        if not self.rotate is None:
            image = cv2.rotate(image, self.rotate)
        image = cv2.putText(image, str(datetime.fromtimestamp(nowtime)),
                (0, 18), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 196, 0), 4, cv2.LINE_AA)
        image = cv2.putText(image, str(datetime.fromtimestamp(nowtime)),
                (0, 18), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg
#https://pystyle.info/opencv-change-contrast-and-brightness/
    def gamma_correction(self, img, gamma):
        table = (np.arange(256) / 255) ** gamma * 255
        table = np.clip(table, 0, 255).astype(np.uint8)
        return cv2.LUT(img, table)