import os
import re
import sys
import cv2
import time
from openface import align_dlib


class FacialRecog:

    def __init__(self, file=0, timeout=10):
        self.device = "webcam" if file == 0 else file
        self.face_alinger = align_dlib.AlignDlib("shape_predictor_68_face_landmarks.dat")
        # If the file is 0 use the webcam as the video capture device
        if file is not 0:
            if not os.path.isfile(file):
                raise IOError("Couldn't find file {}".format(file))

        self.video = cv2.VideoCapture(file)
        timeout += time.time()
        while not self.video.isOpened() and time < timeout:
            self.video = cv2.VideoCapture(file)
            cv2.waitKey(1000)
            print("Waiting for the video capture to start...")

        if not self.video.isOpened():
            raise Exception("Couldn't connect to {}".format(self.device))

    def process_frames(self):
        """
        Plays video feed (webcam or video file)
        :return: nothing
        """
        print("Playing {} video ...".format(self.device))
        start = time.time()
        frames = 0
        while True:
            frames += 1
            flag, frame = self.video.read()
            largest_face_box = self.face_alinger.getLargestFaceBoundingBox(frame)
            if largest_face_box is not None:
                top_left = (largest_face_box.left(), largest_face_box.top())
                bottom_right = (largest_face_box.right(), largest_face_box.bottom())
                cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0))
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) == 27:
                print("Stopping {} video".format(self.device))
                break
            if self.device is not "webcam" and self.video.get(cv2.CAP_PROP_POS_FRAMES) == self.video.get(cv2.CAP_PROP_FRAME_COUNT):
                # This works as it checks if it is a file first, if not it doesn't bother with other checks
                print("Stopping {} video".format(self.device))
                break
        fps = frames / (time.time() - start)
        print("FPS: {}".format(fps))

    def save_person(self, name):
        print("===================================================================")
        print("Facialrecog will take 10 pictures of you face using your webcam.")
        print("Try to align your face in different angles so it can recognise you.")
        print("Press 'C' to capture the image (note this is capital 'C')")
        print("===================================================================")

        parsed_name = "_".join([n.lower() for n in name.split()])
        base_dir = os.path.join(os.path.realpath("."), "people", parsed_name)
        
        if os.path.isdir(base_dir):
            print("{} is already a saved person".format(name))
            file_names = os.listdir(base_dir)
            correct_format = [bool(re.match(parsed_name + "-\d+.png", file)) for file in file_names]
            if sum(correct_format) == 10:
                print("All of {}'s files are saved correctly".format(name))
            else:
                print("{} of {}'s files are not saved correctly".format(str(10 - sum(correct_format)), name))
                print("Delete {} and readd the files".format(parsed_name))
            return None
        else:
            os.makedirs(base_dir)

        for i in range(1, 11):
            print("Taking image {}, press 'C' to capture".format(i))
            while True:
                flag, frame = self.video.read()
                cv2.imshow(name, frame)
                # May want to have face detection stuff repeated here so we can ensure image is worthwhile (don't allow picture unless contains a face
                if cv2.waitKey(1) == 67:
                    print("Snap!")
                    break
            file_name = os.path.join(base_dir, parsed_name + "-" + str(i) + ".png")
            cv2.imwrite(file_name, frame)
        
        cv2.destroyAllWindows()
        print("Thank you, {} has been saved here: {}".format(name, base_dir))

if __name__ == '__main__':
    fr = FacialRecog()
    # fr.process_frames()
