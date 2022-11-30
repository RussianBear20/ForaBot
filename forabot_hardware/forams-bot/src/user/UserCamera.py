import random
from user.utilities.drivers.camera import ToupCamCamera
from user.ForamDetector import ForamDetector
import cv2
import time
import datetime
import numpy as np
import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

class UserCamera():
    def __init__(self, write_queue, read_queue, usb_cam_loc, num_focal_planes):
        self.write_queue = write_queue
        self.read_queue = read_queue
        self.is_running = True
        self.initializeWebcam(usb_cam_loc)
        self.initializeMicroscopeCam()
        self.foram_detector = ForamDetector(num_focal_planes)
        self.executor = ThreadPoolExecutor(None)
        self.root_dir = os.path.join(os.getcwd(),'..','data', datetime.datetime.now().strftime('%Y%m%d_%H%M'))
        os.makedirs(self.root_dir)
        self.foram_failed_str = '{{"function":"foramFailed", "args":["{0}","{1}"]}}'
        self.run_next_automated_str = '{"function":"runNextAutomatedStep", "args":[]}'
        self.run_next_automated_calibration_str = '{"function":"runNextCalibrationStep", "args":[]}'

    def initializeMicroscopeCam(self):
        try:
            cam = ToupCamCamera(resolution=3)
            cam.open()
            cam.set_auto_exposure(False)
            cam.set_exposure_time(200000)
            cam.set_gain(200)
            self.microscope_cam = cam
        except:
            raise RuntimeError("Unable to initialize microscope camera")

    def initializeWebcam(self, loc):
        cap = cv2.VideoCapture(loc)
        if cap.isOpened():
            self.webcam = cap
            #set buffer size
            self.webcam.set(cv2.CAP_PROP_BUFFERSIZE,1)
            for i in range(5):
                ret = self.webcam.grab()
            if ret is None:
            	raise RuntimeError("Unable to grab from webcam")
        else:
            raise RuntimeError("Unable to initialize webcam")

    def run(self):
        while self.is_running:
            msg = self.__executeReadMessages()
            self.write_queue.put(msg)

    def __executeReadMessages(self):
        fn, args = self.read_queue.get()
        message = fn(*args)
        return message

    def takeNeedleImage(self, light_dir, focal_plane):
        if self.isMicroscopeCamActive():
            save_loc = os.path.join(self.root_dir,'needle','{}_{}.tiff'.format(light_dir,focal_plane))
            os.makedirs(os.path.join(self.root_dir,'needle'), exist_ok=True)
            im = self.microscope_cam.get_pil_image()
            self.executor.submit(self.save_tiff, im, save_loc)
            self.foram_detector.addNeedleCalib(im,focal_plane,light_dir)
        return self.run_next_automated_calibration_str

    def takeImage(self, foram_num, light_dir, focal_plane, orientation_id):
        if self.isMicroscopeCamActive():
            base_dir = os.path.join(self.root_dir, foram_num, orientation_id)
            os.makedirs(base_dir, exist_ok=True)
            save_loc = os.path.join(base_dir,'{}_{}.tiff'.format(light_dir,focal_plane))
            im = self.microscope_cam.get_pil_image()
            self.executor.submit(self.save_tiff, im, save_loc)
            if not self.isForamPresentMicroscope(im, focal_plane, light_dir):
                return self.foram_failed_str.format('imaging_mid', orientation_id)
        return self.run_next_automated_str

    def save_tiff(self, img, file_name):
        img.save(file_name, 'TIFF')

    def takeWebcamImage(self, foram_num, foram_loc, state):
        if self.isWebcamActive():
            base_dir = os.path.join(self.root_dir, foram_num)
            os.makedirs(base_dir, exist_ok=True)
            save_loc = os.path.join(base_dir,foram_loc+'.png')
            #ret, frame = self.webcam.read()
            for i in range(2):
                ret = self.webcam.grab()

            if ret:
                ret, frame = self.webcam.retrieve()
            else:
            	print('Failed to grab from webcam')
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(save_loc,gray)
                if self.isForamPresent(gray, foram_loc):
                    return self.run_next_automated_str
                else:
                    print('Foram {} failed at {}'.format(foram_num, foram_loc))
                    return self.foram_failed_str.format(foram_loc, state)
            else:
            	print('Failed to retrieve from webcam')
        print('Failed to connect to webcam')
        return self.foram_failed_str.format(foram_loc, state)

    def isForamPresent(self, gray, foram_loc):
        if foram_loc == 'isolation_needle':
            return self.isForamPresentNeedle(gray)
        else:
            check_foram = self.isForamPresentFunnel(gray)
            if foram_loc == 'imaging_start':
                return check_foram
            elif foram_loc == 'imaging_end':
                return not check_foram
            else:
                raise Exception("What is check for foram at: {}".format(foram_loc))

    def isForamPresentNeedle(self, img):
        return self.foram_detector.isForamOnNeedle(img)

    def isForamPresentFunnel(self, img):
        return self.foram_detector.isForamInFunnel(img)

    def isForamPresentMicroscope(self, img, focal_plane, light_dir):
        return self.foram_detector.isForamInMicroscope(img, focal_plane, light_dir)

    def classifyForam(self, foram_num):
        #run classifier on proper foram dir
        well_num = random.randint(0,15)
        return '{{"function":"runNextAutomatedStep", "args":[[{}]]}}'.format(well_num)

    def isWebcamActive(self):
        return self.webcam is not None

    def isMicroscopeCamActive(self):
        return self.microscope_cam is not None

    def releaseWebcam(self):
        if self.isWebcamActive():
            self.webcam.release()

    def shutdown(self):
        self.executor.shutdown(wait=True, cancel_futures=False)
        self.releaseWebcam()
        cv2.destroyAllWindows()
        self.is_running = False
