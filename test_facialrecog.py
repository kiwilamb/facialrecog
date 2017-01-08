import pytest
import cv2
from facialrecog import FacialRecog


class TestFacialRecog:
    def test_init(self):
        assert FacialRecog(timeout=20) is not None
        assert FacialRecog("bunny.mp4") is not None
        with pytest.raises(IOError):
            FacialRecog("thisfiledoesnotexist.mp4")
        make_webcam_busy = cv2.VideoCapture(0)
        with pytest.raises(Exception):
            FacialRecog()
        make_webcam_busy.release()
