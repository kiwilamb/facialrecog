import os
import cv2
import time
import dlib


class FacialRecog:

    def __init__(self, file=0, timeout=10):
        self.file = file
        self.face_detector = dlib.get_frontal_face_detector()
        # If the file is 0 use the webcam as the video capture device
        if self.file is not 0:
            if not os.path.isfile(self.file):
                raise IOError("Couldn't find file {}".format(self.file))

        self.video = cv2.VideoCapture(self.file)
        timeout += time.time()
        while not self.video.isOpened() and time < timeout:
            self.video = cv2.VideoCapture(self.file)
            cv2.waitKey(1000)
            print("Waiting for the video capture to start...")

        if not self.video.isOpened():
            raise Exception("Couldn't connect to {}".format("webcam" if self.file == 0 else self.file))

    def play_video(self):
        '''
        Plays video feed (webcam or video file)
        :return: nothing
        '''
        print("Playing {} video ...".format("webcam" if self.file == 0 else self.file))
        start = time.time()
        frames = 0
        while True:
            frames += 1
            flag, frame = self.video.read()
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) == 27:
                print("Stopping {} video".format("webcam" if self.file == 0 else self.file))
                break
            if self.file is not 0 and self.video.get(cv2.CAP_PROP_POS_FRAMES) == self.video.get(cv2.CAP_PROP_FRAME_COUNT):
                # This works as it checks if it is a file first, if not it doesn't bother with other checks
                print("Stopping {} video".format("webcam" if self.file == 0 else self.file))
                break
        fps = frames / (time.time() - start)
        print("FPS: {}".format(fps))


if __name__ == '__main__':
    fr = FacialRecog()
    fr.play_video()
