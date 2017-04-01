import os
import re
import bz2
import sys
import cv2
import time
import shutil
from openface import align_dlib


class FacialRecog:

    def __init__(self, timeout=10):
        if not os.path.isfile(landmarks_file):
            url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
            response = urllib.request.urlopen(url)
            data = response.read()
            uncompressed_data = bz2.decompress(data)
            open(landmarks_file, 'wb').write(uncompressed_data)
        self.face_alinger = align_dlib.AlignDlib(landmarks_file)

        self.video = cv2.VideoCapture(0)
        timeout += time.time()
        while not self.video.isOpened() and time < timeout:
            self.video = cv2.VideoCapture(file)
            cv2.waitKey(1000)
            print("Waiting for the video capture to start...")

        if not self.video.isOpened():
            raise Exception("Couldn't connect to webcam")

    def _play_video(self, exit=27, timeout=300):
        """
        Play webcam video. For each frame detect largest face 
        and draw rectangle around it

        :return: nothing
        """
        print("Playing webcam video ...")
        start = time.time()
        timeout += time.time()
        frames = 0
        while time.time() < timeout:
            frames += 1
            flag, frame = self.video.read()
            largest_face_box = self.face_alinger.getLargestFaceBoundingBox(frame)
            if largest_face_box is not None:
                top_left = (largest_face_box.left(), largest_face_box.top())
                bottom_right = (largest_face_box.right(), largest_face_box.bottom())
                cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0))
                result = {
                    "image": frame, 
                    "rect": {
                        "top_left": top_left,
                        "bottom_right": bottom_right
                    }
                }
            else:
                result = {"image": frame}
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) == exit:
                print("Stopping webcam video")
                break
        fps = frames / (time.time() - start)
        print("FPS: {}".format(fps))

        return result

    def save_person(self, name, timeout=20):
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
            for attempt in range(3):
                largest_face = self._play_video(67, timeout)
                if "rect" in largest_face:
                    face_detected = True
                    break
                else:
                    face_detected = False
                    print("No face detected, ensure your face is in front of the webcam")
            if not face_detected:
                raise Exception("No face detected for image {} after 3 attempts".format(i))
            file_name = os.path.join(base_dir, parsed_name + "-" + str(i) + ".png")
            cv2.imwrite(file_name, largest_face["image"])
        
        cv2.destroyAllWindows()
        print("Thank you, {} has been saved here: {}".format(name, base_dir))

    def delete_person(self, name):
        parsed_name = "_".join([n.lower() for n in name.split()])
        base_dir = os.path.join(os.path.realpath("."), "people", parsed_name)
        
        if os.path.isdir(base_dir):
            print("Deleting {}".format(base_dir))
            shutil.rmtree(base_dir)
        else:
            print("{} does not exist".format(base_dir))

    def list_people(self):
        people = os.listdir(os.path.join(os.path.realpath("."), "people"))
        print("The following people have been saved:")
        for person in people:
            print("    {}".format(person))

if __name__ == '__main__':
    fr = FacialRecog()
    fr.save_person("Bob")
    fr.list_people()
    fr.delete_person("Bob")
    # fr.process_frames()
