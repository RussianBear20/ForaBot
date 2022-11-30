import time
from driver.ForamsSystem import ForamsSystem

class ForamsSystemTesting(ForamsSystem):
    def __init__(self, config_file_location):
        self.is_present_funnel_msg = '{"end_point":"camera","function":"isForamInFunnel","args":[]}'
        self.is_present_funnel_second_msg = '{"end_point":"camera","function":"isForamInFunnelConfirm","args":[]}'
        self.is_present_pin_msg = '{"end_point":"camera","function":"isForamOnNeedle","args":[]}'
        self.is_present_pin_second_msg = '{"end_point":"camera","function":"isForamOnNeedleConfirm","args":[]}'
        super().__init__(config_file_location)

    def testIsolation(self):
        self.motor_controller.pickIsolationForam()
        time.sleep(1)
        self.motor_controller.clearIsolation()
        return self.request_ui_input

    def testImaging(self):
        self.motor_controller.pickImagingForam()
        time.sleep(1)
        self.motor_controller.clearImaging()
        return self.request_ui_input

    def testTransferImagingToIsolation(self):
        self.transferImagingToIsolation()
        return self.request_ui_input

    def runIros(self, num_forams):
        self.run_state = {'num_forams':num_forams, 'curr_foram':0, 'num_foram_failures':0, 'num_image_failures':0, 'curr_fn':0, 'curr_foram_id':None}
        self.run_fns = [self.imageForamStart, self.irosSort]
        self.ret_message = None
        return self.runNextAutomatedStep()

    def runIrosHandoff(self, num_forams):
        self.run_state = {'num_forams':num_forams, 'curr_foram':0, 'num_foram_failures':0, 'num_image_failures':0, 'curr_fn':0, 'curr_foram_id':None}
        self.run_fns = [self.startPickRate, self.irosHandoff, self.endIrosHandoff, self.confirmIrosHandoffEnded]
        self.ret_message = None
        return self.runNextAutomatedStep()

    def runIrosDownUp(self, num_forams):
        self.run_state = {'num_forams':num_forams, 'curr_foram':0, 'num_foram_failures':0, 'num_image_failures':0, 'curr_fn':0, 'curr_foram_id':None}
        self.run_fns = [self.startPickRate, self.downUp, self.endDownUp]
        self.ret_message = None
        return self.runNextAutomatedStep()

    def runIrosPickRate(self, num_forams):
        self.run_state = {'num_forams':num_forams, 'curr_foram':0, 'num_foram_failures':0, 'num_image_failures':0, 'curr_fn':0, 'curr_foram_id':None}
        self.run_fns = [self.startPickRate, self.endPickRate]
        self.ret_message = None
        return self.runNextAutomatedStep()

    def confirmIrosHandoffEnded(self, isPresent):
        if isPresent:
            return self.endFn()
        else:
            self.shutdown()

    def endIrosHandoff(self, isPresent):
        if isPresent:
            return self.endFn()
        else:
            self.servo_controller.moveToImagingPick()
            self.motor_controller.dropFromTop() 
            self.servo_controller.moveToWell()
            return self.is_present_funnel_second_msg

    def irosHandoff(self, isPresent):
        if isPresent:
            self.motor_controller.imagingHalfDown()
            self.servo_controller.moveToImagingPick()
            self.motor_controller.imagingHalfUp()
            self.motor_controller.handoffAtImaging()
            self.servo_controller.moveToWell()
            self.motor_controller.clearImaging()
            return self.is_present_funnel_msg
        else:
            self.motor_controller.clearImaging()
            return self.endFn()

    def startPickRate(self):
        self.servo_controller.moveToWell()
        self.motor_controller.pickImagingForam()
        return self.is_present_pin_msg

    def endPickRate(self, isPresent):
        self.motor_controller.clearImaging()
        return self.endFn()

    def endFn(self):
        self.run_state['curr_fn'] += 1
        self.run_state['curr_fn'] = self.run_state['curr_fn']%len(self.run_fns)
        self.run_state['curr_foram'] += self.run_state['curr_fn'] == 0
        if self.checkRunComplete() or self.checkSystemFailure():
            self.ret_message = self.request_ui_input
            return self.ret_message
        else:
            msg = self.runNextAutomatedStep()
            self.run_state['curr_fn'] -= 1
            return msg

    def irosSort(self, well_id):
        self.imageForamEnd()
        return self.sortForam(well_id)

    def pickImaging(self):
        self.motor_controller.pickImagingForam()
        return self.request_ui_input

    def clearImaging(self):
        self.motor_controller.clearImaging()
        return self.request_ui_input

    def downUp(self, isPresent):
        if isPresent:
            self.motor_controller.imagingDownUp()
            return self.is_present_pin_second_msg
        else:
            return self.endFn()

    def endDownUp(self):
        self.motor_controller.clearImaging()
        return self.endFn()

    def imageForam(self):
        self.servo_controller.moveToImaging()
        self.motor_controller.pickImagingForam()
        self.servo_controller.lightForam(0)
        time.sleep(1)
        self.servo_controller.lightOff()
        self.motor_controller.clearImaging()
        return self.ret_message

    def sortForamTest(self, well_idx):
        self.servo_controller.moveWellToIdx(well_idx)
        self.servo_controller.moveToImagingPick()
        self.motor_controller.pickImagingForam()
        self.motor_controller.handoffAtImaging()
        self.servo_controller.moveToWell()
        self.motor_controller.dropFromTop()   
        return self.ret_message 
