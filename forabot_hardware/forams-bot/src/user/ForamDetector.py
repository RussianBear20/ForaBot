from abc import ABC, abstractmethod
import cv2
import numpy as np
import sys
from statistics import mean

class ForamDetector:

    def __init__(self, num_focal_planes):
        self.needle_detector = ConvIdentifier('_needle',method='cv2.TM_CCOEFF_NORMED')
        self.funnel_detector = BlobIdentifier()
        self.microscope_detector = HistogramIdentifier(num_focal_planes)

    def addNeedleCalib(self, image, focal_plane, light_dir):
        fp_i = int(focal_plane)
        ld_i = int(light_dir)
        self.microscope_detector.addNeedleCalib(np.float32(image), fp_i, ld_i)

    def isForamOnNeedle(self, img):
        return True #self.needle_detector.classify(img)


    def isForamInMicroscope(self, img, focal_plane, light_dir):
        fp_i = int(focal_plane)
        ld_i = int(light_dir)
        return True #self.microscope_detector.classify_fp(np.float32(img), fp_i, ld_i)

    def isForamInFunnel(self, img):
        return True #self.funnel_detector.classify(img)

class Identifier(ABC):

    @abstractmethod
    def classify(self, image):
        return

class BlobIdentifier(Identifier):
    def __init__(self):
        params = cv2.SimpleBlobDetector_Params()
        params.minThreshold = 200
        params.maxThreshold = 256
        params.filterByColor = 1
        params.blobColor = 255
        params.filterByArea = True
        params.minArea = 30
        params.filterByConvexity = False
        self.detector = cv2.SimpleBlobDetector_create(params)

        '''
        hole_params = cv2.SimpleBlobDetector_Params()
        hole_params.minThreshold = 0
        hole_params.maxThreshold = 175
        hole_params.filterByColor = 1
        hole_params.blobColor = 0
        hole_params.filterByArea = True
        hole_params.minArea = 8
        self.hole_detector = cv2.SimpleBlobDetector_create(hole_params)
        '''

    def classify(self, image):
        img = image[315:910,375:805]
        keypoints = self.detector.detect(img)
        return len(keypoints)>0

'''
class FeatureIdentifier(Identifier):
    def __init__(self, detect_type ,threshold=0.75):
        self.no_foram_needle = cv2.imread('resources/no_foram'+detect_type+'.png',cv2.IMREAD_GRAYSCALE)
        self.foram_needle = cv2.imread('resources/foram'+detect_type+'.png',cv2.IMREAD_GRAYSCALE)
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        self.orb = cv2.ORB_create()
        self.n_kp, self.n_desc = self.orb.detectAndCompute(self.no_foram_needle,None)
        self.f_kp, self.f_desc = self.orb.detectAndCompute(self.foram_needle,None)
        self.threshold = threshold

    def classify(self, image):
        query_kp, query_desc = self.orb.detectAndCompute(image,None)

        not_foram_m = self.matcher.knnMatch(self.n_desc,query_desc,k=2)
        is_foram_m = self.matcher.knnMatch(self.f_desc,query_desc,k=2)

        not_foram = self.ratio_test(not_foram_m)
        is_foram = self.ratio_test(is_foram_m)
        print(is_foram, not_foram)
        return is_foram > not_foram

    def ratio_test(self, matches):
        good = []
        for m,n in matches:
            if m.distance < self.threshold*n.distance:
                good.append([m])
        return len(good)
'''

class ConvIdentifier(Identifier):
    def __init__(self, detect_type, method, threshold = 0.95):
        self.no_foram_needle = cv2.imread('user/resources/no_foram'+detect_type+'.png',cv2.IMREAD_GRAYSCALE)
        self.foram_needle = cv2.imread('user/resources/foram'+detect_type+'.png',cv2.IMREAD_GRAYSCALE)
        self.w, self.h = self.no_foram_needle.shape[::-1]
        self.method = eval(method)
        self.threshold = threshold

    def classify(self, image):
        ratio_vals = []
        res1 = cv2.matchTemplate(image, self.foram_needle, self.method)
        res2 = cv2.matchTemplate(image, self.no_foram_needle, self.method)

        min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(res1)
        min_val2, max_val2, min_loc2, max_loc2 = cv2.minMaxLoc(res2)
        if self.method is cv2.TM_SQDIFF_NORMED:
            ratio_vals.append(min_val2/(min_val1-sys.float_info.epsilon))
        else:
            ratio_vals.append(max_val1/(max_val2+sys.float_info.epsilon))
        return mean(ratio_vals) > self.threshold

class HistogramIdentifier(Identifier):
    def __init__(self, num_focal_planes, threshold=15000):
        self.threshold = threshold
        self.calib_imgs = [[None,None]]*num_focal_planes
        self.focal_hists = [[None,None]]*num_focal_planes
        c1_ranges = [20, 256]
        c2_ranges = [20, 256]
        c3_ranges = [20,256]
        c1_bins = c1_ranges[1]-c1_ranges[0]
        c2_bins = c2_ranges[1]-c2_ranges[0]
        c3_bins = c3_ranges[1]-c3_ranges[0]
        self.channels = [0,1,2]
        self.ranges = c1_ranges + c2_ranges + c3_ranges
        self.histSize = [c1_bins, c2_bins, c3_bins]
        self.compare_method = 1
        self.curr_focal_plane = 0
        self.curr_light_dir = 0

    def addNeedleCalib(self, img, focal_plane, light_dir):
        self.calib_imgs[focal_plane][light_dir] = img
        self.focal_hists[focal_plane][light_dir] = cv2.calcHist([img], self.channels, None, self.histSize, self.ranges)

    def classify_fp(self, image, focal_plane, light_dir):
        self.curr_focal_plane = focal_plane
        self.curr_light_dir = light_dir
        return self.classify(image)

    def classify(self, image):
        comp_hist = cv2.calcHist([image], self.channels, None, self.histSize, self.ranges)
        metric_val = cv2.compareHist(comp_hist, self.focal_hists[self.curr_focal_plane][self.curr_light_dir], self.compare_method)
        return metric_val>self.threshold
