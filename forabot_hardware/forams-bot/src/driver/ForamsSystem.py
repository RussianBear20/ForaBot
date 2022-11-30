from driver.controller import DCController, LightController, ServoController, StepperController, VibrationController
import config_setup.ConfigUtility as CU
from communication.SerialServer import SerialServer as sServer
from communication.ServerMessageHandler import ServerMessageHandler
import time

#Check/fix imaging indices and foram counter. Seems off
class ForamsSystem:
    def __init__(self, config_file_location):
        self.config_file_location = config_file_location
        self.conf_dict = CU.parseFile(config_file_location)

        self.session_foram_count = 0

        dc_dict, servo_dict, light_dict, stepper_dict, vibration_dict = CU.partitionDicts(self.conf_dict)

        self.dc_controller = DCController.DCController(dc_dict)
        self.servo_controller = ServoController.ServoController(servo_dict)
        self.light_controller = LightController.LightController(light_dict)
        self.stepper_controller = StepperController.StepperController(stepper_dict)
        self.vibration_controller = VibrationController.VibrationController(vibration_dict)

        self.request_ui_input = '{"end_point":"ui","function":"getNextUserCommand","args":[]}'
        self.request_imaging = '{{"end_point":"camera","function":"takeImage","args":["{0}","{1}","{2}","{3}"]}}'
        self.request_needle_imaging = '{{"end_point":"camera","function":"takeNeedleImage","args":["{0}","{1}"]}}'
        self.request_image_check = '{{"end_point":"camera","function":"takeWebcamImage","args":["{0}","{1}","{2}"]}}'
        self.request_classification = '{{"end_point": "camera","function":"classifyForam","args":["{0}"]}}'
        self.ret_message = self.request_ui_input

        self.homeSystem()

        self.ser_server = self.__initSerialServer()
        self.ser_server.run()

    def __initSerialServer(self):
        try:
            message_handler = ServerMessageHandler(self)
            server = sServer(message_handler)
            return server
        except:
            raise RuntimeError("Initialization of server failed for system type: " + self.__class__.__name__)

    def returnMessage(self, message):
        return message

    def startSystem(self, num_forams, failure_threshold, image_orientations,
                        light_directions, lights_per_img, light_steps,
                        num_focal_planes, start_focal_offset, focal_plane_step):
        self.failure_threshold = failure_threshold
        self.image_orientations = image_orientations
        self.light_directions = light_directions
        self.light_controller.setRunParams(lights_per_img, light_steps)
        self.num_focal_planes = num_focal_planes
        self.stepper_controller.setFocalOffset(start_focal_offset)
        self.focal_plane_step = focal_plane_step
        self.run_state = {'num_forams':num_forams, 'curr_foram':0, 'num_foram_failures':0, 'num_image_failures':0, 'curr_fn':0, 'curr_img':0}
        self.run_fns = [self.pickForam, self.transferIsolationToImaging, self.imageForamStart, self.foramImaging]
        self.run_fns.extend( [self.imageForamEnd, self.requestClassification, self.sortForam])
        ###remove next block of lines
        #self.run_fns = [self.pickForam, self.transferIsolationToImaging, self.requestClassification, self.sortForam]
        #self.session_foram_count=1
        ###
        self.ret_message = None
        if self.session_foram_count == 0:
            self.servo_controller.moveToImaging()
            self.calibration_state = {'curr_img':0}
            self.calibration_fns = [self.runNextCalibrationStep]*(self.light_directions*self.num_focal_planes)
            return self.runNextCalibrationStep()
        return self.runNextAutomatedStep()

    def homeSystem(self):
        self.stepper_controller.homePins()
        self.dc_controller.imagingSuctionOff()
        self.dc_controller.isolationSuctionOff()

    def runNextCalibrationStep(self):
        light_dir = self.calibration_state['curr_img']%self.light_directions
        focal_plane = (self.calibration_state['curr_img']//self.light_directions) % self.num_focal_planes
        self.stepper_controller.setFocalPlane(focal_plane*self.focal_plane_step)
        self.light_controller.lightForam(light_dir)
        self.calibration_state['curr_img'] += 1
        if self.calibration_state['curr_img'] > self.light_directions*self.num_focal_planes:
            self.light_controller.lightsOff()
            self.stepper_controller.imagingBottom()
            self.stepper_controller.focalBottom()
            return self.runNextAutomatedStep()
        return self.request_needle_imaging.format(light_dir, focal_plane)

    def runNextAutomatedStep(self, args=[]):
        msg = None
        print(self.run_state)
        if self.run_state['curr_fn'] >= len(self.run_fns):
            self.run_state['curr_fn'] = self.run_state['curr_fn']%len(self.run_fns)
            self.run_state['curr_foram'] += 1
            self.session_foram_count += 1
        if self.checkRunComplete():
            self.ret_message = self.request_ui_input
            return self.ret_message
        if self.checkSystemFailure():
            self.homeSystem()
            self.ret_message = self.request_ui_input
            return self.ret_message
        while msg is None:
            if self.run_state['curr_fn'] > len(self.run_fns):
                raise Exception('ENDING A FORAM IMAGING PROCESS REQUIRES CLIENT SIGNOFF')
            msg = self.run_fns[self.run_state['curr_fn']](*args)
            self.run_state['curr_fn'] += 1
            if self.ser_server.checkShutdownOrCancel():
                self.vibration_controller.stop()
                self.stepper_controller.stop()
                return None
            args=[]
        return msg

    def checkRunComplete(self):
        return self.run_state['num_forams'] <= self.run_state['curr_foram'] and self.run_state['num_forams'] > 0

    def checkSystemFailure(self):
        return self.run_state['num_foram_failures'] >= self.failure_threshold

    def requestClassification(self):
        return self.request_classification.format(self.run_state['curr_foram'])

    def sortForam(self, well_num):
        self.run_state['curr_img'] = 0
        self.servo_controller.moveWellToIdx(well_num)
        self.servo_controller.moveToImagingPick()
        self.dc_controller.imagingSuctionOn()
        self.vibration_controller.imagingVibrationPulse()
        self.stepper_controller.imagingHandoff()
        self.dc_controller.imagingHandoff()
        self.stepper_controller.imagingBottom()
        self.stepper_controller.focalBottom()
        self.servo_controller.moveToWell()
        self.dc_controller.dropForam()
        self.vibration_controller.topVibrationPulse()
        self.servo_controller.moveToImagingWebcam()
        return self.request_image_check.format(self.session_foram_count, 'imaging_end', well_num)


    def imageForamStart(self, tmp=[]):
        self.servo_controller.moveToImaging()
        self.dc_controller.imagingSuctionOn()
        self.vibration_controller.imagingVibrationPulse()
        self.stepper_controller.imageForam()
        self.dc_controller.imagingSuctionOff()
        return None

    def foramImaging(self):
        light_dir = self.run_state['curr_img']%self.light_directions
        focal_plane = (self.run_state['curr_img']//self.light_directions) % self.num_focal_planes
        orientation_id = self.run_state['curr_img']//(self.light_directions * self.num_focal_planes)
        if light_dir == 0 and focal_plane == 0 and  self.run_state['curr_img']>0:
            self.imageForamChangeOrientation()
        if light_dir == 0:
            #self.dc_controller.imagingSuctionOn()
            self.stepper_controller.setFocalPlane(focal_plane*self.focal_plane_step)
            #self.dc_controller.imagingSuctionOff()
        self.light_controller.lightForam(light_dir)
        self.run_state['curr_img'] += 1
        if self.run_state['curr_img'] < (self.light_directions*self.image_orientations*self.num_focal_planes):
            self.run_state['curr_fn'] -= 1
        return self.request_imaging.format(self.session_foram_count, light_dir, focal_plane, orientation_id)

    def imageForamEnd(self):
        self.resetImagingNeedle()
        self.stepper_controller.focalBottom()
        return None
    
    def resetImagingNeedle(self):
        self.light_controller.lightsOff()
        self.dc_controller.imagingSuctionOff()
        self.stepper_controller.imagingBottom()
        self.vibration_controller.imagingVibrationPulse()
        time.sleep(0.1)
        self.vibration_controller.imagingVibrationPulse()
        time.sleep(0.1)
        self.vibration_controller.imagingVibrationPulse()

    def imageForamChangeOrientation(self):
        self.resetImagingNeedle()
        self.imageForamStart()

    def pickForam(self, state_var=0):
        self.servo_controller.moveToIsolationIsolationWebcam()
        self.vibration_controller.isolationVibrationPulse()
        self.dc_controller.isolationSuctionOn()
        self.stepper_controller.isolationCheck()
        return self.request_image_check.format(self.session_foram_count, 'isolation_needle', state_var)

    def resetIsolationPick(self, state):
        self.dc_controller.isolationSuctionOff()
        self.stepper_controller.isolationBottom()

    def foramFailed(self, location, state_var):
        #imaging_end state_var is the species classification
        #imaging_start state_var is how many times we didn't see a foram
        #imaging_mid state_var is the orientation
        #isolation_needle is how many failed picks
        print('Foram {} failed at {} with state {}'.format(self.run_state['curr_foram'], location, state_var))
        print(self.run_state)
        if location == 'imaging_end':
            #failed handoff to sort
            self.run_state['num_foram_failures'] += 1
            ret_message = self.sortForam(state_var)
        elif location == 'imaging_start':
            #failed handoff to imaging
            state_var = int(state_var)
            if state_var <=5:
                ret_message = self.attemptTransferDrop(state_var+1)
            else:
                self.run_state['num_foram_failures'] += 1
                self.run_state['curr_fn'] = 0
                ret_message = self.runNextAutomatedStep()
        elif location == 'imaging_mid':
            #failed foram balancing
            state_var = int(state_var)
            self.run_state['curr_img'] = (self.light_directions * self.num_focal_planes)*state_var
            ret_message = self.runNextAutomatedStep()
            self.run_state['num_foram_failures'] += 1
        elif location == 'isolation_needle':
            #failed foram pick
            if state_var > 3:
                self.run_state['num_foram_failures'] += 1
                state_var = -1
            self.resetIsolationPick()
            ret_message = self.pickForam(state_var+1)
        else:
            raise Exception('Unexpected location for no foram detection at: {}'.format(location))
        if self.checkSystemFailure() or self.checkRunComplete():
            self.run_state['num_foram_failures'] = 0
            self.homeSystem()
            self.ret_message = self.request_ui_input
            ret_message = self.ret_message
        return ret_message

    def attemptTransferDrop(self, attempt_num):
        self.servo_controller.moveToImagingPick()
        self.dc_controller.dropForam()
        self.vibration_controller.topVibrationPulse()
        self.servo_controller.moveToImagingWebcam()
        return self.request_image_check.format(self.session_foram_count, 'imaging_start', attempt_num)

    def transferIsolationToImaging(self):
        self.servo_controller.moveToIsolationPick()
        self.stepper_controller.isolationHandoff()
        self.dc_controller.isolationHandoff()
        self.stepper_controller.isolationBottom()
        self.servo_controller.moveToImagingPick()
        self.dc_controller.dropForam()
        self.vibration_controller.topVibrationPulse()
        self.servo_controller.moveToImagingWebcam()
        return self.request_image_check.format(self.session_foram_count, 'imaging_start', 0)
