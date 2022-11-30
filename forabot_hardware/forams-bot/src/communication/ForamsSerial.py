import serial
import random
import time

'''
The following describes the message patter where %message_id% would represent the value of message_id, not the string:
"<%length_of_message_content%_x_%message_id%_x_%message_content%_x_%message_id%>".
Note the following substrings are reserved for the system to easily parse the data: "_x_", "<", ">".
Other formats may result in the message being ignored or unexpected function.
Note the message_content can be:
"Client In Control", "Server In Control, "Server Requesting Control", or any other string follwing the pattern:
function:%function_name%,vars:[%ordered_variables_for_accompanying_function%]
'''
class ForamsSerial():
    def __init__(self, channel ,is_controlling, message_handler):
        self.logger = None
        self.ser = serial.Serial(channel, 115200, timeout = 0.5)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        self._setupMessageConstants()
        self.is_controlling = is_controlling
        self.message_handler = message_handler
        self.is_running = True

    def _setupMessageConstants(self):
        self.message_break = '_x_'
        self.message_start = '<'
        self.message_end = '>'
        self.message_end_b = self.message_end.encode('utf-8')
        self.successful_id_addon = "_True"
        self.pass_control_message = 'Passing Control'
        self.get_control_message = 'Accepting In Control'
        self.request_connection_check = 'Requesting Connection'
        self.shutdown_msg = '{"function":"shutdown","args":[]}'
        self.stop_msg = '{"function":"stop","args":[]}'
        self.pass_control_len = str(len(self.pass_control_message))
        self.id_len = 5
        self.timeout = 1

    def run(self):
        raise NotImplementedError

    def _enterStateGraph(self, message_to_run=None):
        while self.is_running:
            if self.is_controlling:
                next_command = self.message_handler.runFunctionFromMessage(message_to_run)
                self._passControl(next_command)
                if next_command == self.shutdown_msg:
                    self.shutdown()
                self.is_controlling = False
            else:
                message_to_run = self._waitForControl()
                self._acceptingControl()
                self.is_controlling = True
                if message_to_run == self.shutdown_msg:
                    self.shutdown()

    def _acceptingControl(self):
        message, message_id = self._writeMessage(self.get_control_message)
        self._waitReceiptConfirmation(message, message_id)

    def _waitForControl(self):
        message_to_handle = None
        while True:
            message, message_id = self._getMessage()
            self._confirmReceipt(message_id, True)
            if message == self.pass_control_message:
                return message_to_handle
            elif message != self.get_control_message:
                message_to_handle = message

    def _getMessage(self):
        successful = False
        while not successful:
            message_id, message, successful = self._getFullMessage()
        return message, message_id

    def _waitReceiptConfirmation(self, rec_message, rec_message_id, fn_check = lambda x: False):
        successful = False
        passed_by_lambda = False
        while not successful:
            message_id, message, successful = self._getFullMessage()
            if message == rec_message_id+self.successful_id_addon:
                successful = True
            elif fn_check(message):
                self._confirmReceipt(message_id,True)
                successful = True
                passed_by_lambda = True
            else:
                self.ser.write(rec_message)
                received_data = ''
                successful = False
        return passed_by_lambda

    def _getFullMessage(self):
        start = time.time()
        no_change = time.perf_counter()
        data_left = self.ser.in_waiting
        received_data_b = self.ser.read_until(self.message_end_b,data_left)
        received_data = received_data_b.decode('utf-8')
        while self._checkDataIncomplete(received_data):
            time.sleep(0.01)
            data_left = self.ser.in_waiting
            if data_left > 0:
                received_data_b = self.ser.read_until(self.message_end_b,data_left)
                received_data += received_data_b.decode('utf-8')
                no_change = time.perf_counter()
            elif (time.perf_counter()-no_change) > self.timeout:
                return -1, "", False
        message_id, message, successful = self._extractMessageInfo(received_data)
        return message_id, message, successful

    def _confirmReceipt(self, message_id, successful):
        self._writeMessage(message_id + '_' +str(successful))

    def _checkDataIncomplete(self, current_data):
        if len(current_data) == 0:
            return True
        return current_data[-1] != self.message_end

    def _extractMessageInfo(self, received_data):
        message = ''
        message_id = ''
        split_data = received_data.split(self.message_break)
        try:
            msg_len = int(split_data[0].strip(self.message_start))
            msg_len_offset = len(split_data[0])-1
            message_id = split_data[1]
            message = split_data[2]
            end_id = split_data[3].strip(self.message_end)
        except:
            return message_id, message, False
        is_successful = len(message) == msg_len and end_id == message_id
        return message_id, message, is_successful

    def _createMessage(self, message_content):
        message_len = str(len(message_content))
        message_id = self._createMessageId()
        message = self.message_start + message_len + self.message_break + message_id + self.message_break + message_content + self.message_break + message_id + self.message_end
        return message.encode('utf-8'), message_id

    def _createMessageId(self):
        num = random.randint(1,10**(self.id_len)) - 1
        return str(num).zfill(self.id_len)

    def _writeMessage(self, message_base):
        message, message_id = self._createMessage(message_base)
        self.ser.write(message)
        return message, message_id

    def _passControl(self, accompanying_message):
        if accompanying_message is not None:
            message, message_id = self._writeMessage(accompanying_message)
            self._waitReceiptConfirmation(message, message_id)
        message, message_id = self._writeMessage(self.pass_control_message)
        passed_by_lambda = self._waitReceiptConfirmation(message, message_id, lambda x: x == self.get_control_message)
        if not passed_by_lambda:
            self._confirmControlAccepted()

    def _confirmControlAccepted(self):
        message = ""
        while message != self.get_control_message:
            message, message_id = self._getMessage()
        self._confirmReceipt(message_id,True)

    def shutdown(self):
        self.is_running = False
